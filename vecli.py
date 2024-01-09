import argparse
import json
from urllib.request import Request, urlopen, urlretrieve
from pprint import pprint
import  io, sys
 
URL = "https://virus.exchange/"

parser = argparse.ArgumentParser(description='Primitive virus.exchange CLI. Before running, ensure you have a apitoken.json file in the same path as vecli.py.')
parser.add_argument("hash", action="store", help="hash value of sample to download")
parser.add_argument('-c', "--check", action="store_true", help="check if sample exists")
parser.add_argument('-d', '--download', action='store_true', help="download sample")
parser.add_argument('-v', '--verbose', action='store_true', help="if set, show JSON response with metadata")

args = parser.parse_args()

try:
    f = open('apitoken.json')
except:
    print("No apitoken.json found. Please create one containing { APITOKEN: "<token>" }")

data = json.load(f)

token = data["APITOKEN"]

headers = {
    'User-Agent' : 'Mozilla/5.0',
    'Authorization': f'Bearer {token}'
}

def show_progress(url, filename):
    with urlopen(url) as Response:
            Length = Response.getheader('content-length')
            BlockSize = 1000000  # default value

            if Length:
                Length = int(Length)
                BlockSize = max(4096, Length // 20)

            BufferAll = io.BytesIO()
            Size = 0
            while True:
                BufferNow = Response.read(BlockSize)
                if not BufferNow:
                    break
                BufferAll.write(BufferNow)
                Size += len(BufferNow)
                if Length:
                    Percent = int((Size / Length)*100)
                    sys.stdout.write(f"Download: {Percent}% {filename} \r")
                    sys.stdout.flush()


            with open(args.hash, "wb") as f:
                f.write(BufferAll.getbuffer())

            print(f"Download: {Percent}% {filename} \r")
            print("Done.")

if args.check:
    try:
        req = Request(URL + "api/samples/" + args.hash , headers=headers)
        resp = urlopen(req).read()
        resp_json = json.loads(resp)
        print(" ")
        print("File found with metadata:")
        pprint(resp_json)
    except:
        print("Sample not found.")

if args.download:
    # Retrieve JSON response
    try:
        req = Request(URL + "api/samples/" + args.hash , headers=headers)
        resp = urlopen(req).read()
        resp_json = json.loads(resp)
        if args.verbose:
            pprint(resp_json)

        # Extract download link and download sample to disk
        dl_link = resp_json["download_link"]

        show_progress(dl_link, args.hash)
    except:
        print("Unable to access API.")

    