from flask import Flask
from flask import request, jsonify, render_template

app = Flask(__name__)

from main import get_similar_tags
from inverted_index_elections import POPULARITY_INDEX,INVERTED_INDEX, INVERTED_INDEX_CLEAN

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/r')
def recomendation_query():
    query = request.args.get('q', None)
    if query:
       result = get_similar_tags(query, INVERTED_INDEX, INVERTED_INDEX_CLEAN, 5)
    else:
        result = None
    return jsonify({"results":[result], "query" : query})

@app.route('/ac')
def autocomplete_query():
    query = request.args.get('q', None)
    pop_keys = POPULARITY_INDEX.keys()
    array = [x  for x in pop_keys if query.lower() in str(x).lower()][0:8]
    return jsonify({'results':array, "query" : query})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="7000", debug=True)

