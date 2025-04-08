from flask import Flask, request, render_template
from elasticsearch7 import Elasticsearch

app = Flask(__name__)

CLOUD_ID = "My_deployment:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvOjQ0MyQyNmZjZGU3MDU2ODQ0M2ExOGU4MGNkY2U3ZjQ0NDFhNiQxYmE5MjY3ODFkM2E0NTNiYTkzZjEzZDMxYjU2MDUzMQ=="


# Runs es-builtin retreival model on the query and fetches the top 20 results
def ES_builtin(query):
    es = Elasticsearch(
        request_timeout=10000,
        cloud_id=CLOUD_ID,
        http_auth=("elastic", "zwrRY5OjRfw8xvYaHRNSx78Y"),
    )
    search_result = es.search(index="hw3", query={"match": {"content": query}}, size=200)
    results = []
    rank = 1
    for data in search_result["hits"]["hits"]:
        # for score use data[_score]
        attributes = {}
        attributes["rank"] = rank
        attributes["url"] = data["_source"]["url"]
        results.append(attributes)
        rank += 1
    return results


@app.route("/", methods=["GET", "POST"])
def fetch_results():
    results = []
    if request.method == "POST":
        # Get the query from the form
        query = request.form["query"]
        results = ES_builtin(query)
    return render_template("search.html", results=results[:200])


if __name__ == "__main__":
    app.run(debug=True)
