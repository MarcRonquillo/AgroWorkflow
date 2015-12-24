# Marc Ronquillo. 


#Aqui empiezan los imports necesarios para processing

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

#Aqui terminan los imports necesarios para processing

#Raster Calculator

from qgis.analysis import QgsRasterCalculator, QgsRasterCalculatorEntry
from PyQt4.QtCore import QFileInfo,QSettings

arguments=[]

def main():
	global arguments
	for arg in sys.argv:
		arguments.append(arg)
	print (str(arguments))




main()

QgsApplication.exitQgis()


	#proctools.general.runalg("gdalogr:merge","/media/sf_shared_folder_centos/gdal/R.tif;/media/sf_shared_folder_centos/gdal/G.tif;/media/sf_shared_folder_centos/gdal/B.tif",False,True,5,"/media/sf_shared_folder_centos/gdal/merged.tif")

	
#qgis y grass van bien. Saga tambien crea el output correctamente, pero al ejecutarlo vereis que indica "segmentation fault". Es al cerrar el script, cuando ya esta todo ejecutado y creado (nos la pela)
 
	#proctools.runalg("qgis:convexhull",r"/media/sf_shared_folder_centos/punts.shp",None,0,r"/media/sf_shared_folder_centos/puntsOut.shp")
	#proctools.general.runalg("grass:v.to.points","/home/postpro/test/line.shp","100",False,False,False,None,-1,0.0001,0,"/home/postpro/test/point.shp")
	#proctools.general.runalg("saga:simplefilter","/media/sf_shared_folder_centos/pcd.tif",1,0,5,"/media/sf_shared_folder_centos/saga_smooth.tif")
	#proctools.general.runalg("otb:smoothinggaussian","/media/sf_shared_folder_centos/pcd.tif",128,0,5,"/media/sf_shared_folder_centos/gauss_otb_2.tif")
'''
	fileName = "/media/sf_shared_folder_centos/pcd.tif"
	fileInfo = QFileInfo(fileName)
	baseName = fileInfo.baseName()
	rlayer = QgsRasterLayer(fileName, baseName)
	if not rlayer.isValid():
	  print "Layer failed to load!"
'''


