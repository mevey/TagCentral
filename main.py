from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

from inverted_index_elections import INVERTED_INDEX, POPULARITY_INDEX, INVERTED_INDEX_CLEAN

def get_similar_tags(tag, inverted_index, inverted_index_clean, numRec):
    tag = cleanup(tag)
    array_of_docs = []
    array_of_tags = []
    first_loop = True
    for key in inverted_index_clean:
        row = ",".join([str(x) for x in inverted_index_clean[key]])
        array_of_docs.append(row)
        array_of_tags.append(key)
    array_of_docs = np.array(array_of_docs)
    if tag not in array_of_tags: return []
    t = array_of_tags.index(tag)

    tfidf = TfidfVectorizer().fit_transform(array_of_docs)
    cosine_similarities = cosine_similarity(tfidf[t:t + 1], tfidf).flatten()
    most_similar_tags = cosine_similarities.argsort()[:-(numRec + 1):-1]
    print("most_similar_tags", most_similar_tags)
    for t in most_similar_tags:
        print(array_of_tags[t], array_of_docs[t:t + 1])
    similar_tags = [array_of_tags[i] for i in most_similar_tags]
    similar_Original_tags = []
    for tag in similar_tags:
        similar_Original_tags.append(recommendOriginal(inverted_index, tag))
    return similar_Original_tags[1:]


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
    #word = ascii(word)
    # splits the word by whitespace, per https://www.tutorialspoint.com/python/string_split.htm
    word = word.split()
    # removes duplicates
    word = "".join(list(set(word)))
    # sorts array in place
    return word


def recommendOriginal(invIndex, topRecClean):
    """Take an input of a partial string (e.g. 'Tru').
    Clean input.
    Access inverted index to find matching (cleaned) tags.
    Figure out which matching cleaned tags are most popuar.
    Recommend uncleaned version of most popular tag."""
    """
    cleanQuery = cleanup(query)
    matchList = []
    # Find all clean tags that match the clean query
    for tag in invIndexClean:
        if cleanQuery in tag:
            matchList.append([tag, len(invIndexClean[tag])])
    # print("matchList:", matchList)
    # find most popular tag in matchList
    highest = 0
    topRecClean = ""
    for (tag, popularity) in matchList:
        # print("tag:", tag, "popularity:", popularity)
        if popularity > highest:
            highest = popularity
            topRecClean = tag
    # print(topRecClean)
    # print(highest)
    """
    # What is original version of topRec with the highest popularity?
    # Data is dictionary of element:tags
    # Look in the dirty index
    # Find the multiple tags that clean to cleanquery
    # Recommend the most popular one
    dirtyMatches = []
    highestDirty = 0

    for tag in invIndex:
        if topRecClean == cleanup(tag):
            dirtyMatches.append([tag, len(invIndex[tag])])

    dirtyRec = None
    # print("Dirty matches:", dirtyMatches)
    for (tag, popularity) in dirtyMatches:
        if popularity > highestDirty:
            highestDirty = popularity
            dirtyRec = tag
    return dirtyRec

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="6000", debug=True)
