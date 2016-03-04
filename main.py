import argparse
from functions import *

# ARGPARSE
parser = argparse.ArgumentParser(description='Diminutive predictor and evaluator')
parser.add_argument('-f', metavar='test_file', nargs=1, required=True,
                   help='path to a test file with data')
parser.add_argument('-t', metavar='train_file', nargs=1, required=True,
                   help='path to a train file with data')
parser.add_argument('-sep', metavar='sep', nargs='?', default=",",
                   help='specifies the seperator the data file uses for its items. Default is a comma.')
parser.add_argument('-n', metavar='neighbours', nargs='?', default=1,
                   help='specifies how many neighbours should be used in calculating a best match')

args = parser.parse_args()

test_file = args.f[0]
train_file = args.t[0]

sep = args.sep
neighbours = args.n

train_tuple = load_file(train_file, sep)
test_tuple = load_file(test_file, sep)




# STATISTICS
print()
print("Printing statistics for test file %s:" % test_file)
print_stats(test_tuple)

# PREDICTING AND EVALUATING
predicted_class_labels = predict(train_tuple, test_tuple, neighbours)
evaluate(predicted_class_labels, test_tuple)


