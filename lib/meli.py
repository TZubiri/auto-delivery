 #!/usr/bin/env python
# -*- coding: utf-8 -*-

from lib.ssl_helper import SSLAdapter
import urllib.parse
import json
import os
import re
import requests
import ssl

class Meli(object):
    def __init__(self, client_id, client_secret, access_token=None, refresh_token=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expires_in = None 

        self.API_ROOT_URL = 'https://api.mercadolibre.com'
        self.SDK_VERSION = 'MELI-PYTHON-SDK-1.0.1'
        self.AUTH_URL = 'https://auth.mercadolibre.com'
        self.OAUTH_URL = '/oauth/token'

        self._requests = requests.Session()
        self.SSL_VERSION = 'PROTOCOL_TLSv1'
        self._requests.mount('https://', SSLAdapter(ssl_version=getattr(ssl, self.SSL_VERSION)))


    #AUTH METHODS
    def auth_url(self,redirect_URI):
        params = {'client_id':self.client_id,'response_type':'code','redirect_uri':redirect_URI}
        url = self.AUTH_URL  + '/authorization' + '?' + urllib.parse.urlencode(params)
        return url

    def authorize(self, code, redirect_URI):
        params = { 'grant_type' : 'authorization_code', 'client_id' : self.client_id, 'client_secret' : self.client_secret, 'code' : code, 'redirect_uri' : redirect_URI}
        headers = {'Accept': 'application/json', 'User-Agent':self.SDK_VERSION, 'Content-type':'application/json'}
        uri = self.make_path(self.OAUTH_URL)

        response = self._requests.post(uri, params=urllib.parse.urlencode(params), headers=headers)

        if response.status_code == requests.codes.ok:
            response_info = response.json()
            self.access_token = response_info['access_token']
            if 'refresh_token' in response_info:
                self.refresh_token = response_info['refresh_token']
            else:
                self.refresh_token = '' # offline_access not set up
                self.expires_in = response_info['expires_in']

            return self.access_token
        else:
            # response code isn't a 200; raise an exception
            response.raise_for_status()

    def get_refresh_token(self):
        if self.refresh_token:
            params = {'grant_type' : 'refresh_token', 'client_id' : self.client_id, 'client_secret' : self.client_secret, 'refresh_token' : self.refresh_token}
            headers = {'Accept': 'application/json', 'User-Agent':self.SDK_VERSION, 'Content-type':'application/json'}
            uri = self.make_path(self.OAUTH_URL)

            response = self._requests.post(uri, params=urllib.parse.urlencode(params), headers=headers, data=params)

            if response.status_code == requests.codes.ok:
                response_info = response.json()
                self.access_token = response_info['access_token']
                self.refresh_token = response_info['refresh_token']
                self.expires_in = response_info['expires_in']
                return self.access_token
            else:
                # response code isn't a 200; raise an exception
                response.raise_for_status()
        else:
                raise Exception("Offline-Access is not allowed.")

    # REQUEST METHODS
    def get(self, path, params={}):
        headers = {'Accept': 'application/json', 'User-Agent':self.SDK_VERSION, 'Content-type':'application/json'}
        uri = self.make_path(path)
        response = self._requests.get(uri, params=urllib.parse.urlencode(params), headers=headers)
        return response

    def post(self, path, body=None, params={}):
        headers = {'Accept': 'application/json', 'User-Agent':self.SDK_VERSION, 'Content-type':'application/json'}
        uri = self.make_path(path)
        if body:
            body = json.dumps(body)

        response = self._requests.post(uri, data=body, params=urllib.parse.urlencode(params), headers=headers)
        return response

    def put(self, path, body=None, params={}):
        headers = {'Accept': 'application/json', 'User-Agent':self.SDK_VERSION, 'Content-type':'application/json'}
        uri = self.make_path(path)
        if body:
            body = json.dumps(body)

        response = self._requests.put(uri, data=body, params=urllib.parse.urlencode(params), headers=headers)
        return response

    def delete(self, path, params={}):
        headers = {'Accept': 'application/json', 'User-Agent':self.SDK_VERSION, 'Content-type':'application/json'}
        uri = self.make_path(path)
        response = self._requests.delete(uri, params=params, headers=headers)
        return response

    def options(self, path, params={}):
        headers = {'Accept': 'application/json', 'User-Agent':self.SDK_VERSION, 'Content-type':'application/json'}
        uri = self.make_path(path)
        response = self._requests.options(uri, params=urllib.parse.urlencode(params), headers=headers)
        return response

    def make_path(self, path, params={}):
        # Making Path and add a leading / if not exist
        if not (re.search("^http", path)):
            if not (re.search("^\/", path)):
                path = "/" + path
            path = self.API_ROOT_URL + path
        if params:
            path = path + "?" + urllib.parse.urlencode(params)
        return path