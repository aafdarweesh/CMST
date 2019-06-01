
import pickle
import os


#Common variables (Detection)
location_of_detection_program = 'C:\\tensorflow1\\models\\research\\object_detection'
name_of_detection_program = 'Object_detection_video.py'
location_of_the_video = 'C:\\Users\\Administrator\\Desktop\\CMSTControllingSystem\\CMST\\Server\\DetectionSystem\\ReceivedData\\' #in our case the video's location


#this function runs the detection system on the given video (in the directories specified above)
def runDetectionSystem(file_name):

	try:
		os.system('activate tensorflow1 & cd ' + location_of_detection_program + ' & python ' + name_of_detection_program + ' ' + location_of_the_video + file_name)
		return True
	except:
		print('Problem Running Video ' + str(file_name) + 'on the detection system')
		return False
		
	
#Common variables (Classification)
location_of_classification_program = 'C:\\Users\\Administrator\\Desktop\\TurtleClassification'
name_of_classification_program = 'TestCNN.py'
location_of_the_image = 'C:\\New Project\\Detected\\Cropped\\'
	
#This function runs the classification system on the given image (in the directories specified above)
def runClassificationSystem(file_name):
	#write the address to the file 
	F = open(location_of_classification_program + "\\TestImageAddress.txt","w") 
	F.write(location_of_the_image + file_name)
	F.close()

	try:
		os.system('activate MATLAB & cd ' + location_of_classification_program + ' & python ' + name_of_classification_program)
		return True
	except:
		print('Problem Running image ' + str(file_name) + 'on the classification system')
		return False



#this function return list of files in directory (will be used to get the files detected and feed it to the classification system)
def listOfFilesInDirectory(directory):
	list_of_files = []
	try:
		list_of_files = os.listdir(directory)
		return list_of_files
	except:
		print('No Such file or Directory Error for : ' + directory)
		return list_of_files


#this function returns list of names without the extension (will be used to get the frame id in that video, as we identify the name by the frame number)
def listOfNamesWithoutExtension(list_of_data):
	list_of_files_names = [] #list of files names without the extension
	for x in list_of_files:
		list_of_files_names.append(x.split('.')[0])	

	return list_of_files_names

'''

def copyReceivedVideosToDetection():
	itemlist = []
    try :
        with open ('ReceivedDataMetaData.txt', 'rb') as fp:
            itemlist = pickle.load(fp)
            data['listOfReceivedVideos'] = itemlist
    except:
            print("Nothing in the file")
			
	for x in itemlist:
		try :
			os.system('copy missionID' + str(x) + '.mp4 C:\tensorflow1\models\research\object_detection\missionID' + str(x) + '.mp4')
			print('Copied' + str(x))
		except:
			print('Couldnt Copy' + str(x))



copyReceivedVideosToDetection()

'''


import os


'''
#detection
location_of_detection_program = 'C:\\tensorflow1\\models\\research\\object_detection'
name_of_detection_program = 'Object_detection_video.py'
location_of_the_data = 'C:\\Users\\Administrator\\Desktop\\CMSTControllingSystem\\CMST\\Server\\DetectionSystem\\ReceivedData\\' #in our case the video's location
data_file_name = 'missionID1.mp4' #name of the video
os.system('activate tensorflow1 & cd ' + location_of_detection_program + ' & python ' + name_of_detection_program + ' ' + location_of_the_data + data_file_name)


#classification
location_of_classification_program = 'C:\\Users\\Administrator\\Desktop\\TurtleClassification'
name_of_classification_program = 'TestCNN.py'

data_file_name2 = '1.jpg' #cropped image file name 

#write the address to the file 
F = open("C:\\Users\\Administrator\\Desktop\\TurtleClassification\\TestImageAddress.txt","w") 
F.write('C:\\New Project\\Detected\\Cropped\\' + data_file_name2)
F.close()


os.system('activate MATLAB & cd ' + location_of_classification_program + ' & python ' + name_of_classification_program)



'''


list_of_files = os.listdir('C:\\New Project\\Detected\\Cropped')
print(list_of_files)

list_of_files_names = [] #list of files names without the extension
for x in list_of_files:
    list_of_files_names.append(x.split('.')[0])
print(list_of_files_names)

#list_of_files = [str(x) for x in list_of_files x.split('.')[0] == is.digit()]
