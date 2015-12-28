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

		operation = "("+band.ref+"=-32768)"

		# Saves the current band as a separate file
		calc=QgsRasterCalculator(band.ref, pathOut+baseName+"_band_"+str(i)+".tif","GTiff",layer.extent(),layer.width(),layer.height(), entries)
		calc.processCalculation()
		
		output.append(pathOut+baseName+"_band_"+str(i)+".tif")
		i=i+1
	return output


def reclass_16_to_8(rasterPath):

	# Divide the raster path
	pathSlash=rasterPath.split("/")
	# Generate the folder path and the filename
	rasterFolderPath = "/".join(pathSlash[0:-1],)
	filename = "".join(pathSlash[-1],)
	splitName = filename.split(".")
	baseName = "".join(splitName[0],)
	fileType = "".join(splitName[-1],)

	reclass_table = "/media/sf_shared_folder_centos/Reclass_16_to8.txt"

	layer = QgsRasterLayer(rasterPath, baseName)

	extent = str(layer.extent().xMinimum()) + "," + str(layer.extent().xMaximum()) + "," + str(layer.extent().yMinimum()) + "," + str(layer.extent().yMaximum())

	print extent

	output = rasterFolderPath + "/" + baseName + "_8bits.tif"

	proctools.general.runalg("grass:r.recode",rasterPath,reclass_table,False,extent,0,output)

	return output