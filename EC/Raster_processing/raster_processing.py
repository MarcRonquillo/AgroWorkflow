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


def basic_processing(bulk):

	# Divide the bands to process them separately
	[bulk.paths["blue"],bulk.paths["green"],bulk.paths["red"],bulk.paths["redEdge"],bulk.paths["nir"]] = split_bands(bulk.raster,bulk.paths["interFolder"])

	print "Bands succesfully splitted"

	# Generate the RGB composite and downgrade it to 8 bits
	
	print "Generating RGB Composite"
	red_8b = reclass_to_8("red",bulk.paths["red"],bulk.paths["tables"])
	blue_8b = reclass_to_8("blue",bulk.paths["blue"],bulk.paths["tables"])
	green_8b = reclass_to_8("green",bulk.paths["green"],bulk.paths["tables"])

	
	os.system("gdal_merge.py -v -separate -o " + bulk.paths["rgb"] + " -ot Byte -n 255 -a_nodata 255 "+ red_8b + " " + green_8b + " " + blue_8b)
	#os.system("gdal_translate -scale 0 32768 0 254 -a_nodata 0 -stats -ot Byte /media/sf_shared_folder_centos/RGB_gdal.tif /media/sf_shared_folder_centos/RGB_gdal_16b.tif")
	#os.system("rm /media/sf_shared_folder_centos/RGB_gdal_16b.tif")
	print "RGB Composite is available at " + bulk.paths["rgb"]
	
	# Generate the Plant Cell Density index
	
	calculate_PCD(bulk.paths["red"],bulk.paths["nir"],bulk.paths["pcd"])
	
	# Generate the Zonification

	dose_map(bulk.paths["pcd"], bulk.shape, bulk.paths["zonification"], bulk.paths["points"], bulk.paths["pointsValues"], bulk.paths["kriging"], bulk.paths["smoothKriging"])
	

	# Transform the PCD and the zonification into 8 bits 

	pcd_8b = reclass_to_8("PCD",bulk.paths["pcd"],bulk.paths["tables"],bulk.paths["pcd8b"])

	zonification_8b = reclass_to_8("PCD",bulk.paths["zonification"],bulk.paths["tables"],bulk.paths["zonification8b"])




	return bulk.paths


def dose_map(pathPCD,pathShape,pathZonificado,pathPuntos,pathPuntosValores,pathKriging,pathSmoothKriging):


	# Open the PCD as a layer

	pcdLayer = QgsRasterLayer(pathPCD,"PCD")

	if not pcdLayer.isValid():
		print "Error importing PCD"	

	extent = str(pcdLayer.extent().xMinimum()) + "," + str(pcdLayer.extent().xMaximum()) + "," + str(pcdLayer.extent().yMinimum()) + "," + str(pcdLayer.extent().yMaximum())	
	
	print extent

	# Generate random points in the PCD extent

	#proctools.general.runalg("qgis:randompointsinextent",extent,50000,0,pathPuntos)
	#proctools.general.runalg("grass:v.random",50000,0,0,"z",False,extent,0,pathPuntos)

	# Get raster values to points

	proctools.general.runalg("grass:v.sample",pathPuntos,"z",pathPCD,1,False,False,extent,-1,0.0001,0,pathPuntosValores)

	print "Points succesfully generated"

	# Select the points with value higher than 0 (Done automatically by the grass:sample algorithm)

	# Do the kriging WITH THE PCD EXTENT!!

	proctools.general.runalg("saga:ordinarykriging",pathPuntosValores,"rast_val",0,False,True,100,-1,100,1,"a + b * x",0,1000,0,4,20,0,extent,1,0,None,pathKriging,None)

	print "Kriging generated"

	# Smooth the result

	os.system("otbcli_Smoothing -in " + pathKriging + " -out " + pathSmoothKriging + " -type gaussian -type.gaussian.radius 5")
	
	print "Kriging smoothed"

	# Cut the raster and save the result
	os.system("gdalwarp -q -of GTiff -dstnodata 0 -tr 1.0 -1.0 -tap -cutline " + pathShape + " -crop_to_cutline " + pathSmoothKriging + " " +pathZonificado)
	
	print "PCD Zonification created succesfully"

def calculate_PCD(red,nir,pcdPath):


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

	calc=QgsRasterCalculator("float(" + nirReflectance.ref + ")/float(" + redReflectance.ref + ")", pcdPath,"GTiff",nirLayer.extent(),nirLayer.width(),nirLayer.height(), entries)
	calc.processCalculation()
	
	print "PCD calculated"
