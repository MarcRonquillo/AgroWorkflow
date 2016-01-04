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
		self.paths = self.get_general_paths()
		self.attributes = self.get_attributes()

	def get_attributes(self):
		
		# TODO Read the shape and the associated attribute table

		attributes = []

		return attributes


	def process_raster(self):

		#Define the processing based on the shape information

		#Basic Processing (RGB, )

		print "Basic processing has started"
		self.paths = basic_processing(self)

		print "Basic processing has ended"
			
		return self.paths

	def get_general_paths(self): # Solo funciona si le das el mosaico inicial!!
		# Divide the raster path
		pathSlash=self.raster.split("/")

		# Generate the general paths
		projectPath = "/".join(pathSlash[0:-5],)
		bulkPath = "/".join(pathSlash[0:-2],)
		rasterFolderPath = "/".join(pathSlash[0:-1],)
		shapeFolderPath = bulkPath + "/20_Shape"
		indexFolderPath = bulkPath + "/30_Indices_reales"
		interFolderPath = bulkPath + "/40_Archivos_intermedios"
		tablesPath = interFolderPath + "/reclass_tables"


		# Generate the path of the files

		rgbPath = rasterFolderPath + "/RGB.tif"
		pcdPath = indexFolderPath + "/PCD_raw.tif"
		pcd8bPath = indexFolderPath + "/PCD.tif"
		zonificationPath = indexFolderPath + "/PCD_zonificado_raw.tif"
		zonification8bPath = indexFolderPath + "/PCD_zonificado.tif"

		# Generate the path of the intermediate files

		pointsPath = interFolderPath + "/points.shp"
		pointsValuesPath = interFolderPath + "/points_values.shp"
		krigingPath = interFolderPath + "/kriging.sdat"
		smoothKrigingPath = interFolderPath + "/smoothed_kriging.tif"


		paths = {"project" : projectPath, "bulk" : bulkPath , "rasterFolder" : rasterFolderPath ,"shapeFolder" : shapeFolderPath, "indexFolder" : indexFolderPath ,
		 "interFolder" : interFolderPath, "tables" : tablesPath, "rgb" : rgbPath, "pcd" : pcdPath, "pcd8b" : pcd8bPath, "zonification" : zonificationPath, 
		 "zonification8b" : zonification8bPath, "points" : pointsPath, "pointsValues" : pointsValuesPath, "kriging" : krigingPath, "smoothKriging" : smoothKrigingPath }
		

		return paths






raster = "/media/sf_shared_folder_centos/20_Generacion_Entregables/10_Bulks/B1/10_Raster/B1.tif"

shape = "/media/sf_shared_folder_centos/20_Generacion_Entregables/10_Bulks/B1/20_Shape/B1.shp"

Bulk1 = Bulk(raster,shape)

Bulk1.paths = Bulk1.process_raster()

print Bulk1.paths["blue"]

print "Program is finished"
QgsApplication.exitQgis()


