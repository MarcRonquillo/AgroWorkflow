from Raster_processing.utils import *

import gdal


rasterPath = "/media/sf_shared_folder_centos/20_Generacion_Entregables/10_Bulks/B1/10_Raster/2015-08-03T10_16_35Z_BGREN_Vuelo-1.tif"

raster = gdal.Open(rasterPath)

band = raster.GetRasterBand(1)

stats = band.GetStatistics(True,True)

total_range = stats[1] - stats[0]

create_reclass_table("pathPrueba","tabladeprueba")