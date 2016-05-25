import os
import csv
import sys


def path_input_file():
    file_dir = os.path.dirname(__file__)
    return file_dir+"/car.csv"


def path_output_file():
    file_dir = os.path.dirname(__file__)
    return file_dir + "/output.txt"


def read_input_file():
    data = []
    try:
        with open(path_input_file(), 'rt', encoding='utf8') as f:
            reader = csv.reader(f, delimiter=',', quotechar='\n')
            for row in reader:
                data.append(row)
    except IOError:
        print("Wrong input path")
        sys.exit(0)
    return data


def write_output_file(input_file):
    output_file = path_output_file()
    if output_file is None:
        print("Wrong output path")
        sys.exit(0)
    file = open(output_file, 'wt', encoding='utf-8')
    for item in input_file.keys():
        file.write('P(' + item + ')= ' + repr(input_file[item]))
        file.write('\n')
    file.close()
    return


def naive_bayes_method(input_data, label_identifier):
    header_column = input_data[0]  # retrieve header column of input data
    input_data.remove(input_data[0])
    try:
        label_idx = header_column.index(label_identifier)  # retrieve index of label column
    except ValueError:
        print('Label is not specified correctly')
        sys.exit(0)
    class_dict = {}  # a data structure for saving output data
    #
    # first traversing data for count each class in label
    #
    for row in input_data:
        class_title = row[label_idx]  # title of the class column
        if class_title in class_dict.keys():
            class_dict[class_title]['cnt'] += 1
        else:
            class_dict[class_title] = {}
            class_dict[class_title]['cnt'] = 1
    attribute_list = list(header_column)  # attribute list of our data
    attribute_list.remove(label_identifier)
    for key in class_dict.keys():
        class_dict[key]['attributeList'] = {}
        for attribute in attribute_list:
            class_dict[key]['attributeList'][attribute] = {}
    #
    # second traversing data for count attributes of each class
    #
    for row in input_data:
        cell_label = row[label_idx]
        i = 0
        for att_value in row:
            att_title = header_column[i]
            if att_title in attribute_list:
                if att_value in class_dict[cell_label]['attributeList'][att_title].keys():
                    class_dict[cell_label]['attributeList'][att_title][att_value] += 1
                else:
                    class_dict[cell_label]['attributeList'][att_title][att_value] = 1
            i += 1
    #
    # determining probability of each class and its attributes
    #
    p = {}
    cnt_rows = len(input_data)
    for classifier in class_dict.keys():
        p['class=' + classifier] = (float(class_dict[classifier]['cnt']) / float(cnt_rows))
        for att_title in class_dict[classifier]['attributeList'].keys():
            for att_option in class_dict[classifier]['attributeList'][att_title].keys():
                p[att_title + '=' + att_option + ' | ' + 'class:' + classifier]\
                    = float(class_dict[classifier]['attributeList'][att_title][att_option]) / float(
                    class_dict[classifier]['cnt'])
    return p

dataFile = read_input_file()
probabilities = naive_bayes_method(dataFile, label_identifier='class')  # label column identifier
write_output_file(probabilities)
