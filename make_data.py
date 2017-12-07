# coding: utf-8

# # Tag Central
# Here we will manipulate data from the data folder(US Election tags and Twitch plays pokemon tags).
# 

# In[16]:


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import AffinityPropagation
import numpy as np
import pandas as pd
import json

# In[17]:


#twitch_data = pd.read_csv("data/Twitch Plays Pokemon Identifiers.csv", low_memory=False, encoding="ISO-8859-1")
election_data = pd.read_csv("../data/US Election Identifiers.csv", low_memory=False, encoding="ISO-8859-1")

DATA = election_data


# Twitch data and election data are loaded using panda.
# Each dataset has two columns **Identifier** and **Subject**
# The __tokenize_tags__ function below takes each row of tags, splits them up into arrays and puts them all together into a tags array.

# In[18]:


def tokenize_tags(data):
    tags = data['Subject']
    all_tags = []
    for tag_string in tags:
        tag_string = str(tag_string)
        all_tags.extend(tag_string.split(","))
    all_tags = np.asarray(all_tags)
    return all_tags


TAGS = tokenize_tags(DATA)
print(list(TAGS[0:10]))
print("Total number of tags", len(TAGS))

# ## Inverted Index
# Here we are preparing an inverted index of our tags and identifiers

# First, we convert the dataframe to a dictionary. The key is the identifier and the  the value is a string of comma separated tags.
# The **make_inverted_index** function that converts this dictionary into a dictionary where the key is a tag and the value is a list of documents where is occurs. The documents are labelled by their position. e.g. 0,1,2,3. This is much easier to work with than their longer values e.g. live_user_twitchplayspokemon_1407024801
# 
# We create the popularity index and inverted index at the same time.

# In[19]:


# Run this just once.this converts the csv data into a dictionary
DATA = DATA.set_index('Identifier').T.to_dict('list')


# In[20]:


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
    # word = ascii(word)
    # splits the word by whitespace, per https://www.tutorialspoint.com/python/string_split.htm
    word = word.split()
    # removes duplicates
    word = "".join(list(set(word)))
    # sorts array in place 
    return word


# In[21]:


def make_inverted_index(data):
    inverted_index = {}
    popularity_index = {}
    for i, doc in enumerate(data):
        doc_tags = str(data[doc][0]).split(",")
        for tag in doc_tags:
            if inverted_index.get(tag, None):
                inverted_index[tag].append(i)
                popularity_index[tag] += 1
            else:
                inverted_index[tag] = [i]
                popularity_index[tag] = 1
    return inverted_index, popularity_index


# In[22]:


def make_inverted_index_clean(data):
    inverted_index = {}
    popularity_index = {}
    for i, doc in enumerate(data):
        doc_tags = str(data[doc][0]).split(",")
        for tag in doc_tags:
            tag = cleanup(tag)  # CLEANUP OCCURS HERE
            if inverted_index.get(tag, None):
                inverted_index[tag].append(i)
                popularity_index[tag] += 1
            else:
                inverted_index[tag] = [i]
                popularity_index[tag] = 1
    return inverted_index, popularity_index


# In[23]:


# Generate clean and dirty indices
inverted_index, popularity_index = make_inverted_index(DATA)
inverted_index_clean, popularity_index_clean = make_inverted_index_clean(DATA)
with open('inverted_index_elections.py', 'w') as file:
    file.write("INVERTED_INDEX = ")
    file.write(json.dumps(inverted_index))
    file.write("\n")
    file.write("INVERTED_INDEX_CLEAN = ")
    file.write(json.dumps(inverted_index_clean))
    file.write("\n")
    file.write("POPULARITY_INDEX = ")
    file.write(json.dumps(popularity_index))

# In[24]:


def recommendOriginal(invIndex, invIndexClean, query):
    """Take an input of a partial string (e.g. 'Tru').
    Clean input.
    Access inverted index to find matching (cleaned) tags.
    Figure out which matching cleaned tags are most popuar.
    Recommend uncleaned version of most popular tag."""
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

    # What is original version of topRec with the highest popularity?
    # Data is dictionary of element:tags
    # Look in the dirty index
    # Find the multiple tags that clean to cleanquery
    # Recommend the most popular one
    dirtyMatches = []
    topRecDirty = ""
    highestDirty = 0

    for tag in invIndex:
        if topRecClean == cleanup(tag):
            dirtyMatches.append([tag, len(invIndex[tag])])

    # print("Dirty matches:", dirtyMatches)
    for (tag, popularity) in dirtyMatches:
        if popularity > highestDirty:
            highestDirty = popularity
            dirtyRec = tag
    return dirtyRec

