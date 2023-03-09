import requests


class ProxyAPIException(Exception):
    pass


class RequestError(ProxyAPIException):
    pass


class ResponseError(ProxyAPIException):
    pass


def newip(hostport, credentials=''):
    host, port = hostport.split(':')

    url = "http://%s:1294/control/%s/newip" % (host, port)
    error = None
    try:
        if credentials == '':
            response = requests.get(url)
        else:
            login, password = credentials.split(':')
            response = requests.get(url, auth=(login, password))
    except requests.exceptions.RequestException as e:
        error = e

    if error is not None:
        raise RequestError("Error making a request: %s" % str(error))

    if response.status_code == 200:
        return
    else:
        raise ResponseError(
            "Received %d code from server, response body is \"%s\"" % (response.status_code, response.text.strip()))