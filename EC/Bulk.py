# Bulk: Clase que se define como un grupo de parcelas. Seinicializa con un raster ya cortado y el shape que define las parcelas que aparecen en el mismo. Contiene métodos para el procesado de las imágenes que lo definen


# TODO Generar los imports necesarios para trabajar con raster y shape

import sys
from qgis.core import *
from PyQt4.QtGui import *
app= QApplication([])
QgsApplication.setPrefixPath("/usr/bin", True)
QgsApplication.initQgis()

sys.path.append("/home/postpro/.qgis2/python/plugins/")
import processing

from processing.core.Processing import Processing
Processing.initialize()
from processing.tools import *


class Bulk:


	def __init__(self, raster,shape):
		self.raster = raster
		self.shape = shape
		self.attributes = get_attributes()

	def get_attributes(self):
		
		# TODO Read the shape and the associated attribute table


		return attributes

	def process_raster(self):

		#Define the processing based on the shape information

		#Basic Processing

		basicProcessing(raster,shape)

		









