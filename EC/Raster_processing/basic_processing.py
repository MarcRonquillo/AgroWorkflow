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

#return RGB, PCD, Zonificado
#raster= /path/B1/raster
def basic_processing(raster, shape):
	output=[]
	pathRGB=get_path(raster,"RGB")
	pathPCD=get_path(raster,"PCD")
	pathZonificado=get_path(raster,"Zonificado")

	output = [pathRGB, pathPCD, pathZonificado]

	print output

	return output

def get_path(raster, file):
	pathSlash=raster.split("/")
	return pathSlash

