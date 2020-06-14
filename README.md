![Inove banner](/inove.jpg)
Inove Escuela de Código - Trabajamos en pos de que nuestros alumnos logren sus metras personales y profesionales\
info@inove.com.ar\
Web: [Inove](http://inove.com.ar)

# Buscador-Alquileres-Python
API hecha en Python para buscar alquileres de departamentos y visualizarlos en un mapa

# Descripción:
Esta aplicación hecha en Python utiliza Flask para crear un WebServer que levanta los datos de alquileres de inmuebles
y los presenta en un mapa distribuidos por su ubicación.\
Además, los alquileres se identifican con colores en el mapa según el precio y relación con la media.

# Probar el programa en la nube
Si desean probar como funciona este programa sin necesidad de descargar el código pueden ingresar al siguiente link:\
[inove.api](http://inove.pythonanywhere.com/alquileres)

Luego para utilizar la API les recomiendo que lean la sección de "__Como utilizar la API__".

# Lanzar la API
Para lanzar el programa debemos ejecutar el script de python en nuestra consola:\
`python map.py`

Luego debemos abrir un explorador de internet e ingresar el siguiente link URL\
http://127.0.0.1:5000/alquileres

# Como utilizar la API
Al ingresar al link nos deberá aparecer el mapa con los alquileres de la zona, identificados por color:
- Verde: Alquiler dentro del promedio en precio
- Amarillo: Alquiler debajo del promedio en precio
- Rojo: Alquiler por arribba del promedio en precio
- Azul: Alquiler en dolares US$

![Inove banner](/images/mapa.png)

- Podremos también visualizar el análisis de los alquileres de la zona:

__Versión offline__\
http://127.0.0.1:5000/alquileres/reporte

__Versión online__\
http://inove.pythonanywhere.com/alquileres/reporte

![Inove banner](/images/reporte.png)

- Podremos visualizar la predicción de costo de alquiler basado en el algoritmo de inteligencia artificial implementado:

__Versión offline__\
http://127.0.0.1:5000/alquileres/prediccion

__Versión online__\
http://inove.pythonanywhere.com/alquileres/prediccion

![Inove banner](/images/prediccion.png)

# Muchas gracias!
Espero hayan disfrutado de esta aplicación, cualquier duda o sugerencia pueden contartarse con Inove al mail info@inove.com.ar
o ingresar a nuestra página [Inove](http://inove.com.ar).

Seguinos en las redes

[![alt text][1.1]][1]
[![alt text][2.1]][2]
[![alt text][3.1]][3]
[![alt text][4.1]][4]
[![alt text][5.1]][5]

[1.1]: https://github.com/InoveProyectos/Buscador-Alquileres-Python/blob/master/assets/facebook.png
[2.1]: https://github.com/InoveProyectos/Buscador-Alquileres-Python/blob/master/assets/instagram.png
[3.1]: https://github.com/InoveProyectos/Buscador-Alquileres-Python/blob/master/assets/twitter.png
[4.1]: https://github.com/InoveProyectos/Buscador-Alquileres-Python/blob/master/assets/linkedin.png
[5.1]: https://github.com/InoveProyectos/Buscador-Alquileres-Python/blob/master/assets/youtube.png

[1]: https://web.facebook.com/inovecode/
[2]: https://www.instagram.com/inovecode/
[3]: https://twitter.com/inovecode
[4]: https://www.linkedin.com/company/inovecode/
[5]: https://www.youtube.com/channel/UCwMey2qq3SDpS2Sl3CnjLEA/featured
