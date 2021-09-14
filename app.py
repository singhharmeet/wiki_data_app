from flask import Flask, request

app = Flask(__name__)

@app.route("/outdated-pages/category/<category>", methods=['GET'])
def get_outdated_pages_by_category(category):
    return category

@app.route("/execute-sql", methods=['POST'])
def execute_query():
    print(request.json)
    return request.json["query"]




if __name__ == '__main__':
    app.run()
