import urllib.request as req
import json

def getJson(url):
    with req.urlopen(url) as url:
        data = json.loads(url.read().decode())
        print(data)

def main():
    getJson('https://randomuser.me/api/')

main()
