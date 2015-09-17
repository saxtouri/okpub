# Copyright (c) 2015, Stavros Sachtouris
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# 
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import argparse
from os import environ


OKPUB_URL = environ.get('OKPUB_URL')
OKPUB_TOKEN = environ.get('OKPUB_TOKEN')
OKPUB_CA_CERTS = environ.get('OKPUB_CA_CERTS')


def main():
    """CLI entry point"""

    # Check syntax
    parser = argparse.ArgumentParser(description='Access your cloud keys')
    parser.add_argument('--key-id', help='Get only a specific key')
    parser.add_argument('--url',
        help='Cloud authentication URL, can be set as OKPUB_URL env variable')
    parser.add_argument('--token',
        help='Cloud user token, can be set as OKPUB_TOKEN env variable')
    parser.add_argument('--ca-certs',
        help='Path to CA certificates for SSL, can be set as OKPUB_CA_CERTS '
             'env variable')
    parser.add_argument('--ignore-ssl',
        action='store_true',
        help='Ignore SSL (not recomended), ignores CA certificates path')
    args = parser.parse_args()

    url = args.url or OKPUB_URL
    token = args.token or OKPUB_TOKEN
    assert all([url, token]), 'Both URL and TOKEN required (-h for more)'

    ca_certs = args.ca_certs or OKPUB_CA_CERTS
    assert any([ca_certs, args.ignore_ssl]), (
        'You should either set ca_certs or --ignore-ssl (-h for more)')

    # Resolve SSL issue
    from kamaki.clients.utils import https
    if args.ignore_ssl:
        https.patch_ignore_ssl()
    else:
        https.patch_with_certs(ca_certs)

    # Initialize client
    from okpub.client import KeyAPI
    endpoint = KeyAPI.get_endpoint_url(url)
    client = KeyAPI(endpoint, token)

    # Get results and print
    import json
    from sys import stdout
    if args.key_id:
        r = client.get_public_key(args.key_id)
    else:
        r = client.list_public_keys()
    stdout.write(json.dumps(r, indent=2))
    stdout.write('\n')
    stdout.flush()
