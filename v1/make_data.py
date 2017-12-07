from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import AffinityPropagation
import numpy as np
import pandas as pd
import json

def tokenize_tags(data):
    tags = data['Subject']
    all_tags = []
    for tag_string in tags:
        tag_string = str(tag_string)
        all_tags.extend(tag_string.split(","))
    all_tags = np.asarray(all_tags)
    return all_tags

def cleanup(word):
    if (word == None):
            print("Fingerprint keyer accepts a single string parameter")
    # remove whitespace around the string
    word = word.strip()
    # lowercase the string
    word = word.lower()
    # remove all punctuation and control chars, per https://stackoverflow.com/questions/5843518/remove-all-special-characters-punctuation-and-spaces-from-string
    word = ''.join(e for e in word if e.isalnum())
    # finds ASCII equivalent, per https://stackoverflow.com/questions/21701968/python-the-standard-library-ascii-function
    # not sure if the ascii() function is needed, leaving out to test
    word = ascii(word)
    # splits the word by whitespace, per https://www.tutorialspoint.com/python/string_split.htm
    word = word.split()
    #sort words
    word = sorted(word)
    # removes duplicates
    word = "".join(list(set(word)))
    # sorts array in place
    return word.strip("'")

def make_unclustered_inverted_index(data):
    inverted_index = {}
    popularity_index = {}
    for i, doc in enumerate(data):
        try:
            doc_tags = str(data[doc][0]).split(",")
        except:
            continue
        for tag in doc_tags:
            tag = (tag.strip())
            if inverted_index.get(tag, None):
                inverted_index[tag].append(i)
                popularity_index[tag] += 1
            else:
                inverted_index[tag] = [i]
                popularity_index[tag] = 1
    with open('inverted_index_elections.py', 'w') as file:
        file.write("INVERTED_INDEX = ")
        file.write(json.dumps(inverted_index))
        file.write("\n")
        file.write("POPULARITY_INDEX = ")
        file.write(json.dumps(popularity_index))
    return inverted_index, popularity_index



def make_inverted_index(data, clustered_tags):
    inverted_index = {}
    popularity_index = {}
    for i, doc in enumerate(data):
        doc_tags = str(data[doc][0]).split(",")
        for tag in doc_tags:
            for clustered_tag in clustered_tags:
                arr = clustered_tags.get(clustered_tag, None)
                if arr:  arr.append(clustered_tag)
                else:continue
                if tag in arr:
                    if inverted_index.get(tag, None):
                        inverted_index[tag].append(i)
                        popularity_index[tag] += 1
                    else:
                        inverted_index[tag] = [i]
                        popularity_index[tag] = 1
                    break
    with open('inverted_index_elections.py', 'w') as file:
        file.write("INVERTED_INDEX = ")
        file.write(json.dumps(inverted_index))
        file.write("\n")
        file.write("POPULARITY_INDEX = ")
        file.write(json.dumps(popularity_index))
    return inverted_index, popularity_index

def cluster(data, tags, clean_tags):
    affprop = AffinityPropagation(preference=100)
    affprop.fit(data)
    clustered_tags = {}
    for cluster_id in np.unique(affprop.labels_):
        exemplar = clean_tags[affprop.cluster_centers_indices_[cluster_id]].lower()
        if exemplar in list(clustered_tags.keys()):
            arr = clustered_tags[exemplar]
        else:
            arr = []
        cluster = np.unique(tags[np.nonzero(affprop.labels_==cluster_id)])
        arr.extend(cluster.tolist())
        clustered_tags[exemplar] =  list(set(arr))
        cluster_str = ", ".join(cluster)
    print("No, of labels", len(clustered_tags.keys()))
    return clustered_tags

def strip_non_ascii(string):
    ''' Returns the string without non ASCII characters'''
    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)

if __name__ == "__main__":

    # DATA = pd.read_csv("data/Twitch Plays Pokemon Identifiers.csv", low_memory=False, encoding="ISO-8859-1")
    # TAGS = tokenize_tags(DATA)
    # cleaned_tags = [cleanup(tag) for tag in TAGS]
    #
    # tfidf_vectorizer = TfidfVectorizer()
    # tfidf_matrix = tfidf_vectorizer.fit_transform(cleaned_tags)
    # cs_similarity = np.array([cosine_similarity(tfidf_matrix[i:i + 1], tfidf_matrix).flatten() for i in range(len(cleaned_tags))])
    # clustered_tags = cluster(cs_similarity, TAGS, cleaned_tags)
    #
    # DATA = DATA.set_index('Identifier').T.to_dict('list')
    # make_inverted_index(DATA, clustered_tags)

    #US election Data
    DATA = pd.read_csv("../data/US Election Identifiers.csv", low_memory=False, encoding="utf-8")
    DATA = DATA.set_index('Identifier').T.to_dict('list')
    make_unclustered_inverted_index(DATA)