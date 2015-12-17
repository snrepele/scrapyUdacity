Ejecutar en consola dentro de esta carpeta el comando SCRAPY crawl "nombreDeLaAraña" -j json



Existen cuatro arañas principales
udacity0 sirve para la pagina principal de cursos y entra a cada curso y saca su titulo y
su resumen

udacity1 entra en un curso y recorre sus paginas escogiendo sus links de temas 

udacity2 entra a cada link anterior para recoger las respuestas y comentarios

udacity3 ingresa a la informacion de cada usuario que ha realizado preguntas en el curso




Para cada uno de estos existe el archivo de configuración pipelines , sirve para guardar lo que saca 
cada script en una base de datos mysql , excepto para udacity1 pues solo extrae links y los guarda en un archivo
.csv

Se necesita activar cada pipelines cuando se ejecute la araña correspondiente