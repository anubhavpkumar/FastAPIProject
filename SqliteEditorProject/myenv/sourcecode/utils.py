import uuid
import json
from html.parser import HTMLParser

def getCookieFromCookieString(cookieString, cookieKey):
    cookieKeyValue = cookieString.split(';')
    for cookie in cookieKeyValue:
        if (cookie.split("=")[0].strip() == cookieKey):
            return cookie.split("=")[1].strip()
    else:
        return None

def generateSessionId():
    return uuid.uuid4().hex

def convert_bytes_to_json(byte_stream):
    html_parser = HTMLParser()
    form_data = html_parser.unescape(byte_stream.decode('utf8'))
    form_data_kv = form_data.split('&')
    form_data_json = {}
    
    for kv in form_data_kv:
        [key, value] = kv.split('=')
        form_data_json[key] = value 
    return form_data_json