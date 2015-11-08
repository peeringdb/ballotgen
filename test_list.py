
import ballotgen
import pytest


test_members = [
    {
    'email': u'user@example.com',
    'name': u'Example User'
    },
    {
    'email': u'second@example.com',
    'name': u''
    }
]
test_members_emails = set([u'second@example.com', u'user@example.com'])

test_users = [
    {
    'email': u'user@example.com',
    'name': u'Example User'
    },
    {
    'email': u'second.user@example.com',
    'name': u''
    }
]

mapping = {
    'email': {
        'second@example.com': 'second.user@example.com',
    },
    'org': {
        'example.com': 'user',
    },
}


def test_get_gov_list():
    with pytest.raises(IOError):
        ballotgen.get_gov_list('badpass')


def test_parse_gov_list():
    soup = ballotgen.get_gov_list_file("tests/data/test-members.html")
    assert test_members == ballotgen.parse_gov_list(soup)


def test_users_file():
    data = ballotgen.get_users_file("tests/data/test-users.yaml")
    assert test_users == data


def test_build_set():
    assert test_members_emails == ballotgen.build_set(test_members, 'email')

    with pytest.raises(KeyError):
        ballotgen.build_set(test_members, 'nonexistant')


def test_voters():
    expected = set(['user@example.com', 'second.user@example.com'])
    found = ballotgen.find_voters(test_members, test_users, mapping)
    assert expected == found

    bad_mapping = {'email': {'second@example.com': 'nonexistant'}}
    with pytest.raises(ValueError):
        ballotgen.find_voters(test_members, test_users, bad_mapping)


def test_reduce_org():
    bad_mapping = {'org': {'example.com': 'nonexistant'}}
    with pytest.raises(ValueError):
        ballotgen.reduce_org(test_members_emails, bad_mapping)

    assert set(['user@example.com']) == ballotgen.reduce_org(test_members_emails, mapping)

