#!/usr/bin/env python
'''
SCRAPPING Alquieres con MERCADOLIBRE - API
---------------------------
Autor: Inove Coding School
Version: 1.0
 
Descripcion:
Bajada de datos desde mercadolibre, utilizando el acceso via API POST que proveen.
El proceso esta preparado para descargar elementos de la categoría Inmblues, filtrado por Departamentos y Alquiler
 
Se puede configurar modo DEBUG (set_debug(true)) para solo procesar los primeros elementos, esto
tambien activa el modo "verbose" con salida detallada
 
Requisitos de instalacion:
 
- Python 3.x
- Libreriras (incluye los comandos de instalacion)
    pip install numpy
    pip install pandas

Datos útiles de la API de MercadoLibre
ID de las distintas categorías existentes
    https://developers.mercadolibre.com.ar/es_ar/categorias-y-atributos

'''

__author__ = "Inove Coding School"
__email__ = "INFO@INOVE.COM.AR"
__version__ = "1.0"


import requests                     # Bajada de datos URL
import json                         # La API utiliza Json para transmitir datos
import pandas as pd
import re                           # RegExp
from time import gmtime, strftime   # Para obtener la fecha actual
 
class inmueble:
    #mercadolibre_id = 'MLA79242' # Locales
    #mercadolibre_id = 'MLA79243' # Alquiler
    mercadolibre_id = 'MLA1459' # Inmuebles
    ubicacion = 'Capital Federal'
    columnas = ['fecha', 'latitud', 'longitud', 'url', 'titulo', 'tipo_propiedad', 'precio', 'moneda', 'm2', 'ambientes']
 
    # Serializo de json a dataframe y rearmado de datos para que sea formato tabla
    def serialize(self, items):
        data = pd.DataFrame(items)
        data = data.groupby(['id']).first().reset_index() # Elimina duplicados
 
        largo = data.shape[0]
        for i in range(0, largo):
            if(i % 100 == 0): print("Procesando: " + str(i) + " de " + str(largo))
            try:
                # La fecha es la fecha de ejecucion, lo utilizamos para identificar los reportes
                data.loc[i,'fecha'] = strftime("%Y_%m_%d", gmtime())
                data.loc[i,'mercadolibre_id'] = data.loc[i,'id']
                data.loc[i,'latitud'] = data.loc[i,'location']['latitude']
                data.loc[i,'longitud'] = data.loc[i,'location']['longitude']
                data.loc[i,'url'] = data.loc[i,'permalink']
                dataAttr = pd.DataFrame(data.loc[i,'attributes'])
                
                if(dataAttr.loc[dataAttr['id']=='PROPERTY_TYPE']['value_name'].count() > 0):
                    data.loc[i,'tipo_propiedad'] = dataAttr.loc[dataAttr['id']=='PROPERTY_TYPE']['value_name'].item()
                else:
                    data.loc[i,'tipo_propiedad'] = 'DESCONOCIDO'

                if(dataAttr.loc[dataAttr['id']=='TOTAL_AREA']['value_name'].count() > 0):
                    data.loc[i,'m2'] = dataAttr.loc[dataAttr['id']=='TOTAL_AREA']['value_name'].item().split(' ')[0]
                else:
                    data.loc[i,'m2'] = ''


                if(dataAttr.loc[dataAttr['id']=='ROOMS']['value_name'].count() > 0):
                    data.loc[i,'ambientes'] = dataAttr.loc[dataAttr['id']=='ROOMS']['value_name'].item()
                else:
                    data.loc[i,'ambientes'] = ''

                data.loc[i,'titulo'] = data.loc[i,'title']
                data.loc[i,'precio'] = data.loc[i,'price']
                data.loc[i,'moneda'] = data.loc[i,'currency_id']
                
 
            except Exception as e:
                print('Error adaptando: ' + str(i) + ' - ' + str(data.loc[i,'mercadolibre_id']) + ' - ' + ' -- %s' % e)
                pass            
        data = data.fillna('') # Los nulos los completamos con un string vacio
        return data[self.columnas]
 
class mercadolibreAPI:
    debug = False # Limita el procesamiento a los primeros elementos del primer indice, habilida la salida por pantalla de mensajes
    query = None 
    objeto = None
    meli_url = 'http://api.mercadolibre.com/sites/MLA/search?category='
    items = []
    pd.options.display.float_format = '{:.2f}'.format
 
    def set_debug(self, debug):
        self.debug = debug
        if(self.debug): print("Modo Debug ENCENDIDO")
 
    def request_get(self, url):
        if(self.debug): print("Procesando url: ", url)
        try:
            return requests.get(url).json()
        except:
            return None
 
    def search(self, objeto, pages_to_load = 0):
        self.objeto = objeto()
        parameters = '&q=Departamentos%20Alquiler%20'+re.sub("[ ,.]", "%20F", self.objeto.ubicacion)
        url = self.meli_url + self.objeto.mercadolibre_id + parameters 
        print("Buscando: " + url)
        if(self.debug):
            paginators = 5
        else:
            if pages_to_load == 0:
                paginators = round(self.request_get(url)['paging']['total']/50)+1
            else:
                paginators = pages_to_load
 
           
        for offset in range(0,paginators):
            url = self.meli_url + self.objeto.mercadolibre_id + parameters + '&limit=50&offset=' + str(offset*50)
            jsdata = self.request_get(url)
            try:
                if(jsdata is not None): self.items = self.items + jsdata['results']
            except:
                continue

        self.serialize()
 
    def serialize(self):
        o = self.objeto
        self.items = o.serialize(self.items)
 
    def export(self, tipo = 'csv'):
        if tipo.lower() == 'sql':
            self.export_sql()
        elif tipo.lower() == 'csv':
            self.export_csv()
        else:
            print("No existe el metodo de exportacion: " + tipo.lower())
    
    def export_sql(self):
        ## No implementado
        return None
 
    def export_csv(self):
        file_name = "propiedades" + ".csv"
        
        with open(file_name,"w+") as file:
            if(self.debug): print("Guardando archivo", file_name)
            self.items.to_csv(file_name, sep=",", decimal=".")

        
if __name__ == "__main__":
 
    meli = mercadolibreAPI()
    meli.set_debug(False)
    meli.search(inmueble)
    meli.export()
    print("Fin")