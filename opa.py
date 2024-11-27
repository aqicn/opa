import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from urllib.error import HTTPError, URLError
from socket import timeout
import configparser
import time

class Configuration:
    

    def __init__(self,filename='opa.ini'):
        self.config = configparser.ConfigParser()
        self.config.read(filename)

    def IP(self):
        return self.config.get('pa_local_api', 'ip')
    
    def json(self):
        return {s:dict(self.config.items(s)) for s in self.config.sections()}
        
    
class Response:
    text: str
    status_code: int

    def __init__(self,text,status_code):
        self.status_code = status_code
        self.text = text

    def json(self):
        try:
            output = json.loads(self.text)
        except json.JSONDecodeError:
            output = None
        return output
    

def fetch(
    url: str,
    data: dict = None,
    params: dict = None,
    headers: dict = None,
    method: str = "GET",
):
    if not url.casefold().startswith("http"):
        raise urllib.error.URLError("Incorrect and possibly insecure protocol in url")
    method = method.upper()
    request_data = None
    headers = headers or {}
    data = data or {}
    params = params or {}
    headers = {"Accept": "application/json", **headers}

    if method == "GET":
        params = {**params, **data}
        data = None

    if params:
        url += "?" + urllib.parse.urlencode(params, doseq=True, safe="/")

    if data:
        request_data = json.dumps(data).encode()
        headers["Content-Type"] = "application/json; charset=UTF-8"

    httprequest = urllib.request.Request(
        url, data=request_data, headers=headers, method=method
    )

    print("fetch(%s): "%url,end="")
    sys.stdout.flush()


    try:
        with urllib.request.urlopen(httprequest, timeout=10) as httpresponse:
            print("response status %d"%httpresponse.status)
            body = httpresponse.read().decode(
                    httpresponse.headers.get_content_charset("utf-8")
                )
            return Response(
                status_code=httpresponse.status,
                text=body,
            )
    except HTTPError as e:
        print("http error %d"%e.code)
    except URLError as e:
        if isinstance(e.reason, timeout):
            print("timeout")
        else:
            print("error %s"%e.reason)
        
    response = Response(
        status_code=0,
        text="error",
    )
        
    return response


   


class Exporter:
    
    def __init__(self):
        self.config = Configuration()
        
    def run(self):
        while True:
            data = self.fetch_purple_air(self.config.IP())
            if data is not None:
                self.export(data)
            time.sleep(60)

    def fetch_purple_air(self, ip):
        url = "http://"+ip+"/json"
        r = fetch(url)
        if r.status_code!=200:
            print("Sorry, failed to access the local PurpleAir API at %s: http error %d"%(url,r.status_code))
            print(r.text)
            return None

        if r.json()is None:
            print("Sorry, failed to access the local PurpleAir  at %s: Invalid JSON (%s...)"%(url,r.text[:50]))
            return None
            
        return r.json()


    def export(self, data):
        url = "http://127.0.0.1:88/sensor/upload"
        r= fetch(url, data={"opa":data,"config":self.config.json()}, method="POST")
        if r.status_code!=200:
            print("Sorry, failed to upload to the WAQI server at %s: http error %d"%(url,r.status_code))
            print(r.text)
            return None

        response_json = r.json()
        if response_json is None:
            print("Invalid response (not JSON): %s"%r.text)
        elif response_json["status"]!="ok":
            print("Sorry, failed to upload to the WAQI server at %s: response %s"%(url, json.dumps(response_json, indent=2)))
        else:
            print("all fine\n%s"%(json.dumps(response_json, indent=2)))
        

Exporter().run()
