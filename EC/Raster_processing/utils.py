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

# GDAL para informacion del raster

import gdal

#Raster Calculator

from qgis.analysis import QgsRasterCalculator, QgsRasterCalculatorEntry
from PyQt4.QtCore import QFileInfo,QSettings

#Final de los imports


def split_bands(pathIn,pathOut):

# Recibe un path de entrada (raster multibanda) y devuelve las bandas por separado

	fileInfo=QFileInfo(pathIn)
	baseName=fileInfo.baseName()
	layer=QgsRasterLayer(pathIn, baseName)

	if not layer.isValid():
		print "Error importing Micasense Mosaic to split"

	print "Splitting bands from " + baseName

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

		# Saves the current band as a separate file
		#calc=QgsRasterCalculator(band.ref, pathOut+ "/" +baseName+"_band_"+str(i)+".tif","GTiff",layer.extent(),layer.width(),layer.height(), entries)
		#calc.processCalculation()
		
		output.append(pathOut+"/"+baseName+"_band_"+str(i)+".tif")
		i=i+1
	return output


def reclass_to_8(baseName,rasterPath,tablesPath,reclassifiedRasterPath = ""):

	print "Reclassifying " + baseName + " into 8 bits"

	# Divide the raster path
	pathSlash=rasterPath.split("/")

	# Generate the folder
	rasterFolderPath = "/".join(pathSlash[0:-1],)

	# Create the table path
	tablePath = tablesPath + "/" + baseName + ".txt"


	# If the user does not give any output path, it's created automatically
	if reclassifiedRasterPath == "":

		reclassifiedRasterPath = rasterFolderPath + "/" + baseName + "_8bits.tif"

	# Create a reclassification table if it's necessary

	if not os.path.isfile(tablePath):

		print "This table does not exist. Creating new reclsssifying table: " + tablePath

		raster = gdal.Open(rasterPath)

		band = raster.GetRasterBand(1)

		stats = band.GetStatistics(True,True)

		total_range = stats[1] - stats[0]


		tablePath = tablesPath + "/" + baseName + ".txt"

		reclass_table = create_reclass_table(tablePath,total_range)

	else:

		print "Table already exists: " + tablePath

		reclass_table = tablePath

	# Get the extent of the raster and reclassify it

	layer = QgsRasterLayer(rasterPath, baseName)

	extent = str(layer.extent().xMinimum()) + "," + str(layer.extent().xMaximum()) + "," + str(layer.extent().yMinimum()) + "," + str(layer.extent().yMaximum())

	output = reclassifiedRasterPath

	proctools.general.runalg("grass:r.recode",rasterPath,reclass_table,False,extent,0,output)

	return output


def create_reclass_table(tablePath,total_range):


	prueba = open(tablePath,"w")

	initial_value = float(0)


	table = ""

	for i in range(255):
		A = initial_value
		B = A + (float(total_range)/255)
		C = i

		fila = [A,B,C]

		table = table + ":".join(map(str,fila),) + "\n"

		initial_value = B

	prueba.write(table)
	prueba.close

	return tablePath
