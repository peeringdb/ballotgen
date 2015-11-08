#!/usr/bin/env python

from bs4 import BeautifulSoup
import click
import munge
import munge.codec.all
import re
import requests


def status_msg(msg):
    click.echo(msg)


def parser(data):
    return BeautifulSoup(data, "html.parser")


def get_gov_list(passwd, host='http://lists.peeringdb.com'):
    """ get member list from mailman page """
    # TODO - requires chunk size set correctly, or chunk parsing
    url = host + "/cgi-bin/mailman/admin/pdb-gov/members"
    status_msg("getting mailing list members from %s..." % host)

    # login
    r = requests.post(url, data={"adminpw": passwd}, stream=True)
    length = int(r.headers.get("content-length", 0))
    status_msg("parsing %d bytes..." % length)
    soup = parser(r.content)
    if "Authentication" in soup.title.string:
        raise IOError("list authentication failed")

    return soup


def get_gov_list_file(filename):
    """ get member list from file """
    status_msg("getting mailing list members from file %s..." % filename)
    with open(filename) as html:
        soup = parser(html.read())
        return soup


def parse_gov_list(soup):
    """ parse email addrs from member doc """
    nodes = soup.findAll("input", {"name": re.compile('_realname$')})
    members = []
    status_msg("compiling member list...")
    for node in nodes:
        members.append({
            "email": node.parent.previous_sibling.string,
            "name": node['value'],
        })

    status_msg("got %d members" % len(members))
    return members


def get_users():
    raise Exception("live user list is not yet supported")


def get_users_file(filename):
    status_msg("getting users from file %s..." % filename)
    users = munge.load_datafile(filename, '.')
    status_msg("got %d users" % len(users))
    return users


def get_mapping_file(filename):
    status_msg("getting mapping from file %s..." % filename)
    data = munge.load_datafile(filename, '.')
    status_msg("got %d email mappings" % len(data))
    return data


def build_set(dict_list, key):
    r = {x[key] for x in dict_list}
    return r


def find_voters(members, users, mapping):
    status_msg("finding voters...")
    # make sets / indices
    member_emails = build_set(members, 'email')
    member_idx = {x['email']: x['name'] for x in members}
    user_emails = build_set(users, 'email')
    user_idx = {x['name']: x['email'] for x in users}
    map_emails = mapping['email']

    found = member_emails & user_emails
    status_msg("direct matches %d/%d" % (len(found), len(member_emails)))

    left = member_emails - found
    name_matches = set()
    mapped = set()
    status_msg("leaving %d" % len(left))
    status_msg("checking for email+<something>@domain matches")
    status_msg("checking mapping file")
    for email in left:
        # check mapping file
        if email in map_emails:
            if email not in user_emails:
                ValueError("mapping %s -> %s not found", email, map_emails[email])
            mapped.add(email)

        # check for +something and remove it
        (new, count) = re.subn("\+\w+@", "@", email)
        if count and new in user_emails:
            found.add(new)
            continue

    left -= mapped
    status_msg("%d mapped, leaving %d" % (len(mapped), len(left)))

    # check for name matches, use pdb email
    status_msg("checking for full name matches:")
    for email in left:
        name = member_idx[email]
        if name in user_idx:
            print "  %s: %s" % (user_idx[name], email)
            found.add(user_idx[name])
            name_matches.add(email)

    left -= name_matches
    status_msg("%d name matches, leaving %d" % (len(name_matches), len(left)))
    print "unhandled:", left


@click.command()
@click.option('--list-file', help='use this file instead of getting live')
@click.option('--list-passwd', help='admin password for the gov list')
@click.option('--map-file', default='map', help='mapping file for email addresses')
@click.option('--users-file', help='use this file instead of getting live')
def ballotgen(list_file, list_passwd, map_file, users_file):
    """make a ballot list"""

    # get list members
    if list_file:
        soup = get_gov_list_file(list_file)
    else:
        soup = get_gov_list(list_passwd)

    members = parse_gov_list(soup)

    # pdb users
    if users_file:
        users = get_users_file(users_file)
    else:
        users = get_users()

    mapping = get_mapping_file(map_file)

    find_voters(members, users, mapping)

if __name__ == '__main__':
    ballotgen()
