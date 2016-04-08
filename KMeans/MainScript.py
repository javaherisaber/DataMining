"""
Internal Evaluation method :
- Silhouette
External Evaluation method :
- Purity
"""
from __future__ import print_function
import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
print(__doc__)


def path_input_file():
    file_dir = os.path.dirname(__file__)
    return file_dir+"/seeds.csv"


def purity_measure(input_data, labels, clusters, k_value):
    scores = {}
    for index in range(0, k_value):
        scores[index] = {}
        for j in range(0, len(input_data)):
            if clusters[j] == index:
                if labels[j] in scores[index].keys():
                    scores[index][labels[j]] += 1
                else:
                    scores[index][labels[j]] = 1
    sum_values = 0
    for index in range(0, k_value):
        temp = 0
        for label in scores[index].keys():
            if scores[index][label] > temp:
                temp = scores[index][label]
        sum_values += temp
    return sum_values / len(input_data)


def silhouette_measure(clusterer, input_data):
    cluster_labels = clusterer.fit_predict(input_data)
    silhouette_avg = silhouette_score(input_data, cluster_labels)
    return silhouette_avg


def plot_illustrate(silhouette_values, purity_values, n_clusters):
    # Create a subplot with 1 row and 2 columns
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.set_size_inches(20, 7)

    #
    #  The 1st subplot is the silhouette plot
    ax1.set_xlim([min(n_clusters) - 1, max(n_clusters) + 1])  # x axis range
    ax1.set_ylim([min(silhouette_values) - 1, max(silhouette_values) + 1])  # y axis range
    ax1.set_title("The silhouette graph")  # figure title
    ax1.set_xlabel("K value")  # x axis label
    ax1.set_ylabel("silhouette score")  # y axis label
    ax1.plot(n_clusters, silhouette_values, color='brown')
    ax1.grid()

    #
    # The 2nd subplot is the Purity plot
    ax2.set_xlim([min(n_clusters) - 1, max(n_clusters) + 1])  # x axis range
    ax2.set_ylim([min(purity_values) - 1, max(purity_values) + 1])  # y axis range
    ax2.set_title("The Purity graph")  # figure title
    ax2.set_xlabel("K value")  # x axis label
    ax2.set_ylabel("Purity score")  # y axis label
    ax2.plot(n_clusters, purity_values, color='black')
    ax2.grid()

    plt.suptitle("Silhouette and Purity evaluation for KMeans", fontsize=14, fontweight='bold', color='blue')
    plt.show()


def reading_data(label_stamp, label_index, attribute_range):
    #
    # reading data from csv file
    d = pd.read_csv(path_input_file(), header=0)
    #
    # separate label column from input data
    labels = d.drop(d.columns[attribute_range], axis=1, inplace=False)
    # remove label column
    d.drop(d.columns[label_index], axis=1, inplace=True)
    # data.drop(data.columns[1], axis=1, inplace=True)
    return d.as_matrix(), labels[label_stamp]


data, label = reading_data(label_index=[7], label_stamp="status", attribute_range=range(0, 6))
c_clusters_ = range(2, 30)
silhouette = []
purity = []
for k in c_clusters_:
    km = KMeans(n_clusters=k).fit(data)
    silhouette.append(silhouette_measure(clusterer=km, input_data=data))
    purity.append(purity_measure(data, label, km.labels_, k))

plot_illustrate(silhouette, purity, c_clusters_)
