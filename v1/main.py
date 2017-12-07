from flask import Flask
from flask import request, jsonify, render_template

app = Flask(__name__)

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

from v1.inverted_index_elections import INVERTED_INDEX, POPULARITY_INDEX

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/r')
def recomendation_query():
    query = request.args.get('q', None)
    if query:
        result = get_similar_tags(query, INVERTED_INDEX)
    else:
        result = None
    return jsonify({"results":[result], "query" : query})

@app.route('/ac')
def autocomplete_query():
    query = request.args.get('q', None)
    array = [x  for x in POPULARITY_INDEX.keys() if query.lower() in str(x).lower()][0:8]
    return jsonify({'results':array, "query" : query})

def get_similar_tags(tag, inverted_index):
    array_of_docs = []
    array_of_tags = []
    for key in inverted_index:
        row = ",".join([str(x) for x in inverted_index[key]])
        array_of_docs.append(row)
        array_of_tags.append(key)
    array_of_docs = np.array(array_of_docs)
    if tag not in array_of_tags:
        return []
    t = array_of_tags.index(tag)

    tfidf = TfidfVectorizer().fit_transform(array_of_docs)
    cosine_similarities = cosine_similarity(tfidf[t:t + 1], tfidf).flatten()
    most_similar_tags = cosine_similarities.argsort()[:-6:-1]

    output_array = []
    print("most_similar_tags", most_similar_tags)
    for t in most_similar_tags:
        output_array.append(array_of_docs[t:t+1])

    similar_tags = [array_of_tags[i] for i in most_similar_tags]
    return (similar_tags[1:])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="7000", debug=True)

