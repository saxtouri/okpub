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

from kamaki.clients import Client, utils, astakos, cyclades


class KeyAPI(Client):
    """A kamaki-based API client for  public Key API"""

    @staticmethod
    def get_endpoint_url(auth_url):
        """Use the authentication URL and astakos to construct Key API url"""
        auth = astakos.AstakosClient(auth_url, '')
        compute_endpoint = auth.get_endpoint_url(
            cyclades.CycladesComputeClient.service_type)
        endpoint, _ = compute_endpoint.split('/compute')
        return endpoint

    def list_public_keys(self):
        """List all public keys"""
        self.set_header('Content-Type', 'application/json')
        path = utils.path4url('userdata', 'keys')
        r = self.get(path, success=(200, ))
        return r.json

    def get_public_key(self, key_id):
        """Get the full information of a public key"""
        self.set_header('Content-Type', 'application/json')
        path = utils.path4url('userdata', 'keys', key_id)
        r = self.get(path, success=(200, ))
        return r.json
