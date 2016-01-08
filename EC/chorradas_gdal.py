gdalbuildvrt -separate -srcnodata 255 /media/sf_shared_folder_centos/30_Entregables/Pruebas_virtual_raster/prueba.vrt /media/sf_shared_folder_centos/30_Entregables/B1/PCD.tif



gdal_translate -scale 0 32768 0 254 -a_nodata 0 -stats -ot Byte /media/sf_shared_folder_centos/RGB_gdal.tif /media/sf_shared_folder_centos/RGB_gdal_16b.tif"

gdaldem color-relief /media/sf_shared_folder_centos/30_Entregables/Pruebas_virtual_raster/prueba.vrt /media/sf_shared_folder_centos/30_Entregables/Pruebas_virtual_raster/rampa_prueba.txt /media/sf_shared_folder_centos/30_Entregables/Pruebas_virtual_raster/coloreado.tif

 gdal_translate -a_nodata 255 255 255 -b 1 -b 2 -b 3 /media/sf_shared_folder_centos/30_Entregables/Pruebas_virtual_raster/coloreado.tif /media/sf_shared_folder_centos/30_Entregables/Pruebas_virtual_raster/coloreado_ND255.tif