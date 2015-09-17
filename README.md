okpub
=====

Overview
--------

A minimal python library and CLI for the ~okeanos public key API

Setup
-----

First, install:

    $ python setup.py install

Now you need to declare a cloud URL, user TOKEN and a path to the CA
certificates bundle. E.g. in a debian environment with bash and the standard
~okeanos deployment:

    $ export OKPUB_URL="https://accounts.okeanos.grnet.gr/identity/v2.0"
    $ export OKPUB_TOKEN="your token here"
    $ export OKPUB_CA_CERTS="/etc/ssl/certs/ca-certificates.crt"

You can provide these values on runtime too (--url, --token, --ca-certs)

Usage
-----

List your public keys:

    $ okpub

Get information on a public key with id 1234:

    $ okpub --key-id=1234
