# Este es un archivo de pruebas de Marc Ronquillo

import sys, os
from qgis.core import *
from PyQt4.QtGui import *

QgsApplication.setPrefixPath("/usr/bin", True)
app= QgsApplication([],True)
QgsApplication.initQgis()

#from os.path import expanduser
#home=expanduser("~")

sys.path.append(r"/home/postpro/.qgis2/python/plugins")

from processing.core.Processing import Processing
Processing.initialize()
from processing.tools import *

arguments=[]

def main():
	global arguments
	for arg in sys.argv:
		arguments.append(arg)
	print (str(arguments))

	

	general.runalg("qgis:convexhull",r"/media/sf_shared_folder_centos/punts.shp",None,0,r"/media/sf_shared_folder_centos/puntsOut.shp")




main()

QgsApplication.exitQgis()
