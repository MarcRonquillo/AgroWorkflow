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

# Imports de GDAL

#sys.path.append("/usr/bin")
#import gdal_merge

# Imports de herramientas propias

from utils import *

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

	red_8b = reclass_16_to_8(red)
	blue_8b = reclass_16_to_8(blue)
	green_8b = reclass_16_to_8(green)

	os.system("gdal_merge.py -v -separate -o " + pathRGB + " -ot Byte -n 255 -a_nodata 255 "+ red_8b + " " + green_8b + " " + blue_8b)
	#os.system("gdal_translate -scale 0 32768 0 254 -a_nodata 0 -stats -ot Byte /media/sf_shared_folder_centos/RGB_gdal.tif /media/sf_shared_folder_centos/RGB_gdal_16b.tif")
	#os.system("rm /media/sf_shared_folder_centos/RGB_gdal_16b.tif")


	# Generate the Plant Cell Density index

	output = [pathRGB, pathPCD, pathZonificado]


	return output



