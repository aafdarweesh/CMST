#C:\tensorflow1\models\research\object_detection
#"./ReceivedData/videoTemp.txt", "./ReceivedData/" + videoName + ".mp4"

import pickle
import os


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