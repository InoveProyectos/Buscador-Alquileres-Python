#!/usr/bin/env python
'''
Presentación de alquileres en Mapa interactivo
---------------------------
Autor: Inove Coding School
Version: 1.0
 
Descripcion:
Se utiliza Flask para crear un WebServer que levanta los datos de alquileres de inmuebles
y los presenta en un mapa distribuidos por ubicación
 
Ejecución: Lanzar el programa y abrir en un navegador la siguiente dirección URL
http://127.0.0.1:5000/

Nos deberá aparecer el mapa con los alquileres de la zona, identificados por color:
- Verde: Alquiler dentro del promedio en precio
- Amarillo: Alquiler debajo del promedio en precio
- Rojo: Alquiler por arribba del promedio en precio
- Azul: Alquiler en dolares US$

- Podremos también visualizar el análisis de los alquileres de la zona
http://127.0.0.1:5000/reporte

- Podremos visualizar la predicción de costo de alquiler basado
 en el algoritmo de inteligencia artificial implementado
http://127.0.0.1:5000/prediccion

Requisitos de instalacion:

- Python 3.x
- Libreriras (incluye los comandos de instalacion)
    pip install numpy
    pip install pandas
    pip install -U Flask
'''

__author__ = "Inove Coding School"
__email__ = "INFO@INOVE.COM.AR"
__version__ = "1.0"


import pandas as pd
import numpy as np
import traceback
import io

from flask import Flask, request, jsonify, render_template, Response, redirect
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from sklearn import linear_model

import reporte as rp
import meli as ml

app = Flask(__name__)


@app.route("/")
def index():
    return redirect('/alquileres')

@app.route("/alquileres")
def alquileres():
    return render_template('index.html')

@app.route('/alquileres/propiedades') # Your API endpoint URL would consist /predict
def propiedades():
    try:
        df = pd.read_csv("propiedades.csv")

        # Clasifico los alquileres según el precio de cada uno
        propiedades_pesos = df.loc[df['moneda'] == 'ARS']

        # Analizo la media y los alquilers que se encuentra a un 20% de ella
        q_low = propiedades_pesos["precio"].quantile(0.30)
        q_hi  = propiedades_pesos["precio"].quantile(0.70)

        red_marker = 'http://www.openstreetmap.org/openlayers/img/marker.png'
        blue_marker = 'http://www.openstreetmap.org/openlayers/img/marker-blue.png'
        gold_marker = 'http://www.openstreetmap.org/openlayers/img/marker-gold.png'
        green_marker = 'http://www.openstreetmap.org/openlayers/img/marker-green.png'

        # Marco que bandera o marca mostrar en cada caso
        df['marca'] = df.apply(lambda x: blue_marker if x['moneda'] == 'USD' else gold_marker if x['precio'] < q_low else red_marker if x['precio'] > q_hi else green_marker, axis=1 )

        result = df.to_json()
        return(result)
    except:
        return jsonify({'trace': traceback.format_exc()})

@app.route('/alquileres/reporte') # Your API endpoint URL would consist /predict
def reporte():
    try:
        # Utilizo el programa de reporte para generar el gráfico y mostrarlo en la web
        fig = rp.generar_reporte(reporte=0, silent_mode=True)
        
        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)
        return Response(output.getvalue(), mimetype='image/png')
    except:
        return jsonify({'trace': traceback.format_exc()})

@app.route('/alquileres/prediccion') # Your API endpoint URL would consist /predict
def prediccion():
    try:
        # Utilizo el programa de reporte para generar el gráfico y mostrarlo en la web
        fig = rp.generar_reporte(reporte=5, silent_mode=True)

        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)
        return Response(output.getvalue(), mimetype='image/png')
    except:
        return jsonify({'trace': traceback.format_exc()})

@app.route('/alquileres/buscar') # Your API endpoint URL would consist /predict
def buscar():
    try:
        # Utilizo el modulo "meli" para generar un archivo CSV con los alquileres

        ubicacion = request.args.get('ubicacion')
        if ubicacion is None:
            ubicacion = 'Capital Federal'

        meli = ml.mercadolibreAPI()
        meli.set_debug(True)
        meli.search(ml.inmueble, ubicacion, 10)
        df = meli.export('df')

        return Response(
            df.to_csv(),
            mimetype="text/csv",
            headers={"Content-disposition":
            "attachment; filename=propiedades.csv"})

    except:
        return jsonify({'trace': traceback.format_exc()})


if __name__ == '__main__':
    try:
        port = int(sys.argv[1]) # This is for a command-line argument
    except:
        port = 5000 # Puerto default
        
    app.run(host='0.0.0.0', port=port, debug=True)