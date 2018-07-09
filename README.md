# Proyecto BigData

## Dataset

Se utilizó el dataset de sentimientos de twitter apple, disponible en el enunciado del proyecto./

## Requerimientos

Para realizar los siguientes experimentos, para prepocesamiento se utilizo excel y python 3.6. Para el training se requirio instalar python 2.7 y utilizar pip para instalar la libreria Gensim, para ello seguimos el siguiente tutorial: http://blog.leifmadsen.com/blog/2017/01/03/installing-python-2.7-on-centos-6.x/. Por último, usamos 
GloVe de 6B en su version de 50 dimensiones, el cual es transformado al formato de gensim con el script convert.py disponible en (INSERTAR LINK)

## Preprocesamiento. 

### Parte 1. Excel

Para el preprocesamiento, se elimino las columnas no utiles con excel, y se filtro todas las entradas que no tenian una nota valida de sentimiento.

### Parte 2. Python

El resultado anterior deja un archivo en el cual hay caracteres especiales (',','.','#',...) y hay un serio problema con los saltos de linea. En 
especifico, los saltos de lineas son utilizados para separar los tweets, pero tambien pueden existir en los mismos tweets. Por ultimo,
en adición a las correcciones anteriores, la libreria mllib de pyspark no soporta multiples clases (los sentimientos en este dataset van de 1 a 5), por lo que los pasamos en la siguiente forma, si el sentimiento es 3 4 o 5 entonces 1, en caso contrario 0.

## Training

Al igual que la tarea 3, no se cambio el archivo de flume respecto a la pregunta 3 de esta tarea, el cual esta disponible en (INSERTAR LINK).
Sin embargo, el script de spark tuvo que cambiar en gran medida. Primero filtramos que el streaming no sea vacio (para no procesar data vacia). Tambien agregamos GloVe con 50 dimensiones para codificar las palabras. Si una palabra no se encuentra esta se ignora. Posteriormente promediamos los embeddings de las palabras en el diccionario. Esto despues lo pasamos por un clasificador LinearSVM, disponible en la libreria mllib(from pyspark.mllib.classification import SVMWithSGD). Por último, hacemos las predicciones, imprimimos la matriz de confusion y guardamos los vectores con su prediccion y valor real, los cuales son procesados en un script externo. 

## Resultados

Con el trabajo realizado previamente, se obtiene la siguiente matriz de confusión: 
``` [[319, 900], [124, 2461]] ```

Se reutilizó el tsne de la tarea 3 para mostrar los resultados. En el gráfico los puntos morados representan las clasificaciones predecidas correctamente y en amarillo los errores.

![TSNE](./tsne/tsne.png)

