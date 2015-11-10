# ballotgen

Script to read from both the pdb-gov list and the PeeringDB user database and generate a ballot list for voting. Uses Python 2.7.

### install
    pip install -r facsimile/requirements.txt

### testing
    pip install -r facsimile/requirements-test.txt
    py.test test_list.py 

### map file format
    email:
      <pdb-gov email>: <pdb2 user email>
    org:
      # if there are two addresses, user.a@example.com and user.b@example.com
      # to make user.a the voting member, do
      # example.com: user.a
      <domain>: <voting mailbox name>

### usage
    ./ballotgen.py --help
    Usage: ballotgen.py [OPTIONS]

      make a ballot list

    Options:
      --list-file TEXT    use this file instead of getting live
      --list-passwd TEXT  admin password for the gov list
      --map-file TEXT     mapping file for email addresses
      --users-file TEXT   use this file instead of getting live
      --help              Show this message and exit.

For dev runs, save full memberlist to `pdb-gov-members.html`, then generate a full user list with `./manage.py pdb_dump_users --output=users.yaml` and run the following command.

    ./ballotgen.py --list-file=pdb-gov-members.html --users-file=users.yaml 

