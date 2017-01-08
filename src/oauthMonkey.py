# -*- coding: <encoding name> -*-

import oauth2client.transport
import httplib2
import re
oldRequest = oauth2client.transport.request
def newRequest(http, uri, method='GET', body=None, headers=None,
            redirections=httplib2.DEFAULT_MAX_REDIRECTS,
            connection_type=None):
    body = re.sub(r'(^|&)(scope=[^&]+)($|&)',r"\1\3",body)
    body = re.sub(r'&&', "&", body)
    if 'Content-type' in headers:
        headers['Content-type'] = 'application/json'
    if 'Accept' in headers:
        headers['Accept'] = 'application/json'
    if 'User-Agent' in headers:
        headers['User-Agent'] = 'MELI-PYTHON-SDK-1.0.0'

    return oldRequest(http,uri,method,body,headers,redirections,connection_type)

oauth2client.transport.request = newRequest
