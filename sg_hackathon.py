# -*- coding: utf-8 -*-
"""SG hackathon.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LzHMUH7TLoM13clO4plw-m6ywxACGtzs
"""

import random
import pandas as pd
import networkx as nx
import numpy as np

dataset_size = 5000  # Set your desired dataset size

# Define the bias factors for source and destination
source_bias_factor = 0.2
destination_bias_factor = 0.2
date = [random.randint(0, 729) for _ in range(dataset_size)]
data_person = ['user', 'attacker']
person = [random.choice(data_person) for _ in range(dataset_size)]

# Introduce bias in the 'source' attribute
data_source = list(range(10))  # Possible values for source
biased_data_source = [random.choices(data_source, weights=[source_bias_factor if src in [2,4,3,5,7,9,0,1] else 1 for src in data_source])[0] for _ in range(dataset_size)]

# Introduce bias in the 'destination' attribute
data_destination = list(range(10))  # Possible values for destination
biased_data_destination = [random.choices(data_destination, weights=[destination_bias_factor if dest in [6,8,3,5,7,9,0,1] else 1 for dest in data_destination])[0] for _ in range(dataset_size)]

# Combine attributes into a list of tuples
biased_dataset = list(zip(date, biased_data_source, biased_data_destination, person))
df = pd.DataFrame(biased_dataset)

# Save the biased dataset to a CSV file
df.to_csv('biased_dataset.csv', index=False)

G=nx.MultiDiGraph()
df =pd.read_csv('/content/biased_dataset.csv')

x=df.to_numpy()
edge_set=x[:,1:3]
e1=[]
for x in edge_set:
  e1.append(tuple(x))
#e=tuple(e1)
#print(e1)
G.add_edges_from(e1)

#in_degree=dict(
print("IN Degree: ",G.in_degree())
print("OUT Degree: ",G.out_degree())
#print(in_degree)
#G.betweenness_centrality()

df.columns=['date','source','destination','person']
grouped = df.groupby(['source', 'destination']).size().reset_index(name='Count')
print(grouped)
grouped.to_excel('/content/count.xlsx')

dfm = grouped.to_numpy()
elist=[]
for i in range(len(dfm)):
  elist.append(tuple(dfm[i]))
print(len(elist))
weights_dict = {}
for row in elist:
  first_element, second_element, weight = row
  pair = tuple(sorted([first_element, second_element]))
  weights_dict[pair] = weight
print(weights_dict)

WSG = nx.Graph()

for source, destination in weights_dict.keys():
    WSG.add_edge(source, destination, weight=weights_dict[source, destination])

nx.draw(WSG, with_labels=True)

betweenness_centrality = nx.betweenness_centrality(WSG, weight="weight")

print(betweenness_centrality)

eigenvector_centrality = nx.eigenvector_centrality(WSG)

print(eigenvector_centrality)
print("max: ",max(eigenvector_centrality))

arr=df.to_numpy()
print(arr)

'''
result 101="System  traffic is too high, network infrastructure to be improvised"
result 102="Add more new nodes in network which will act as alternative to the hotspots ports"
result 103="add more new nodes alternative to source host and add dummy nodes for the nodes which faces most transmissions"
result 104="Add more new source nodes to decrease network traffic"
result 105="add more new destination nodes to decrease network traffic and add dummy nodes for the nodes which faces most transmissions"
result 106="add more new destination nodes to decrease network traffic"
result 107="add dummy nodes for the nodes which faces most transmissions"
result 108="does not have network traffic"
result 109="security threats and it needs to be improvised"
'''

src_hs1,src_hs2=6,8
dest_hs1,dest_hs2=2,4
bet_hs=max(betweenness_centrality)
arr1=np.zeros(5000)
for i in range(5000):
  if(arr[i][1]==src_hs1 or arr[i][1]==src_hs2):
    if(arr[i][2]==dest_hs1 or arr[i][2]==dest_hs2):
      if(arr[i][1]==bet_hs or arr[i][2]==bet_hs):
        if(arr[i][3]=='user'):
          arr1[i]=101
        else:
          arr1[i]=109
      else:
        if(arr[i][3]=='user'):
          arr1[i]=102
        else:
          arr1[i]=109
    else:
      if(arr[i][1]==bet_hs or arr[i][2]==bet_hs):
        if(arr[i][3]=='user'):
          arr1[i]=103
        else:
          arr1[i]=109
      else:
        if(arr[i][3]=='user'):
          arr1[i]=104
        else:
          arr1[i]=109
  else:
    if(arr[i][2]==dest_hs1 or arr[i][2]==dest_hs2):
      if(arr[i][1]==bet_hs or arr[i][2]==bet_hs):
        if(arr[i][3]=='user'):
          arr1[i]=105
        else:
          arr1[i]=109
      else:
        if(arr[i][3]=='user'):
          arr1[i]=106
        else:
          arr1[i]=109
    else:
      if(arr[i][1]==bet_hs or arr[i][2]==bet_hs):
        if(arr[i][3]=='user'):
          arr1[i]=107
        else:
          arr1[i]=109
      else:
        if(arr[i][3]=='user'):
          arr1[i]=108
        else:
          arr1[i]=109

arr1.reshape(-1,1)
print(arr1)

df['resolution']=arr1

print(df)

cols = arr[:, 1:4]
x = np.array(cols)
for i in range(5000):
  if(x[i][2]=='user'):
    x[i][2]=0
  else:
    x[i][2]=1

y=df['resolution'].values

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test= train_test_split(x, y, test_size= 0.2, random_state=0)
from sklearn.tree import DecisionTreeClassifier

#DECISION TREE CLASSIFIER

classifier= DecisionTreeClassifier(criterion='entropy', random_state=0)
classifier.fit(x_train, y_train)

y_pred= classifier.predict(x_test)
print(y_pred)

from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
cm= confusion_matrix(y_test, y_pred)
print(cm)
accuracy = accuracy_score(y_test, y_pred)
print("\nAccuracy: ", accuracy)

from matplotlib import pyplot as plt
from sklearn import datasets
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
clf = DecisionTreeClassifier(random_state=1234)
model = clf.fit(x_train, y_train)

text_representation = tree.export_text(clf)
print(text_representation)

with open("DT Text Representation.doc", "w") as fout:
    fout.write(text_representation)

#RANDOM FOREST CLASSIFIER

from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(x_train, y_train)

# Make predictions
predictions = model.predict(x_test)

# Evaluate the model
accuracy = accuracy_score(y_test, predictions)
print("Accuracy:", accuracy)