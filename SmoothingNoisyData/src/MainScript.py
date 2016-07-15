"""
DataSet = seeds
chosen attribute = Area
smoothing noisy data via windows mean
"""
import os
import copy
import math
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def path_input_file():
    file_dir = os.path.dirname(__file__)
    return file_dir+"/seeds.csv"


def input_data():
    #
    # reading data from csv file
    data = pd.read_csv(path_input_file(), header=0, usecols=["Area"])
    return data.as_matrix()


def make_alfa_percent_noisy(alfa, data):
    data_len = len(data)
    sample_count = int(data_len * (alfa/100))
    random_indexes = random.sample(range(0, data_len-1), sample_count)
    noisy_items = {x: np.random.normal(data[x]) for x in random_indexes}
    for key, value in noisy_items.items():
        data[key] = value
    return data


def euclidean_distance(data, new_data):
    sum_values = 0
    for element in range(0, len(data)):
        sum_values += (abs((data[element] - new_data[element])))**2
    return math.sqrt(sum_values)


def smooth_noisy_data(data, windows_count):
    _len = len(data)
    item_count = int((_len - windows_count)/(windows_count+1))
    mean_counter = 0
    sum_strip = 0
    for index in range(0, _len):
        if mean_counter == item_count:
            for i in range(index+1, index+item_count+1):
                if i < _len:
                    sum_strip += data[i]
                else:
                    break
            data[index] = (sum_strip / (2*item_count))
            mean_counter = 0
            sum_strip = 0
        else:
            mean_counter += 1
            sum_strip += data[index]
    return data


def plot_illustrate(twenty_win_values, forty_win_values, eighty_win_values, alfa_percent):
    # Create a subplot with 1 row and 3 columns
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
    fig.set_size_inches(5, 5)

    #
    #  The 1st subplot is for 20 windows
    ax1.set_xlim([min(alfa_percent) - 1, max(alfa_percent) + 1])  # x axis range
    ax1.set_ylim([min(twenty_win_values) - 1, max(twenty_win_values) + 1])  # y axis range
    ax1.set_title("20 windows")  # figure title
    ax1.set_xlabel("Alfa")  # x axis label
    ax1.set_ylabel("Euclidean distance")  # y axis label
    ax1.plot(alfa_percent, twenty_win_values, color='red')
    ax1.grid()

    #
    # The 2nd subplot is for 40 windows
    ax2.set_xlim([min(alfa_percent) - 1, max(alfa_percent) + 1])  # x axis range
    ax2.set_ylim([min(forty_win_values) - 1, max(forty_win_values) + 1])  # y axis range
    ax2.set_title("40 windows")  # figure title
    ax2.set_xlabel("Alfa")  # x axis label
    ax2.set_ylabel("Euclidean distance")  # y axis label
    ax2.plot(alfa_percent, forty_win_values, color='blue')
    ax2.grid()

    #
    # The 3rd subplot is for 80 windows
    ax3.set_xlim([min(alfa_percent) - 1, max(alfa_percent) + 1])  # x axis range
    ax3.set_ylim([min(forty_win_values) - 1, max(forty_win_values) + 1])  # y axis range
    ax3.set_title("80 windows")  # figure title
    ax3.set_xlabel("Alfa")  # x axis label
    ax3.set_ylabel("Euclidean distance")  # y axis label
    ax3.plot(alfa_percent, eighty_win_values, color='black')
    ax3.grid()

    plt.suptitle("Smoothing the noisy data via below windows number", fontsize=14, fontweight='bold', color='blue')
    plt.show()


def do_algorithm():
    data = input_data()
    eucl_dists = {20: [], 40: [], 80: []}
    for alfa in range(5, 85, 5):
        for key, value in eucl_dists.items():
            noisy = make_alfa_percent_noisy(alfa, copy.copy(data))
            flatten_noisy = [x[0] for x in noisy]
            flatten_noisy = sorted(flatten_noisy)
            smoothed = smooth_noisy_data(copy.copy(flatten_noisy), key)
            distance = euclidean_distance(data=copy.copy(flatten_noisy), new_data=copy.copy(smoothed))
            eucl_dists[key].append(distance)
    plot_illustrate(twenty_win_values=eucl_dists[20], forty_win_values=eucl_dists[40], eighty_win_values=eucl_dists[80]
                    , alfa_percent=range(5, 85, 5))


do_algorithm()
