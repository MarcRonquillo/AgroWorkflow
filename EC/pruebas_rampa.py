
classes = 3

rasterMin = 5

rasterMax = 254

colorRampPath = "/home/postpro/Agro-workflow/AgroWorkflow/EC/resources/rampa_ejemplo_3.txt"


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

createColorRamp(classes, rasterMin, rasterMax, colorRampPath)