from flask import Flask
from flask import request, jsonify, render_template

app = Flask(__name__)

from main import get_similar_tags, cleanup, recommendOriginal
from inverted_index_elections import POPULARITY_INDEX, POPULARITY_INDEX_CLEAN, INVERTED_INDEX, INVERTED_INDEX_CLEAN

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/r')
def recomendation_query():
    query = request.args.get('q', None)
    if query:
       result = get_similar_tags(query, INVERTED_INDEX, INVERTED_INDEX_CLEAN, 8)
    else:
        result = None
    result = list(set([x for x in result if x.lower() != query.lower()]))
    return jsonify({"results":[result], "query" : query})

@app.route('/ac')
def autocomplete_query():
    print("Autocomplete query started")
    query = request.args.get('q', None)
    query = cleanup(query)#query.lower()
    pop_keys = POPULARITY_INDEX_CLEAN
    output = []
    for key in pop_keys:
        if query in key and key.lower() not in output:
            output.append(key)
    popularity_array = []
    for o in output:
        popularity_array.append(POPULARITY_INDEX_CLEAN[o])
    print("Output:", output)
    print("Popularity Array:", popularity_array)
    final_output = []
    while len(popularity_array) > 0:
        max_ = max(popularity_array)
        i = popularity_array.index(max_)
        final_output.append(output[i])
        output.pop(i)
        popularity_array.pop(i)
    for i,item in enumerate(final_output[0:8]):
        final_output[i] = recommendOriginal(INVERTED_INDEX, item)
    return jsonify({'results':final_output[0:8], "query" : query})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
