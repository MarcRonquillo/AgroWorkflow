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


# Otros imports

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
	proctools.general.runalg("gdalogr:merge", red+";"+green+";"+blue,False,True,5,pathRGB)


	# Generate the Plant Cell Density index

	output = [pathRGB, pathPCD, pathZonificado]


	return output



