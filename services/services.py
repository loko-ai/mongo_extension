import logging

import pymongo
from flask import Flask, request, jsonify

from config.app_config import HOST, PORT, USERNAME, PASSWORD, DB

app = Flask("")

client = pymongo.MongoClient(host=HOST, port=PORT, username=USERNAME, password=PASSWORD)
db = client[DB]

@app.route("/", methods=["POST"])
def test():
    value = request.json.get("value")
    args = request.json.get("args", {})
    coll = args['collection']
    if not isinstance(value, list):
        value = [value]
    db[coll].insert_many(value)
    return jsonify(dict(msg=f"{len(value)} documents inserted"))


@app.route("/query", methods=["POST"])
def query():
    value = request.json.get("value")
    args = request.json.get("args", {})
    coll = args['collection']
    logging.error(value)
    logging.error(args)
    stream = args.get("stream")

    ret = list(db[coll].find(value))
    print(ret)
    logging.error(ret)
    for el in ret:
        el['_id'] = str(el['_id'])
    if stream:
        return jsonify(ret)
    else:
        return jsonify(dict(data=ret))


@app.route("/delete", methods=["POST"])
def delete():
    value = request.json.get("value")
    args = request.json.get("args", {})
    coll = args['collection']

    ret = db[coll].delete_many(value)
    return jsonify(f"{ret.deleted_count} documents deleted")


@app.route("/list", methods=["POST"])
def list_collections():
    value = request.json.get("value")
    args = request.json.get("args", {})
    ret = {}
    for coll in db.list_collection_names():
        ret[coll] = db[coll].count_documents({})

    return jsonify(ret)


if __name__ == "__main__":
    app.run("0.0.0.0", 8080)
