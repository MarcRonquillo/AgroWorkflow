# Marc Ronquillo. 
#Aqui empiezan los imports necesarios

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

#Aqui terminan los imports necesarios

arguments=[]

def main():
	global arguments
	for arg in sys.argv:
		arguments.append(arg)
	print (str(arguments))

	
#qgis y grass van bien. Saga tambien crea el output correctamente, pero al ejecutarlo veréis que indica "segmentation fault". Es al cerrar el script, cuando ya está todo ejecutado y creado (nos la pela)
 
	#proctools.runalg("qgis:convexhull",r"/media/sf_shared_folder_centos/punts.shp",None,0,r"/media/sf_shared_folder_centos/puntsOut.shp")
	#proctools.general.runalg("grass:v.to.points","/home/postpro/test/line.shp","100",False,False,False,None,-1,0.0001,0,"/home/postpro/test/point.shp")
	proctools.general.runalg("saga:simplefilter","/media/sf_shared_folder_centos/pcd.tif",1,0,5,"/media/sf_shared_folder_centos/saga_smooth.tif")


main()

QgsApplication.exitQgis()

