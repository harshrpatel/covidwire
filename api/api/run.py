import flask
from flask import request
from api.creds import db_config
from scipy.spatial.distance import euclidean, cosine
import datetime
import dataset
import json
import time
import html
from urllib.parse import unquote_plus as urldecode
cache = {}

db = dataset.connect(
        f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
    )
articles = db['articles']

app = flask.Flask(__name__)
app.config["DEBUG"] = True
import numpy as np
from collections import defaultdict


@app.route('/', methods=['GET'])
def home():
    defaults = {"_limit": 50}
    kwargs = request.args or {}
    kwargs = dict(**defaults, **request.args)
    formatted_args = '</p><p>'.join([f"{k} = {v}\n" for k,v in request.args.items()])
    results = articles.find(**kwargs)
    formatted_results = '</div><div>'.join([json.dumps(result, indent=4, default=lambda x: x if isinstance(x, (str, int, float, list)) else str(x)).replace(" ", "&nbsp;").replace("\n", "<br>") for result in results])
    return f"""<h1>Query Parameters:</h1><p>{formatted_args}</p>
               <h2>Results:</h2><div>{formatted_results}</div>"""
import random
@app.route('/scored', methods=['GET'])
def get_scored_results():
    print(f"Cache keys: {list(cache.keys())}")
    kwargs = {"_limit": 50, "p": 0, "fips": "06097", "audience": ""}
    _kwargs = {k: urldecode(v) for k,v in request.args.items()} or {}
    kwargs.update(_kwargs)

    fips = kwargs['fips']
    print(f"fips is : {fips}")
    start = int(kwargs['_limit']) * int(kwargs['p'])
    stop = start + int(kwargs['_limit'])
    print(f"Start is: {start}, Stop is: {stop}")
    results = None
    if fips in cache and cache[fips] and cache[fips][0] > time.time():
        results = cache[fips][1]
    else:
        query = f"""SELECT distinct on (title)
        id, published_at, name, title, description, content, url, docvec, ner, image_url, audience, cast(scored ->> '{fips}' as float)  / (extract(days from (now() - published_at)) * 2 + 1) as score
    FROM
        articles
    WHERE scored ->> '{fips}' != '0';"""
        results = []
        for r in sorted(db.query(query), key=lambda x: x['score'], reverse=True):
            try:
                r['docvec'] = list(map(float,r['docvec'][1:-1].split(",")))


            except:
                r['docvec'] = [x*0.00000001 for x in random.sample(range(-70000000,70000000), 8)]
            results.append(r)

        cache[fips] = [time.time() + 3200, results]
    #print(results[start:stop])
    #ormatted_args = '</p><p>'.join([f"{k} = {v}\n" for k, v in request.args.items()])
    #formatted_results = '</div><div>'.join([json.dumps(result, indent=4, default=str).replace(" ", "&nbsp;").replace("\n", "<br>").replace("\\n", "<br>") for result in results[start:stop]])
    if kwargs['audience']:
        audience = kwargs['audience']
        results = [result for result in results if result['audience'] == audience]
    results = results[start:stop]
    response = app.response_class(
        response = json.dumps(results, indent=4, default=lambda x: x if not isinstance(x, datetime.datetime) else x.isoformat()),
        status=200,
        mimetype = 'application/json')
    return response
    # return f"""<h1>Query Parameters:</h1><p>{formatted_args}</p>
    #                <h2>Results:</h2><div>{formatted_results}</div>"""

app.run(host='0.0.0.0', port=8888)

