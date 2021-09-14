import json
from ast import literal_eval
from flask import Flask, request
from db.sql import MySQLDBConn
from db.redis_cache import RedisCache
from utils import convert_json_serialisable


app = Flask(__name__)

@app.route("/outdated-pages/category/<category>", methods=['GET'])
def get_outdated_pages_by_category(category):
    try:
        if not category:
            return {"msg":"no input given"}, 400
        if RedisCache.rconn.exists(category):
            data = RedisCache.rconn.get(category)
            if data:
                data = json.loads(data)
                return {"data":data}, 200
        else:
            return {"msg":"category not in cache"}, 404
    except Exception as e:
        msg = "Error: unable to fetch results: "+str(e)
        return {"msg":msg}, 500

@app.route("/execute-sql", methods=['POST'])
def execute_query():
    try:
        print(request.json["query"])
        data = convert_json_serialisable(MySQLDBConn.execute_query(request.json["query"]))
        return {"result":data}, 200
    except Exception as e:
        msg = "Error: unable to execute query: "+str(e)
        return {"result":[msg]}, 500




if __name__ == '__main__':
    app.run()
