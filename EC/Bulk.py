#title           :Bulk.py
#description     :Clase que se define como un grupo de parcelas. Se inicializa con un raster ya 
#			 	  cortado y el shape que define las parcelas que aparecen en el mismo. 
#				  Contiene metodos para el procesado de las imagenes que lo definen
#author          :EC - MR
#date            :20151224
#version         :0.1
#usage           :python Bulk.py
#notes           :
#==============================================================================

#Imports para emplear el modulo processing de QGIS

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


#Imports para procesado de rasters

from Raster_processing.raster_processing import basic_processing

#Final de los imports

class Bulk:



	def __init__(self, raster,shape):

		self.raster = raster
		self.shape = shape
		self.attributes = self.get_attributes()

	def get_attributes(self):
		
		# TODO Read the shape and the associated attribute table

		attributes = raster.split("/")

		return attributes


	def process_raster(self):

		#Define the processing based on the shape information

		#Basic Processing (RGB, )

		print "Basic processing has started"
		[RGB, PCD, Zonificado] = basic_processing(raster,shape)
		print "Basic processing has ended"
			



raster = "/media/sf_shared_folder_centos/20_Generacion_Entregables/10_Bulks/B1/10_Raster/Vuelo_1.tif"

shape = "/path/B1/shape"

Bulk1 = Bulk(raster,shape)

Bulk1.process_raster()


print "Program is finished"
QgsApplication.exitQgis()


