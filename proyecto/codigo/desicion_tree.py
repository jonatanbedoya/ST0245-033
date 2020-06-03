from __future__ import print_function
import time
#@GoogleDevelopers & GrupoDeTomasBedoya
import pandas as pd
# Este método sirve para cargar los datos de entrenamiento y prueba para el árbol de decisión
# además permite obtener el header del csv para utilizarlas en las preguntas
def carga_datos(ruta_entrenamiento,ruta_prueba):
    datos_entrenamiento = []
    datos_prueba = []
    Filas = []

    #Cargar el archivo de datos
    archivo_entrenamiento = open(ruta_entrenamiento,encoding='utf-8')
    archivo_prueba = open(ruta_prueba,encoding='utf-8')

    #Crear una lista de listas de estudiantes
    for linea in archivo_entrenamiento:
        linea = linea[:-1] #Se elimina el salto de línea en el csv
        Filas = linea.split(";")
        datos_entrenamiento.append(Filas)

    #Retirar las cabeceras del data_array, estas se utilizan para imprimir el árbol  
    cabeceras = datos_entrenamiento[0] 
    datos_entrenamiento.pop(0) #Se eliminan las cabeceras del data set

    Filas = []

    for linea in archivo_prueba:
        linea = linea[:-1] #Se quita salto de línea
        estudiante = linea.split(";")
        datos_prueba.append(estudiante)

    datos_prueba.pop(0) #Se eliminan las cabeceras del data set


    #Eliminar columnas
    a = ['estu_consecutivo.1',
    'periodo',
    'estu_inst_cod_departamento',
    'estu_tipodocumento.1',
    'estu_nacionalidad.1',
    'estu_fechanacimiento.1',
    'estu_estudiante.1',
    'estu_pais_reside.1',
    'estu_cod_reside_depto.1',
    'estu_cod_reside_mcpio.1',
    'estu_trabajaactualmente',
    'cole_codigo_icfes',
    'cole_cod_dane_establecimiento',
    'cole_cod_dane_sede',
    'cole_cod_mcpio_ubicacion',
    'cole_cod_depto_ubicacion']

    datos_entrenamiento_df = pd.DataFrame.from_records(datos_entrenamiento)
    datos_prueba_df = pd.DataFrame.from_records(datos_prueba)

    for i in range(len(a)):
        aux = cabeceras.index(a[i])
        del datos_entrenamiento_df[aux]
        del datos_prueba_df[aux]

    datos_entrenamiento = datos_entrenamiento_df.values.tolist()
    datos_prueba = datos_prueba_df.values.tolist()
    
    return datos_entrenamiento,datos_prueba,cabeceras
# Cargar los datos de entrenamiento y prueba
training_data, data_array_test, header = carga_datos("Datos/train.csv",
                                                     "Datos/test.csv")


def unique_vals(rows, col):
    """Find the unique values for a column in a dataset."""
    return set([row[col] for row in rows])



def class_counts(rows):
    """Counts the number of each type of example in a dataset."""
    counts = {}  # a dictionary of label -> count.
    for row in rows:
        # in our dataset format, the label is always the last column
        label = row[-1]
        if label not in counts:
            counts[label] = 0
        counts[label] += 1
    return counts


def is_numeric(value):
    """Test if a value is numeric."""
    return isinstance(value, int) or isinstance(value, float)

class Question:
    
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
        return "Is %s %s %s?" % (
            header[self.column], condition, str(self.value))

def partition(rows, question):
    """Partitions a dataset.
    For each row in the dataset, check if it matches the question. If
    so, add it to 'true rows', otherwise, add it to 'false rows'.
    """
    true_rows, false_rows = [], []
    for row in rows:
        if question.match(row):
            true_rows.append(row)
        else:
            false_rows.append(row)
    return true_rows, false_rows

def gini(rows):
    """Calculate the Gini Impurity for a list of rows.
    There are a few different ways to do this, I thought this one was
    the most concise. See:
    https://en.wikipedia.org/wiki/Decision_tree_learning#Gini_impurity
    """
    counts = class_counts(rows)
    impurity = 1
    for lbl in counts:
        prob_of_lbl = counts[lbl] / float(len(rows))
        impurity -= prob_of_lbl**2
    return impurity

def info_gain(left, right, current_uncertainty):
    """Information Gain.
    The uncertainty of the starting node, minus the weighted impurity of
    two child nodes.
    """
    p = float(len(left)) / (len(left) + len(right))
    return current_uncertainty - p * gini(left) - (1 - p) * gini(right)

def find_best_split(rows):
    """Find the best question to ask by iterating over every feature / value
    and calculating the information gain."""
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
    """A Leaf node classifies data.
    This holds a dictionary of class (e.g., "Apple") -> number of times
    it appears in the rows from the training data that reach this leaf.
    """

    def __init__(self, rows):
        self.predictions = class_counts(rows)


class Decision_Node:
    """A Decision Node asks a question.
    This holds a reference to the question, and to the two child nodes.
    """

    def __init__(self,
                 question,
                 true_branch,
                 false_branch):
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
    
def Exactitud(data_array_test, arbol):
    valores_reales = []
    valores_predecidos = []
    
    
    for row in data_array_test:
        valores_reales.append(row[-1])
        valores_predecidos.append([*classify(row, arbol).keys()])

    total = 0

    for i in range(len(valores_reales)):
        if int(valores_reales[i]) == int(valores_predecidos[i][0]):
            total += 1
    
    return (print('Exactitud: ' +str((total/len(valores_reales))*100) +'%'))
    
def print_leaf(counts):
    """A nicer way to print the predictions at a leaf."""
    total = sum(counts.values()) * 1.0
    probs = {}
    for lbl in counts.keys():
        probs[lbl] = str(int(counts[lbl] / total * 100)) + "%"
    return probs

if __name__ == '__main__':
  tiempopromedio = []
  for i in range(0,100):
    tiempo_inicial = time.time()
    my_tree = build_tree(training_data)
    tiempo_final = time.time()
    #print_tree(my_tree)
    tiempo_ejecución = tiempo_final - tiempo_inicial
    tiempopromedio.append(tiempo_ejecución)
    #print("Tarda " + str(round(tiempo_ejecución, 2)) + " segundos en ejecutar")
  suma = 0
  for j in range(0,100):
    suma+=tiempopromedio[j]
  prome = suma/100
  print("Tiempo promedio de ejecución: ",prome)
Exactitud(data_array_test, my_tree)
