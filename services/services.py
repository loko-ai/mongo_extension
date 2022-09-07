import logging

import pymongo
from flask import Flask, request, jsonify

app = Flask("")

client = pymongo.MongoClient(host="mongo")
db = client.test_database


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

    ret = list(db[coll].find(value))
    print(ret)
    logging.error(ret)
    for el in ret:
        el['_id'] = str(el['_id'])
    return jsonify(ret)


@app.route("/delete", methods=["POST"])
def delete():
    value = request.json.get("value")
    args = request.json.get("args", {})
    coll = args['collection']

    ret = db[coll].delete_many(value)
    return jsonify(f"{ret.deleted_count} documents deleted")


if __name__ == "__main__":
    app.run("0.0.0.0", 8080)
