#title           :utils.py
#description     :Cajon de sastre con varias funciones:
#					- getpath

#author          :EC - MR
#date            :20151224
#version         :0.1
#usage           :import utils
#notes           :
#==============================================================================

# QGIS Processing

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

#Raster Calculator

from qgis.analysis import QgsRasterCalculator, QgsRasterCalculatorEntry
from PyQt4.QtCore import QFileInfo,QSettings

#Final de los imports





def get_general_paths(rasterPath):
	# Divide the raster path
	pathSlash=rasterPath.split("/")
	# Generate the general paths
	rasterFolderPath = "/".join(pathSlash[0:-1],)
	bulkPath = "/".join(pathSlash[0:-2],)
	projectPath = "/".join(pathSlash[0:-5],)
	# Return the paths
	output = [rasterFolderPath,bulkPath,projectPath]
	return output

def get_path(rasterPath,filetype):
	pathSlash=rasterPath.split("/")
	rasterFolderPath = "/".join(pathSlash[0:-1],)
	bulkPath = "/".join(pathSlash[0:-2],)


	return pathSlash

# band_split recibe un path de entrada (raster multibanda) y devuelve las bandas por separado
def split_bands(pathIn,pathOut):

	fileInfo=QFileInfo(pathIn)
	baseName=fileInfo.baseName()
	layer=QgsRasterLayer(pathIn, baseName)

	if not layer.isValid():
		print "fail"

	numBands=layer.bandCount()
	i=1
	entries=[]
	output=[]
	while(i<=numBands):
		band = QgsRasterCalculatorEntry()
		band.ref = "band@"+str(i)
		band.raster=layer
		band.bandNumber=i
		entries.append(band)

		#calc=QgsRasterCalculator(band.ref, pathOut+baseName+"_band_"+str(i)+".tif","GTiff",layer.extent(),layer.width(),layer.height(), entries)
		#calc.processCalculation()
		
		output.append(pathOut+baseName+"_band_"+str(i)+".tif")
		i=i+1
	return output