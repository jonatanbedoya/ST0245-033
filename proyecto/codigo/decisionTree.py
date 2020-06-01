"""
@GoogleDevelopers
"""
from __future__ import print_function
"""Modificar
he = []
header = []
training_data = []
train = []
k = 0
h = 0
with open('algo.csv', 'r') as archivo:
    lineas = archivo.read().splitlines()
    he = lineas.pop(0)
    j = len(he)
    for i in range(1,j):
        if (he[i] == ','):
            header.append(he[k:i])
            k=i+1
            h+=1
    if(h==len(header)):
        header.append(he[k:j])
    for l in lineas:
        lin = l.split()
        training_data.append(lin)
    print(header)
    m = len(training_data)
    for i in range(0,m):
        train.append(training_data[i])
    print(train)
"""
training_data = [
    ['Green', 3, 'Apple'],
    ['Yellow', 3, 'Apple'],
    ['Red', 1, 'Grape'],
    ['Red', 1, 'Grape'],
    ['Yellow', 3, 'Lemon'],
]

# Column labels.
# These are used only to print the tree.
header = ["color", "diameter", "label"]

def unique_vals(rows, col):
    """Find the unique values for a column in a dataset."""
    return set([row[col] for row in rows])

def class_counts(rows):
    """cuenta el número de cada tipo de ejemplo en un "dataset"."""
    counts = {} #un diccionario de etiqueta
    for row in rows:
        #En nuestro formato dataset, la etiqueta es siempre la última columna
        label = row[-1]
        if label not in counts:
            counts[label] = 0
        counts[label] += 1
    return counts

def is_numeric(value):
    """Evalua si el valor es un número."""
    return isinstance(value, int) or isinstance(value, float)

class Question:
    """Una pregunta es usada para dividir(Particionar) un dataset.
    """
    def __init__(self, column, value):
        self.column = column
        self.value = value

    def match(self, example):
        # Compare the feature value in an example to the
        # feature value in this question.
        val = example[self.column]
        if is_numeric(val):
            return val >= self.value
        else:
            return val == self.value

    def __repr__(self):
        # This is just a helper method to print
        # the question in a readable format.
        condition = "=="
        if is_numeric(self.value):
            condition = ">="
        return "Is %s %s %s?" % (header[self.column], condition, str(self.value))
    
def partition(rows, question):
    """Partición o división del dataset.
    Para cada fila en el dataset, se comprueba si coincide con la
    pregunta, si es correcto se añade a 'true rows' de lo contrario
    se añade a 'false true'.
    """
    true_rows, false_rows = [], []
    for row in rows:
        if question.match(row):
            true_rows.append(row)
        else:
            false_rows.append(row)
    return true_rows, false_rows

def gini(rows):
    """Calcula la impureza de Gini fara una lista de filas.
    Hay muchas maneras para hacer esto, Se utilizará está:
    Ver:
    """
    counts = class_counts(rows)
    impurity = 1
    for lbl in counts:
        prob_of_lbl = counts[lbl]/ float(len(row))
        impurity -= prob_of_lbl**2
    return impurity

def info_gain(left, right, current_uncertainty):
    """Calcula la ganancia de información.
    Se trabaja con la incertidumbre del nodo inicial, menos
    la impureza ponderada de los dos nodos secundarios.
    """
    p = float(len(left)) / (len(left) + len(right))
    return current_uncertainty - p * gini(left) - (1 - p) * gini(right)

def find_best_split(rows):
    """Busca la mejor pregunta para hacer la iteración sobre cada
    caracteristica/valor y calcula la ganancia de información.
    """
    best_gain = 0  # keep track of the best information gain
    best_question = None  # keep train of the feature / value that produced it
    current_uncertainty = gini(rows)
    n_features = len(rows[0]) - 1  # number of columns

    for col in range(n_features):  # for each feature

        values = set([row[col] for row in rows])  # unique values in the column

        for val in values:  # for each value

            question = Question(col, val)

            # try splitting the dataset
            true_rows, false_rows = partition(rows, question)

            # Skip this split if it doesn't divide the
            # dataset.
            if len(true_rows) == 0 or len(false_rows) == 0:
                continue

            # Calculate the information gain from this split
            gain = info_gain(true_rows, false_rows, current_uncertainty)

            # You actually can use '>' instead of '>=' here
            # but I wanted the tree to look a certain way for our
            # toy dataset.
            if gain >= best_gain:
                best_gain, best_question = gain, question
                
    return best_gain, best_question

class Leaf:
    """
    A leaf node classifies data.
    It holds a dictionary of class -> number of times it appears in the rows 
    from the training data that reached the leaf.
    """
    def _init_(self, rows):
        self.predictions = class_counts(rows)
        
class Decision_Node:
    """
    A decision node asks a question.
    It holds a reference to a question and to the two child nodes.
    """
    def _init_(self, question,true_branch,false_branch):
        self.question = question
        self.true_branch = true_branch
        self.false_branch = false_branch

def build_tree(rows):
    """Builds the tree.
    Rules of recursion: 1) Believe that it works. 2) Start by checking
    for the base case (no further information gain). 3) Prepare for
    giant stack traces.
    """

    # Try partitioing the dataset on each of the unique attribute,
    # calculate the information gain,
    # and return the question that produces the highest gain.
    gain, question = find_best_split(rows)

    # Base case: no further info gain
    # Since we can ask no further questions,
    # we'll return a leaf.
    if gain == 0:
        return Leaf(rows)

    # If we reach here, we have found a useful feature / value
    # to partition on.
    true_rows, false_rows = partition(rows, question)

    # Recursively build the true branch.
    true_branch = build_tree(true_rows)

    # Recursively build the false branch.
    false_branch = build_tree(false_rows)

    # Return a Question node.
    # This records the best feature / value to ask at this point,
    # as well as the branches to follow
    # dependingo on the answer.
    return Decision_Node(question, true_branch, false_branch)

def print_tree(node, spacing=""):
    """World's most elegant tree printing function."""

    # Base case: we've reached a leaf
    if isinstance(node, Leaf):
        print (spacing + "Predict", node.predictions)
        return

    # Print the question at this node
    print (spacing + str(node.question))

    # Call this function recursively on the true branch
    print (spacing + '--> True:')
    print_tree(node.true_branch, spacing + "  ")

    # Call this function recursively on the false branch
    print (spacing + '--> False:')
    print_tree(node.false_branch, spacing + "  ")
    
def classify(row, node):
    """See the 'rules of recursion' above."""

    # Base case: we've reached a leaf
    if isinstance(node, Leaf):
        return node.predictions

    # Decide whether to follow the true-branch or the false-branch.
    # Compare the feature / value stored in the node,
    # to the example we're considering.
    if node.question.match(row):
        return classify(row, node.true_branch)
    else:
        return classify(row, node.false_branch)

def print_leaf(counts):
    """ A nicer way to print the predictions at a leaf. """
    total = sum(counts.values()) * 1.0
    probs = {}
    for lbl in counts.keys():
        probs[lbl] = str(int(counts[lbl] / total * 100)) + '%'
    return probs

if __name__ == '__main__':

    my_tree = build_tree(training_data)

    print_tree(my_tree)
