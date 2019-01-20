# -*- coding: utf-8 -*-
"""
Created on Sat Oct 20 19:54:26 2018

@author: akash
"""

import re
from collections import Counter
from sklearn.cluster import KMeans

# Reading the dataset
with open('finefoods.txt','r', encoding = 'latin-1') as f:
    data = f.read().split('\n\n')

# Storing reviews in the variable
dataset = [review.split('\n')[-1] for review in data]

print('Reading the reviews completed')

# Reading stop words from the file
stop_words = []
with open('stop_words.txt', 'r') as f:
    words = f.read()
    stop_words = words.split('\n')


# Getting a list of unique words from the review dataset and generating count of the words
_dictW = Counter()
L = set()
W = []

for row in dataset:
    try:
        temp = []
        for i in row.split(' ')[1:]:
            s = "".join(re.findall('[a-zA-Z]+', i)).lower()
            L.add(s)
            temp.append(s)
            # Removing stop words
            if (s not in stop_words):
                W.append(s)
                # Maintaining the count
                _dictW[s] = _dictW.get(s, 0) + 1
            
        row = (' ').join(temp)
    except AttributeError:
        pass
        #print("Error occured for ", i)
    

# Extracting top 500 words and saving them in a text file
mostCommon = _dictW.most_common(500)
with open('top500words.txt', 'w+') as f:
    for w in mostCommon:
        f.write("{} \t {} \n".format(w[0], w[1]))
        
print('Writing top 500 words in the file')        

# Vectorizing the dataset
dataVector = []
for row in dataset:
    temp = []
    for w in mostCommon:
        temp.append(row.split().count(w[0]))
    dataVector.append(temp)
    

print('Running kmeans')

# Running k-means on the vectorized dataset
kmeans = KMeans(n_clusters = 10, max_iter = 50)
kmeans.fit(dataVector)
centroids = kmeans.cluster_centers_


# Creating a list of top 5 words for each centroid
topWords = []
for c in centroids:
    topInCentroid = sorted(range(len(c)), key = lambda i: c[i], reverse = True)[:5]
    for i in topInCentroid:
        topWords.append((mostCommon[i][0], c[i]))
    
print('Writing top 50 words in the file')

# Writing top words in a text file
with open('top50.txt', 'w+') as f:
    for w in topWords:
        f.write("{} \t {} \n".format(w[0], w[1]))