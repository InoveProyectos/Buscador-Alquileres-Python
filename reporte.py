#!/usr/bin/env python
'''
Reporte búsqueda de alquileres de Inmuebles
---------------------------
Autor: Inove Coding School
Version: 1.0
 
Descripcion:
Este script realiza reportes de los datos adquiridos de alquileres de inmuebles
Reporte Nº
0: Visualizar todos los reportes juntos de estudio por ambientes y m2
1: Cantidad de alquileres por ambiente
2: Precio por ambiente
3: Cantidad de alquileres por m2
4: Precio por m2
5: Calcular y visualizar le prediccion de costos por m2

Requisitos de instalacion:
 
- Python 3.x
- Libreriras (incluye los comandos de instalacion)
    pip install numpy
    pip install pandas
    pip install matplotlib
    pip install seaborn
    pip install sklearn
'''

__author__ = "Inove Coding School"
__email__ = "INFO@INOVE.COM.AR"
__version__ = "1.0"

import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.axes
import seaborn as sns
from sklearn import linear_model

def generar_reporte(reporte, silent_mode=False):

    df = pd.read_csv("propiedades.csv")

    # Sacamos todas las filas de la tabla las cuales el campo "m2" o "ambientes" se encuentre vacio
    propiedades = df[df['m2'].notna()]
    propiedades = propiedades[propiedades['ambientes'].notna()]

    # Nos quedamos solamente con aquellas filas que el precio haya sido informado en pesos Argentinos
    propiedades = propiedades.loc[propiedades['moneda'] == 'ARS']

    # Como alternativa se puede pasar los precios en dolares a pesos, pero en general estos datos se escapan de la media
    #dolar_pesos = 67
    #propiedades['precio'] = propiedades.apply(lambda x: x['precio']*dolar_pesos if x['moneda']  == 'USD' else x['precio'], axis = 1)
    
    # Obtener cuantos alquileres por ambientes hay
    ambientes = propiedades.groupby('ambientes')['ambientes'].count()
    ambientes_df = ambientes.reset_index(name='cantidad')

    # Obtener el precio promedio por cantidad de ambientes
    precio_por_ambiente = propiedades.groupby('ambientes')['precio'].mean()/1000
    precio_por_ambiente_df = precio_por_ambiente.reset_index(name='precio')

    fig = plt.figure(figsize=(16,9))
    axs = np.empty(4, dtype=type(matplotlib.axes))
    
    # En funcion del reporte a mostrar defino el estilo del gráfico
    if reporte < 5:
        sns.set_style("white")
    else:
        sns.set_style("whitegrid", {'grid.linestyle': '--'})

    if reporte == 0:
        # En el caso de desear visualizar todos los gráficos genero subplots para mostarlos juntos
        axs[0] = fig.add_subplot(221)
        axs[1] = fig.add_subplot(222)
        axs[2] = fig.add_subplot(223)
        axs[3] = fig.add_subplot(224)
    elif reporte <= 4:
        # Creo unicamente el gráifico que voy a mostrar
        axs[reporte-1] = fig.add_subplot(111)
    elif reporte == 5:
        ax1 = fig.add_subplot(111)
    elif reporte == 6:
        axs[0] = fig.add_subplot(121)
        axs[1] = fig.add_subplot(122)
    elif reporte == 7:
        axs[2] = fig.add_subplot(121)
        axs[3] = fig.add_subplot(122)

    if reporte == 0 or reporte == 1 or reporte == 6:
        # Graficar "Cantidad de alquileres por ambiente"
        ax = sns.barplot(x=ambientes_df['ambientes'], y=ambientes_df['cantidad'], ax=axs[0])
        ax.set_alpha(0.8)
        ax.set_title("Cantidad de alquileres por ambiente", fontsize=15)
        ax.set_ylabel("Cantidad", fontsize=12)
        ax.set_xlabel("Ambientes", fontsize=12)
    

    if reporte == 0 or reporte == 2 or reporte == 6:
        # Graficar "Precio por ambiente"
        ax = sns.barplot(x=precio_por_ambiente_df['ambientes'], y=precio_por_ambiente_df['precio'], palette="pastel", ax=axs[1])
        ax.set_alpha(0.8)
        ax.set_title("Precio por ambiente", fontsize=15)
        ax.set_ylabel("Precio[miles de pesos]", fontsize=12)
            
    if reporte == 0 or reporte == 3 or reporte == 7:
        # Graficar "Cantidad de alquileres por m2"
        ax = sns.distplot(propiedades['m2'], bins=40, kde=True, kde_kws={"color": "blue", "alpha":0.3, "linewidth": 1, "shade":True }, ax=axs[2])
        ax.set_title("Cantidad de alquileres por m2", fontsize=15, y=0.7, x = 0.5)
        ax.set_ylabel("Cantidad", fontsize=12)
        ax.set_xlabel('m2')

    if reporte == 0 or reporte == 4 or reporte == 7:
        # Graficar "Precio por m2"
        ax = sns.scatterplot(propiedades['m2'],propiedades['precio']/1000, color='blue', ax=axs[3])
        ax.set_title("Precio por m2", fontsize=15, y=-0.01)
        ax.set_ylabel("Precio[miles de pesos]", fontsize=12)
        ax.set_xlabel('m2')

    if reporte == 5:
        # Calcular y visualizar le prediccion de costos por m2
        regr = linear_model.LinearRegression()
        x = np.asanyarray(propiedades[['ambientes','m2']])
        y = np.asanyarray(propiedades['precio'])
        regr.fit(x, y)
        y_hat= regr.predict(propiedades[['ambientes','m2']])

        # Graficar "Precio por m2"
        sns.set_style("whitegrid", {'grid.linestyle': '--'})
        ax = sns.scatterplot(propiedades['m2'],propiedades['precio']/1000, color='blue', ax=ax1)
        ax = sns.lineplot(propiedades['m2'],y_hat/1000, color='red', ax=ax1)
        ax.set_title("Precio por m2", fontsize=15)
        ax.set_ylabel("Precio[miles de pesos]", fontsize=12)
        ax.set_xlabel('m2')
        plt.legend(('predicción', 'precio publicado '), prop={'size': 15})

    if silent_mode == False:
        plt.show(block=True)

    return fig

if __name__ == '__main__':
    try:
        reporte = int(sys.argv[1]) # Tomo el número de reporte de la líne ade comando
    except:
        reporte = 0 # Sino especificamos el reporte a visualizar se mostrarán todos

    if(reporte < 0 or reporte > 7):
        print("Error: El reporte especificado debe estar entre los valores 0 y 7")

    generar_reporte(reporte=reporte)