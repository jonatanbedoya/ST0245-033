from __future__ import print_function
import time
import pandas as pd

# Este método sirve para cargar los datos de prueba y training_data para el árbol de decisión
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

#Este método permite obtener los valores únicos que hay en la columna interesada (éxito)
def unique_vals(rows, col):
    return set([row[col] for row in rows])


#Este método cuenta la cantidad de valores iguales que existen en una columna del data set
def class_counts(rows):
    counts = {}  #diccionario para contar en la columna de exito, en este caso cantidad de 1s y 0s.
    for row in rows:
        # La última columna es la de exito, por lo tanto nuestra variable de decisión
        label = row[-1]
        if label not in counts:
            counts[label] = 0
        counts[label] += 1
    return counts

#Este método permite conocer cuál es el tipo de dato que se encuentra en la columna
#es necesario conocer el tipo para establecer la pregunta adecuada
def is_numeric(value):
    return isinstance(value, int) or isinstance(value, float)#devuelve falso si es un string o verdadero de lo contrario

class Question:
    # En esta clase se generan las preguntas que ayudan a partir el data set
    # estas preguntas surgen del information gain, pues es este quien dice cuales son las variables realmente.
    # Importate, la clase guarda una columna con los valores y el item para realizar la pregunta
    def __init__(self, column, value):
        self.column = column
        self.value = value

    def match(self, example):
       #El método match realiza la comparación validando el tipo de dato en la pregunta.
       # Numérico o string.
        val = example[self.column]
        if is_numeric(val):
            return val >= self.value
        else:
            return val == self.value

    def __repr__(self):
        # Según el criterio de comparación, se indica >= para número, == para string
        condition = "=="
        if is_numeric(self.value):
            condition = ">="
        return "Is %s %s %s?" % (
            header[self.column], condition, str(self.value))
    
# Permite subdividir los datos en aquellos que sí cumplen con la pregunta y los que no, esto se hace
# con el fin de crear las ramas del árbol
def partition(rows, question):
    true_rows, false_rows = [], []
    for row in rows:
        if question.match(row):
            true_rows.append(row)
        else:
            false_rows.append(row)
    return true_rows, false_rows

#Calcula la impureza de gini para una lista (o grupo) de filas
#Es un método de ayuda.
#Ver más en: https://en.wikipedia.org/wiki/Decision_tree_learning#Gini_impurity
def gini(rows):
    counts = class_counts(rows)
    impurity = 1
    for lbl in counts:
        prob_of_lbl = counts[lbl] / float(len(rows))
        impurity -= prob_of_lbl**2
    return impurity

# Calcula la incertidumbre entre el nodo de inicio
# Menos la impureza ponderada de los dos nodos hijos (o ramas).
# Se le conoce como ganancia de información
def info_gain(left, right, current_uncertainty):
    p = float(len(left)) / (len(left) + len(right))
    return current_uncertainty - p * gini(left) - (1 - p) * gini(right)

# Método que ayuda a encontrar la mejor pregunta para realizar iterando
# entre cada característica/valor, Calculando su ganancía de información
def find_best_split(rows):
    best_gain = 0  # Inicia un seguimiento de la ganancia de información
    best_question = None  # Mantiene la característica/valor que se produjó
    current_uncertainty = gini(rows)
    n_features = len(rows[0]) - 1  # número de columns

    for col in range(n_features):  # Para cada carectirística

        values = set([row[col] for row in rows])  # Valor único en las columna

        for val in values:  # para cada valor

            question = Question(col, val)

            # Intenta dividir los datos
            true_rows, false_rows = partition(rows, question)

            # Omite está división sino divide los datos.
            if len(true_rows) == 0 or len(false_rows) == 0:
                continue

            # Calcula la ganancia de información de la división
            gain = info_gain(true_rows, false_rows, current_uncertainty)
            # Se puede modificar el criterío de evaluación, según
            # lo que se quiera obtener se utilizó >= en nuestro caso.
            # Puede afectar la Exactitud
            if gain >= best_gain:
                best_gain, best_question = gain, question

    return best_gain, best_question

#Un nodo Hoja clasifica los datos.
#Esto contiene un diccionario de clase (por ejemplo para estatus, "3") -> número de veces
#aparece en las filas de training_data que llegan a esta hoja.
class Leaf:
    def __init__(self, rows):
        self.predictions = class_counts(rows)

#Un nodo de decisión hace una pregunta.
#Esto contiene una referencia a la pregunta y a los dos nodos hijos.
class Decision_Node:
    
    def __init__(self,
                 question,
                 true_branch,
                 false_branch):
        self.question = question
        self.true_branch = true_branch
        self.false_branch = false_branch

# Construye un árbol.
# Rules of recursion: 1) Believe that it works. 2) Start by checking
# for the base case (no further information gain). 3) Prepare for
# giant stack traces.
def build_tree(rows):
    # Intenta dividir el conjunto de datos en cada atributo único
    # Calcula la ganancia de información
    # Devuelve la pregunta que produce la mayor ganancia de informacion
    gain, question = find_best_split(rows)

    # Caso base: no más ganancia de información
    # Como no podemos hacer más preguntas,
    # Devolvemos una hoja
    if gain == 0:
        return Leaf(rows)

    # Si llegamos aquí, Se encontró una característica/valor útil
    # para particionar.
    true_rows, false_rows = partition(rows, question)

    # Recursivamente construye la rama (hijo) verdadera.
    true_branch = build_tree(true_rows)

    # Recursivamente construye la rama (hijo) falsa.
    false_branch = build_tree(false_rows)

    # Devuelve un nodo pregunta
    # Guarda la mejor característica/valor para preguntar en este momento
    # así como las ramas a seguir dependiendo de la respuesta.
    return Decision_Node(question, true_branch, false_branch)

# Método que ayuda a "mostrar" el arbol  
def print_tree(node, spacing=""):

    # Caso base: hemos llegado a una hoja
    if isinstance(node, Leaf):
        print (spacing + "Predict", node.predictions)
        return

    # Imprime la pregunta en este nodo
    print (spacing + str(node.question))

    # Llama a esta función recursivamente en la rama (o hijo) verdadera
    print (spacing + '--> True:')
    print_tree(node.true_branch, spacing + "  ")

    # Llama a esta función recursivamente en la rama (o hijo) falsa
    print (spacing + '--> False:')
    print_tree(node.false_branch, spacing + "  ")


def classify(row, node):
    """Ver las reglas de recursión, arriba."""

    # Caso base: hemos llegado a una hoja
    if isinstance(node, Leaf):
        return node.predictions
    
    # Decide seguir ya sea, la rama verdadera o la rama falsa
    # Compare la característica / valor almacenado en el nodo
    # Vamos a considerar (Se puede modificar).
    if node.question.match(row):
        return classify(row, node.true_branch)
    else:
        return classify(row, node.false_branch)
# Método que compara los datos_test con nuestro valores predecidos
# se obtiene una exactitud entre 0 y 100
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

# Una mejor manera de imprimir las predicciones en una hoja
def print_leaf(counts):
    total = sum(counts.values()) * 1.0
    probs = {}
    for lbl in counts.keys():
        probs[lbl] = str(int(counts[lbl] / total * 100)) + "%"
    return probs

# Para ejecutar, calcula un tiempo promedio de ejecución de 100 ejecuciones
# construye el arbol con el training_data & header
# Muestra la Exactitud de nuestro árbol 
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
