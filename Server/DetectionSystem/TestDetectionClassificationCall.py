
import pickle
import os
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
