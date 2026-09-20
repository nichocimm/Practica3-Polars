# <center> Practica 3: Polars </center>

## <center>Integrantes <center>

<center>

| Nombre                         | Número de cuenta |
|:------------------------------:|:----------------:|
| Vega Navas Saúl                | 322088267        |
| Cimmino Yáñez Nicholas Joseph  | 322490712        |
| Benítez Pérez Kristian Leonel  | 322011346        |
| Herrera Cuamatla Jennifer Jade | 322255481        |

</center>

## Objetivo

En esta práctica se pondrá aprueba y a evaluación los siguientes puntos:

+ Aprender a estructurar correctamente un proyecto de mineria de datos
+ Seleccionar un framework de análisis de datos de manera correcta según el problema y los datos a analizar
+ Aplicar un preprocesamiento de los datos (normalización, eliminación de duplicados, conversión de tipos de datos e imputación) dados. 
+ Calcular e interpretar medidas de localización y variabilidad para un análisis exploratorio.

##  Fuente de los datos

La fuente de datos  oficial se obtuve del gobierno mexicano sobre violencia contra las mujeres, que esta disponible en este [enlace](https://www.inegi.org.mx/programas/endireh/2021/), en la sección de Microdatos, donde se descargó la base de datos en formato _csv_  y se juntó todos los archivos en un solo archivo csv, así como tambien se descargo el descriptor de archivos en formato _pdf_.

##  Instalación del entorno

Para poder instalar el entorno para ejecutar el programa es necesario ejecutar en la terminal
lo siguiente:

#### Windows:
```
python -m venv venv
pip install -r requirements.txt 
```

#### Mac o Linux:
```
python3 -m venv venv
pip install -r requirements.txt
```

## Ejecutar el  pipeline