#title           :raster_processing.py
#description     :Contiene las funciones para el procesado raster, que incluye:
#					- basic_processing: RGB, PCD y Zonificado
#date            :20151224
#version         :0.1
#usage           :python Bulk.py
#notes           :
#==============================================================================

# Imports para emplear el modulo processing de QGIS

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

# Imports de herramientas propias

from utils import *

#Raster Calculator

from qgis.analysis import QgsRasterCalculator, QgsRasterCalculatorEntry
from PyQt4.QtCore import QFileInfo,QSettings

# Final de los imports


def basic_processing(raster, shape):
	output=[]
	# Generate the general paths
	[rasterFolderPath,bulkPath,projectPath] = get_general_paths(raster)

	pathRGB = bulkPath + "/10_Raster/RGB.tif"
	pathPCD = bulkPath + "/30_Indices_reales/PCD_raw.tif"
	pathZonificado = bulkPath + "/30_Indices_reales/PCD_zonificado_raw.tif"

	# Divide the bands to process them separately
	[blue,green,red,redEdge,nir] = split_bands(raster,bulkPath+"/40_Archivos_intermedios/")

	# Generate the RGB composite and downgrade it to 8 bits
	'''
	print "Generating RGB Composite"
	red_8b = reclass_to_8(red,bulkPath + "/40_Archivos_intermedios/reclass_tables")
	blue_8b = reclass_to_8(blue,bulkPath + "/40_Archivos_intermedios/reclass_tables")
	green_8b = reclass_to_8(green,bulkPath + "/40_Archivos_intermedios/reclass_tables")

	os.system("gdal_merge.py -v -separate -o " + pathRGB + " -ot Byte -n 255 -a_nodata 255 "+ red_8b + " " + green_8b + " " + blue_8b)
	#os.system("gdal_translate -scale 0 32768 0 254 -a_nodata 0 -stats -ot Byte /media/sf_shared_folder_centos/RGB_gdal.tif /media/sf_shared_folder_centos/RGB_gdal_16b.tif")
	#os.system("rm /media/sf_shared_folder_centos/RGB_gdal_16b.tif")
	print "RGB Composite is available at " + pathRGB
	'''
	# Generate the Plant Cell Density index
	
	pathPCD = calculate_PCD(red,nir,bulkPath)


	output = [pathRGB, pathPCD, pathZonificado]


	return output

def calculate_PCD(red,nir,bulkPath):


	# Obtain file information and create the layers

	redInfo=QFileInfo(red)
	nirInfo=QFileInfo(nir)
	redBaseName=redInfo.baseName()
	nirBaseName=nirInfo.baseName()
	folderPath = redInfo.absolutePath()
	redReflectancePath = folderPath + "/red_reflectance.tif" 
	nirReflectancePath = folderPath + "/nir_reflectance.tif"

	redLayer = QgsRasterLayer(red,redBaseName)

	if not redLayer.isValid():
		print "Error importing red band to calculate reflectances"

	nirLayer = QgsRasterLayer(nir,nirBaseName)
	
	if not nirLayer.isValid():
		print "Error importing NIR band to calculate reflectances"


	# The images are transformed into reflectances by dividing by 32768

	entries=[]

	redReflectance = QgsRasterCalculatorEntry()
	redReflectance.ref = "red_band@1"
	redReflectance.raster=redLayer
	redReflectance.bandNumber = 1
	entries.append(redReflectance)
	
	# Converts the DN raster into a reflectance raster
	calc=QgsRasterCalculator('float(' + redReflectance.ref + ')/32768', redReflectancePath,"GTiff",redLayer.extent(),redLayer.width(),redLayer.height(), entries)
	calc.processCalculation()


	nirReflectance = QgsRasterCalculatorEntry()
	nirReflectance.ref = "nir_band@1"
	nirReflectance.raster=nirLayer
	nirReflectance.bandNumber = 1
	entries.append(nirReflectance)
	
	# Converts the DN raster into a reflectance raster
	calc=QgsRasterCalculator('float(' + nirReflectance.ref + ')/32768', nirReflectancePath,"GTiff",nirLayer.extent(),nirLayer.width(),nirLayer.height(), entries)
	calc.processCalculation()

	# Calculate the PCD index
	
	pcdPath = bulkPath + "/30_Indices_reales/PCD_raw.tif"

	calc=QgsRasterCalculator("float(" + nirReflectance.ref + ")/float(" + redReflectance.ref + ")", pcdPath,"GTiff",nirLayer.extent(),nirLayer.width(),nirLayer.height(), entries)
	calc.processCalculation()
	

	

	return pcdPath

