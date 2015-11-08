
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
    'email': u'second@example.com',
    'name': u''
    }
    ]


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
    pass
