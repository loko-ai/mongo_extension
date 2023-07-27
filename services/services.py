import logging

import pymongo
from flask import Flask, request, jsonify
from loguru import logger
from loko_extensions.business.decorators import extract_value_args
from loko_extensions.model.components import Component, Input, Output, Arg, save_extensions
from werkzeug.exceptions import NotFound

from config.app_config import HOST, PORT, USERNAME, PASSWORD, DB
from doc.doc import mongo_doc

mongo = Component("MongoDB",
                  inputs=[Input("insert", service="insert", to="insert_output"),
                          Input("query", service="query", to="query_output"),
                          Input("list", service="list", to="list_output"),
                          Input("delete", service="delete", to="delete_output")],
                  outputs=[Output("insert_output"), Output("query_output"),
                           Output("list_output"), Output("delete_output")],
                  args=[Arg(name="collection", label="Collection name", helper="Specify the mongo collection name"),
                        Arg(name="stream", type="boolean", label="Stream or not results", description="Stream ")],
                  description=mongo_doc)

save_extensions([mongo])

app = Flask("")

client = pymongo.MongoClient(host=HOST, port=PORT, username=USERNAME, password=PASSWORD)
db = client[DB]

def handle_invalid_usage(exception):
    e = str(exception)
    j = dict(error=e)
    response = jsonify(j)

    if isinstance(exception, NotFound):
        logger.error(NotFound)
        response.status_code = 404
        return response
    logger.exception(e)

    status_code = getattr(exception, "status_code", None) or 500
    response.status_code = status_code
    logger.debug(f'ERROR: {status_code} - {j}')

    return response
@app.route("/insert", methods=["POST"])
@extract_value_args(_request=request)
def insert(value, args):
    coll = args['collection']
    if not isinstance(value, list):
        value = [value]
    db[coll].insert_many(value)
    return jsonify(dict(msg=f"{len(value)} documents inserted"))


@app.route("/query", methods=["POST"])
@extract_value_args(_request=request)
def query(value, args):
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
@extract_value_args(_request=request)
def delete(value, args):
    coll = args['collection']

    ret = db[coll].delete_many(value)
    return jsonify(f"{ret.deleted_count} documents deleted")


@app.route("/list", methods=["POST"])
@extract_value_args(_request=request)
def list_collections(value, args):
    ret = {}
    for coll in db.list_collection_names():
        ret[coll] = db[coll].count_documents({})

    return jsonify(ret)


if __name__ == "__main__":
    app.run("0.0.0.0", 8080)
