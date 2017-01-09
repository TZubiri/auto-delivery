import oauth2client.transport
import oauth2client.client
import httplib2
import re
import requests
try:
    import urlparse
    from urllib import urlencode
except: # For Python 3
    import urllib.parse as urlparse
    from urllib.parse import urlencode

old_Http = httplib2.Http
class new_Http(old_Http):
    def request(self,uri, method='GET', body=None, headers=None,
                    redirections=httplib2.DEFAULT_MAX_REDIRECTS,
                    connection_type=None):
        if b'Authorization' in headers:
            access_token = re.search(r'Bearer (.*)$',str(headers[b'Authorization'],'ASCII'),re.U).group(1)
            if re.search('mercadolibre',uri,re.I):
                params = {'access_token': access_token }

                url_parts = list(urlparse.urlparse(uri))
                query = dict(urlparse.parse_qsl(url_parts[4]))
                query.update(params)

                url_parts[4] = urlencode(query)
                uri = urlparse.urlunparse(url_parts)

        return old_Http.request(self,uri,method,body,headers,redirections,connection_type)

httplib2.Http = new_Http

def undo_monkey_patch():
    httplib2.Http = old_Http