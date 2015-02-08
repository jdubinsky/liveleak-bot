#!/usr/bin/python3

from flask import Flask
import requests
import json

app = Flask(__name__)

@app.route("/liveleak/<title>")
def social_search(title):
    r = _social_search_helper(title)
    comment = None
    for i in range(len(r['items'])):
        comment = r['items'][0]['description'].strip()
        if len(comment) > 0:
            break

    if comment is None or len(comment) == 0:
        comment = "Shit! Jacob Bot didn't find anything about {0}".format(title)

    return comment

def _social_search_helper(title):
    BASE_URL = "http://socialmention.com/search?q="
    URI_EXTENSIONS = "&f=json&t=comments&src=facebook"
    r = requests.get(BASE_URL + title + URI_EXTENSIONS)
    return json.loads(r.text)

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0")



