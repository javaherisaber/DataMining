"""
DataSet = seeds
chosen attribute = Area
Fill missing values by 3 ways below :
- Mean
- Mean within same class
- KNN
"""
import os
import random
import copy
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsRegressor


def path_input_file():
    file_dir = os.path.dirname(__file__)
    return file_dir+"/seeds.csv"


def input_data():
    fields = ["Area", "status"]
    #
    # reading data from csv file
    data = pd.read_csv(path_input_file(), header=0, usecols=fields)
    return data.as_matrix()


def input_data_knn():
    data = pd.read_csv(path_input_file(), header=0)
    return data.as_matrix()


def delete_alfa_percent(alfa, data):
    data_len = len(data)
    sample_count = int(data_len * (alfa/100))
    missing_indexes = random.sample(range(0, data_len-1), sample_count)
    for element in missing_indexes:
        data[element][0] = float(-1)
    return data, missing_indexes


def mean(data):
    sum_values = 0
    for element in data:
        if element[0] != float(-1):
            sum_values += element[0]
    return round(sum_values/(len(data)), 2)


def find_same_class_data(data, label):
    output_data = []
    for element in data:
        if element[0] != float(-1) and element[1] == float(label):
            output_data.append(np.array([element[0], element[1]]))
    return np.array(output_data)


def euclidean_distance(data, new_data, missing_indexes):
    sum_values = 0
    for element in missing_indexes:
        sum_values += (abs((data[element][0] - new_data[element][0])))**2
    return math.sqrt(sum_values)


def plot_illustrate(mean_values, mean_class_values, knn_values, alfa_percent):
    # Create a subplot with 1 row and 3 columns
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
    fig.set_size_inches(5, 5)

    #
    #  The 1st subplot is the mean plot
    ax1.set_xlim([min(alfa_percent) - 1, max(alfa_percent) + 1])  # x axis range
    ax1.set_ylim([min(mean_values) - 1, max(mean_values) + 1])  # y axis range
    ax1.set_title("Filling by Mean")  # figure title
    ax1.set_xlabel("Alfa")  # x axis label
    ax1.set_ylabel("Euclidean distance")  # y axis label
    ax1.plot(alfa_percent, mean_values, color='red')
    ax1.grid()

    #
    # The 2nd subplot is the mean in same class plot
    ax2.set_xlim([min(alfa_percent) - 1, max(alfa_percent) + 1])  # x axis range
    ax2.set_ylim([min(mean_class_values) - 1, max(mean_class_values) + 1])  # y axis range
    ax2.set_title("Filling by Mean in same class")  # figure title
    ax2.set_xlabel("Alfa")  # x axis label
    ax2.set_ylabel("Euclidean distance")  # y axis label
    ax2.plot(alfa_percent, mean_class_values, color='blue')
    ax2.grid()

    #
    # The 3rd subplot is the knn plot
    ax3.set_xlim([min(alfa_percent) - 1, max(alfa_percent) + 1])  # x axis range
    ax3.set_ylim([min(mean_class_values) - 1, max(mean_class_values) + 1])  # y axis range
    ax3.set_title("Filling by KNN")  # figure title
    ax3.set_xlabel("Alfa")  # x axis label
    ax3.set_ylabel("Euclidean distance")  # y axis label
    ax3.plot(alfa_percent, knn_values, color='black')
    ax3.grid()

    plt.suptitle("Filling the missing values by 3 ways below", fontsize=14, fontweight='bold', color='blue')
    plt.show()


def via_knn_regression(data, knn_attributes, missing_att_index):
    neigh = KNeighborsRegressor(n_neighbors=7)  # knn nearest neighbours
    neigh.fit([list(row[knn_attributes]) for row in data if row[missing_att_index] != float(-1)],
              [row[missing_att_index] for row in data if row[missing_att_index] != float(-1)])
    for i in range(0, len(data)):
        if data[i][missing_att_index] == float(-1):
            data[i][missing_att_index] = neigh.predict([data[i][knn_attributes]])[0]
    return data


def fill_missing():
    data = input_data()
    knn_data = input_data_knn()
    mean_eucl = []
    mean_class_eucl = []
    knn_eucl = []
    for alfa in range(5, 85, 5):
        contain_missing_data, missing_indexes = delete_alfa_percent(alfa, copy.copy(data))
        #
        # via mean method
        avg = mean(contain_missing_data)
        for element in missing_indexes:
            contain_missing_data[element][0] = avg
        distance = euclidean_distance(copy.copy(data), new_data=contain_missing_data, missing_indexes=missing_indexes)
        mean_eucl.append(distance)
        #
        # via mean in same class
        avg_by_class = {}
        for element in missing_indexes:
            if data[element][1] not in avg_by_class:
                avg_by_class[data[element][1]] = 0
        for label in avg_by_class:
            temp_data = find_same_class_data(data=contain_missing_data, label=label)
            class_avg = mean(temp_data)
            avg_by_class[label] = round(class_avg, 2)
        for item in missing_indexes:
            contain_missing_data[item][0] = avg_by_class[contain_missing_data[item][1]]
        distance = euclidean_distance(copy.copy(data), new_data=contain_missing_data, missing_indexes=missing_indexes)
        mean_class_eucl.append(distance)
        #
        # via knn regression
        contain_missing_data, missing_indexes = delete_alfa_percent(alfa, copy.copy(knn_data))
        filled_data = via_knn_regression(copy.copy(contain_missing_data), [1, 2, 3, 4, 5, 6], 0)
        distance = euclidean_distance(copy.copy(data), new_data=filled_data, missing_indexes=missing_indexes)
        knn_eucl.append(distance)
    plot_illustrate(mean_values=mean_eucl, mean_class_values=mean_class_eucl, knn_values=knn_eucl
                    , alfa_percent=range(5, 85, 5))

fill_missing()
