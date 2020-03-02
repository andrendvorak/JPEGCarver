import io
import binascii
from PIL import Image

fileName = input("Enter the file name: ")

#Open file and while open read into completeFile and convert to hex representation
with open(fileName, 'rb') as file:
	completeFile = file.read()
	hexFile = binascii.hexlify(completeFile)

#Headers keeps track of header locations, count keeps track of number of images saved
headers = []
count = 0

#Go through hex file
for c in enumerate(hexFile):
	#If there are four characters, FFD8, in a row this means we found a header, add header location to list
	if hexFile[c[0]:c[0]+1].decode('ascii') == 'f' and hexFile[c[0]+1:c[0]+2].decode('ascii') == 'f' and hexFile[c[0]+2:c[0]+3].decode('ascii') == 'd' and hexFile[c[0]+3:c[0]+4].decode('ascii') == '8' and c[0]%2==0:
		headers.append(c[0])
	#If there are four characters, FFD9, in a row this means we found a footer, time to process and create image
	if hexFile[c[0]:c[0]+1].decode('ascii') == 'f' and hexFile[c[0]+1:c[0]+2].decode('ascii') == 'f' and hexFile[c[0]+2:c[0]+3].decode('ascii') == 'd' and hexFile[c[0]+3:c[0]+4].decode('ascii') == '9' and len(headers) != 0 and c[0]%2==0:
		#Initialize JPEGFile to be from the location of the last header found to the location of this footer
		JPEGFile = hexFile[headers.pop():c[0]+4]
		#Convert back to original binary representation from hex representation
		JPEGFile = binascii.unhexlify(JPEGFile)
		#Create Byte Stream
		stream = io.BytesIO(JPEGFile)
		#Attempt to save image, if it fails discard and continue
		try:
			img = Image.open(stream)
			img.save("image" + str(count) + ".jpg")
			img.close()
			count+=1
		except:
			pass
