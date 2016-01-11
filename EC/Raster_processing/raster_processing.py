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
	
	
	# Transform the PCD and the zonification into 8 bits (AP Deliverables) 
	
	pcd_8b = reclass_to_8("PCD",bulk.paths["pcd"],bulk.paths["tables"],bulk.paths["pcd8b"])

	zonification_8b = reclass_to_8("PCD",bulk.paths["zonification"],bulk.paths["tables"],bulk.paths["zonification8b"])
	
	# Apply color to the PCD and the zonification (VN Deliverables) and copy the RGB
	
	os.system("cp " + bulk.paths["rgb"] + " " + bulk.paths["rgbVN"])

	pcdVN = applyColor(bulk.paths["pcd8b"],bulk.paths["interFolder"],bulk.paths["pcdVN"],bulk.paths["colorRamps"], "PCD")

	zonificationVN = applyColor(bulk.paths["zonification8b"], bulk.paths["interFolder"], bulk.paths["zonificationVN"],bulk.paths["colorRamps"], "Zonification")


	return bulk.paths


def target_sectors(bulk):

	# Create the intermediate and final paths

	targetSectorsNC = bulk.paths["interFolder"] + "/target_sectors_NC.tif"

	targetSectors = bulk.paths["VNDeliverables"] + "/Target_Sectors.tif"

	bulk.paths["shapeStatistics"] = create_statistics(bulk.shape, bulk.paths["pcd8b"], bulk.paths["shapeFolder"])

	os.system("gdal_rasterize -a pcd_mean -a_nodata 255 -tr 1.0 1.0 -l statistics " + bulk.paths["shapeStatistics"] + " " + targetSectorsNC)

	applyColor(targetSectorsNC,bulk.paths["interFolder"],targetSectors,bulk.paths["colorRamps"],"Target_Sectors")


	return bulk.paths

def variability_map(bulk):

	# Create the intermediate and final paths

	variabilityMapNC = bulk.paths["interFolder"] + "/variability_map_NC.tif"

	variabilityMap = bulk.paths["VNDeliverables"] + "/Variability_Map.tif"

	bulk.paths["shapeStatistics"] = create_statistics(bulk.shape, bulk.paths["pcd8b"], bulk.paths["shapeFolder"])

	os.system("gdal_rasterize -a pcd_std -a_nodata 255 -tr 1.0 1.0 -l statistics " + bulk.paths["shapeStatistics"] + " " + variabilityMapNC)

	applyColor(variabilityMapNC,bulk.paths["interFolder"],variabilityMap,bulk.paths["colorRamps"],"Variability_Map")
	

	return bulk.paths



def create_statistics(shapePath, indexPath, shapeFolderPath):

	shapeStatistics = shapeFolderPath + "/statistics.shp"

	if not os.path.isfile(shapeStatistics):

		# Create the vector layer to run the algorithm

		shapeLayer = QgsVectorLayer(shapePath, "shape", "ogr")

		# Generate the statistics

		print "Calculating Zonal Statistics"

		proctools.general.runalg('qgis:zonalstatistics',indexPath,1,shapeLayer, "pcd_",True,shapeStatistics)

	else:

		print "Zonal Statistics exist already"

	return shapeStatistics



def createColorRamp(classes, rasterMin, rasterMax, colorRampPath):


	# Open the txt ramp file

	txt = open(colorRampPath,"w")

	ramp = ""

	if classes == 5: # Blue - Light Blue - Green - Yellow - Red

		ran = (rasterMax -rasterMin)/classes

		ramp = str(rasterMax) + " 0 0 254 \n" + str(rasterMax-ran) + " 51 194 254 \n" + str(rasterMax-2*ran) + " 182 254 143 \n" + str(rasterMax-3*ran) + " 254 200 0 \n" + str(rasterMax-4*ran) + " 254 0 0 \n" + "nv 255 255 255"
	
	if classes == 4:

		ran = (rasterMax -rasterMin)/classes

		ramp = str(rasterMax) + " 0 0 254 \n" + str(rasterMax-ran) + " 51 194 254 \n" + str(rasterMax-2*ran) + " 254 200 0 \n" + str(rasterMax-3*ran) + " 254 0 0 \n" + "nv 255 255 255"
	
	if classes == 3:

		ran = (rasterMax -rasterMin)/classes

		ramp = str(rasterMax) + " 157 204 16 \n" + str(rasterMax-ran) + " 199 227 113 \n" + str(rasterMax-2*ran) + " 236 252 204 \n" + "nv 255 255 255"


	txt.write(ramp)
	txt.close

	return colorRampPath


def applyColor(rasterPath,temporalRasterFolderPath,colouredRasterPath,colorRampsPath,deliverableType):

	# Check the type of deliverable: Index (for PCD/Zonification), Target Sectors or Variability Map
	if deliverableType == "PCD" or deliverableType == "Zonification":

		# Create the layer to read max and min real values
		rasterLayer = QgsRasterLayer(rasterPath,"raster")

		dp = rasterLayer.dataProvider()
		stats = dp.bandStatistics(1)

		rasterMax = stats.maximumValue
		rasterMin = stats.minimumValue

		# Create the color ramp path

		colorRampPath = colorRampsPath + "/" + deliverableType + ".txt"

		# Create the color ramp

		colorRamp = createColorRamp(5, rasterMin, rasterMax,colorRampPath)


	elif deliverableType == "Target_Sectors":

		# Create the layer to read max and min real values
		rasterLayer = QgsRasterLayer(rasterPath,"raster")

		dp = rasterLayer.dataProvider()
		stats = dp.bandStatistics(1)

		rasterMax = stats.maximumValue
		rasterMin = stats.minimumValue

		# Create the color ramp path

		colorRampPath = colorRampsPath + "/" + deliverableType + ".txt"

		# Create the color ramp

		colorRamp = createColorRamp(4, rasterMin, rasterMax,colorRampPath)


	elif deliverableType == "Variability_Map":

		# Create the layer to read max and min real values
		rasterLayer = QgsRasterLayer(rasterPath,"raster")

		dp = rasterLayer.dataProvider()
		stats = dp.bandStatistics(1)

		rasterMax = stats.maximumValue
		rasterMin = stats.minimumValue

		# Create the color ramp path

		colorRampPath = colorRampsPath + "/" + deliverableType + ".txt"

		# Create the color ramp

		colorRamp = createColorRamp(3, rasterMin, rasterMax,colorRampPath)


	else:
		print "Type of deliverable is not valid (applyColor)"




	temporalRasterPath = temporalRasterFolderPath + "/temporal.tif"

	# Delete the temporal file if it exists
	if os.path.isfile(temporalRasterPath):

		os.system("rm " + temporalRasterPath)

	# Apply the color ramp 
	
	os.system("gdaldem color-relief " + rasterPath + " " + colorRamp + " " + temporalRasterPath)

	# Add a NoData value to the raster

	os.system("gdal_translate -a_nodata 255 -b 1 -b 2 -b 3 " + temporalRasterPath + " " + colouredRasterPath)
	
	# Delete the temporal file if it exists
	if os.path.isfile(temporalRasterPath):

		os.system("rm " + temporalRasterPath)

	return colouredRasterPath


def dose_map(pathPCD,pathShape,pathZonificado,pathPuntos,pathPuntosValores,pathKriging,pathSmoothKriging):


	# Open the PCD as a layer

	pcdLayer = QgsRasterLayer(pathPCD,"PCD")

	if not pcdLayer.isValid():
		print "Error importing PCD"	

	rasterExtent = str(pcdLayer.extent().xMinimum()) + "," + str(pcdLayer.extent().xMaximum()) + "," + str(pcdLayer.extent().yMinimum()) + "," + str(pcdLayer.extent().yMaximum())	


	# Generate random points in the PCD extent


	shapeLayer = QgsVectorLayer(pathShape, "pol", "ogr")

	if not shapeLayer.isValid():
		print "Error importing PCD"	

	shapeExtent = str(shapeLayer.extent().xMinimum()) + "," + str(shapeLayer.extent().xMaximum()) + "," + str(shapeLayer.extent().yMinimum()) + "," + str(shapeLayer.extent().yMaximum())	
	

	#proctools.general.runalg("qgis:randompointsinlayerbounds",shapeLayer,30000,0,pathPuntos)

	proctools.general.runalg("qgis:randompointsinsidepolygonsfixed",shapeLayer,1,0.5,0,pathPuntos)

	# Get raster values to points

	proctools.general.runalg("grass:v.sample",pathPuntos,"id",pathPCD,1,False,False,rasterExtent,-1,0.0001,0,pathPuntosValores)

	print "Points succesfully generated"
	
	# Select the points with value higher than 0 (Done automatically by the grass:sample algorithm)

	# Do the kriging WITH THE PCD EXTENT!!
	
	proctools.general.runalg("saga:ordinarykriging",pathPuntosValores,"rast_val",0,False,True,100,-1,100,1,"a + b * x",0,1000,0,4,20,0,rasterExtent,1,0,None,pathKriging,None)

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
