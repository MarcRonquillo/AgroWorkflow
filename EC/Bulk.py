# Bulk: Clase que se define como un grupo de parcelas. Seinicializa con un raster ya cortado y el shape que define las parcelas que aparecen en el mismo. Contiene metodos para el procesado de las imagenes que lo definen


# TODO Generar los imports necesarios para trabajar con raster y shape
# Marc Ronquillo. 
#Aqui empiezan los imports necesarios

import sys, os
from qgis.core import *
from PyQt4.QtGui import *

QgsApplication.setPrefixPath("/usr/bin", True)
app= QgsApplication([],True)
QgsApplication.initQgis()

sys.path.append("/home/postpro/.qgis2/python/plugins")

from processing.core.Processing import Processing
Processing.initialize()
import processing.tools as proctools

#Aqui terminan los imports necesarios


class Bulk:



	def __init__(self, raster,shape):

		self.raster = raster
		self.shape = shape
		self.attributes = self.get_attributes()
		print self.attributes

	def get_attributes(self):
		
		# TODO Read the shape and the associated attribute table

		print raster

		attributes = raster.split("/")

		return attributes


	def process_raster(self):

		#Define the processing based on the shape information

		#Basic Processing (RGB, )

		[RGB, PCD, Zonificado] = basicProcessing(raster,shape)





raster = "/path/B1/raster"
shape = "/path/B1/shape"

Bulk1 = Bulk(raster,shape)







