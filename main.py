import distance
from collections import Counter

def load_file(filename, sep):
    """
    Returns a tuple with all the items and their attributes (as a tuple).

    This function takes as input:
        1. a filename (path)
        2. separator character(s)

    It loads the specified file and outputs a tuple containing tuples for each line in the file. These latter tuple consists of the separated attributes.
    """

    list_of_tuples = []

    with open(filename) as infile:
        for line in infile:
            tuple_of_attributes = tuple(line.strip().split(sep))
            list_of_tuples.append(tuple_of_attributes)

    # some testing

    # checks if there are items in the file
    try:
        assert len(list_of_tuples) >= 1
    except AssertionError:
        raise IOError("Empty file!", "There are no items found in the specified file!")

    # checks if all the tuples are of the same length, i.e. if every line
    # contains the same amount of attributes.
    length_of_longest_tuple = len(max(list_of_tuples, key=len))
    length_of_shortest_tuple = len(min(list_of_tuples, key=len))

    try:
        assert length_of_longest_tuple == length_of_shortest_tuple
    except AssertionError:
        raise IOError("Inconsistent file!", "Not every item has the same length! Make sure every line in the file has the same amount of attributes. Are there empty lines?")

    return tuple(list_of_tuples)


def print_stats(intuple, index=-1):
    """
    Prints statistics for a dataset.

    Prints the following:
        Number of items
        Number of features
        Unique class labels (with proportions)

    Optional argument: index=n, which indicates at what order the class label is located inside the item in the datafile.
    """
    list_of_class_labels = []

    n_items = len(intuple)
    n_features = len(intuple[0])

    # class labels
    for item in intuple:
        list_of_class_labels.append(item[index])

    unique_class_labels = sorted(set(list_of_class_labels))
    total = len(list_of_class_labels)

    print("Some statistics:")
    print("\t", "Number of items:", n_items)
    print("\t", "Number of features:", n_features)
    print("\t", "Unique class labels (relative proportion):")
    for n, label in enumerate(unique_class_labels, 1):
        count_labels = list_of_class_labels.count(label)
        print("\t\t", n, "\t", label, "(%d/%d (%d%%))" % (count_labels,total,round(count_labels/total*100)))

    # some testing
    # Checks if there is only a single class label
    # and breaks the function if so.
    try:
        assert len(unique_class_labels) > 1
    except AssertionError:
        raise ValueError("Only one class label found!", "Make sure there is more than one class label in de data file, otherwise using this tool would not make any sense!")

def predict(train_tuple, test_tuple, n=False):
    """
    Predicts what the class label should are for items in a test dataset.

    This function takes every item in a test dataset and compares it to items from a train dataset. The closest match is returned.

    The function returns a tuple with only the predicted class labels. The order corresponds to the order in the datafile.
    """

    data = distance_calculating(train_tuple, test_tuple)
    predicted_class_labels = []

    for n_test, datalist in data.items():
        list_of_class_labels = []

        # correct for amount of nearest neighbours to use (n)
        if n is False:
            for n_train in datalist[1]:
                class_label = get_class_label(n_train, train_tuple)
                list_of_class_labels.append(class_label)
        else:
            for n_train in datalist[1][:n]:
                class_label = get_class_label(n_train, train_tuple)
                list_of_class_labels.append(class_label)

        final_class_label = Counter(list_of_class_labels).most_common()[0][0]
        predicted_class_labels.append(final_class_label)

    return tuple(predicted_class_labels)

def evaluate(predicted_class_labels, test_tuple):
    """
    """
    data = dict()
    list_of_class_labels = []
    real_class_labels = tuple([x[-1] for x in test_tuple])
    total_predictions = len(predicted_class_labels)

    for predicted_label, real_label in zip(predicted_class_labels, real_class_labels):
        data.setdefault(real_label, {"correct":0, "wrong":0})

        if predicted_label == real_label:
            data[real_label]["correct"] += 1
        else:
            data[real_label]["wrong"] += 1


    print("Evaluation statistics:")
    correct_predictions = sum(map(Counter, data.values()), Counter())["correct"]
    total_predictions = sum(x for counter in data.values() for x in counter.values())

    avg_predictions = correct_predictions/total_predictions
    print("\t","Average number of correct predictions:", round(avg_predictions, 2), "(%d/%d" % (correct_predictions, total_predictions))

    print("\t\t", "Class label (correct/total (%%))")
    for class_label, values in data.items():
        total_class_predictions = sum(values.values())
        correct_class_predictions = values["correct"]
        correct_percentage = correct_class_predictions/total_class_predictions*100
        print("\t\t",class_label,"(%d/%d (%d%%))" % (correct_class_predictions,total_class_predictions, correct_percentage))

        list_of_class_labels.append((class_label, correct_percentage))


    # list_of_class_labels = sorted(list_of_class_labels, function=min)
    print("Label hardest to learn:", "%s (%d%%)" % min(list_of_class_labels, key=lambda x: x[1]))


    print()




def distance_calculating(train_tuple, test_tuple):
    """
    Calculate the Levenshtein distance between two items and return a dictionary with the index of closest matches as a list as its value and the n_test item as the key.

    This function returns a dictionary of the form:
        n_test: [distance, [n_train...n_train]]
    """
    data = dict()

    for n_test, test_item in enumerate(test_tuple):

        # set default value for the data dict.
        data.setdefault(n_test,[-1,[]])

        # remove the class label
        test_item = test_item[:-1]

        for n_train, train_item in enumerate(train_tuple):
            # remove the class label
            train_item = train_item[:-1]

            min_distance = distance.levenshtein(test_item, train_item)

            # if there is an exact match
            if min_distance == 0:
                data[n_test] = [min_distance, [n_train]]
                break
            elif min_distance == data[n_test][0]:
                data[n_test][1].append(n_train)
            elif min_distance < data[n_test][0] or data[n_test][0] == -1:
                data[n_test] = [min_distance, [n_train]]

    return data


def get_class_label(n_train, data_tuple):
    """
    Returns the class label given an index number from a datafile.

    Helper function to retrieve the class label from an index number and a datatuple.
    """

    data_tuple = enumerate(data_tuple)
    class_label = list(filter(lambda x: x[0] == n_train, data_tuple))[0][1][-1]

    return class_label








train_tuple = load_file("dimin.train", ",")
test_tuple = load_file("dimin.test", ",")
# train_tuple = load_file("train.train", ",")
# test_tuple = load_file("test.test", ",")
print_stats(test_tuple)

predicted_class_labels = predict(train_tuple, test_tuple, 5)
evaluate(predicted_class_labels, test_tuple)


