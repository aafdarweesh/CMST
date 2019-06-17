# CMST

Coastal Monitoring for Sea Turtles 

## What is CMST ?

A drone-based coastline monitoring system for
sea turtle detection and species classification.
The system includes an autonomous drone with a
high-resolution camera mounted on it. The drone
has real time communication with a cloud system
to store and analyze the data. Finally, the end
user of the system will be notified with the results
in real-time.


Check system Demo :
<iframe width="560" height="315" src="https://www.youtube.com/embed/MNfx6OTe8CU" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

```
https://www.youtube.com/watch?v=MNfx6OTe8CU&t
```


### Main system Components 
In our system, we have Server (which contains the Detection and Classification algorithms, Server Controller, and Detection System Controller):


Server Controller:


It is responsible for assigning new mission, communication with Raspberry pi, communication with UI, and Database.


Detection Controller:


It is responsible for reciving mission data from the Pi (videos or images), run the detection and classification algrithms on the received data, and finally store the results in storage system. The main objective is the synchronization in all process between these systems.


Detection Program:


It takes the video received, divide it into frames, run the detection algorithm, and finally gives detected images results and cropped images of the detected objects.


Classification Program:


It is responsible for classfying the detected objects into trained classes (in our case: Green sea turtle, and Loggerhead sea turtle).



### Hardware components

Server, Raspberry Pi, RPi camera, Drone Controller , The following links help you get familiar with Pi applications:
```
PiCamera Python Documentation :
https://picamera.readthedocs.io/en/release-1.13/recipes1.html

Camera connections :
Raspberry Pi 3 (Camera v2)
https://www.raspberrypi.org/documentation/hardware/camera/
https://www.youtube.com/watch?v=WoIIYiZPmLM
https://www.youtube.com/watch?v=MmcBcOFGWd0
https://www.youtube.com/watch?v=F44R5PaV25M
https://www.youtube.com/watch?v=N6f3_DOcG78

External Cameras :
https://www.youtube.com/watch?v=qMDDPlWbY2Q
https://www.youtube.com/watch?v=Jglsk4bH3eo
https://www.e-consystems.com/4k-usb-camera.asp

Thermal camera :
https://www.instructables.com/id/Thermal-Camera-AMG833-Raspberry-Pi/

Raspberry Pi camera streaming via WIFI :
https://www.youtube.com/watch?v=QVc_Cn6bZ7M
https://randomnerdtutorials.com/video-streaming-with-raspberry-pi-camera/
https://elinux.org/RPi-Cam-Web-Interface

Webcam Raspberry pi streaming via WIFI :
https://www.raspberrypi.org/documentation/usage/webcams/
https://www.youtube.com/watch?v=BeyBu-Mzeq4
https://www.youtube.com/watch?v=oIUHw0VChEU

Communicating with Raspberry Pi (and pixhawk) via MAVLink :
http://ardupilot.org/dev/docs/raspberry-pi-via-mavlink.html
https://www.youtube.com/watch?v=cZVNndOaYCE
https://www.youtube.com/watch?v=DGAB34fJQFc
```
Incase you would like to use PowerBank, the following link can be used to estimate the endurance time:
```
https://spellfoundry.com/raspberry-pi-battery-runtime-calculator/
```

### Run the program on boot (for the Raspberry pi or the server systems)
The following links show you how to run programs on boot in linux system:
```
https://en.wikipedia.org/wiki/Cron
https://askubuntu.com/questions/419548/how-to-set-up-a-root-cron-job-properly
https://www.raspberrypi.org/documentation/linux/usage/rc-local.md
```



### Drone Construction details
Please check the following link for the Drone construction and testing details
```
https://drive.google.com/open?id=1zR54pWELpCh46SZbTjuFEVBrV7V4D-1t
```


### Detection Program Documentation and Installation 
Please check the following link for the Detection Program Documentation (How to install it, where to provide the dataset, how to train your model for detection, and finally how to run it):
```
https://github.com/MuBadawy/Tensorflow-based-SeaTurtle-Detection
```


### Classification Program Documentation and Installation 
Please check the following link for the Classification Program Documentation (How to install it, where to provide the dataset, how to train your model for classification, and finally how to run it):
```
https://drive.google.com/open?id=1UvaFrQvBPWi75JcrgXSkxyPTLsiFvjHX
```


### Storage system (DB)
The database was implemented using MySQL. A dump of the database is at the DB folder. Note that the schema has some features that we didn't use like operator's profiles and areas. The schema can be briefly described as follows:

**Operator** ( username , password, fname, lname, e-mail, address)

  Alternate key:
  
  - e-mail
    
**Mission** ( missionID , username (fk: Operator.username) , droneID (fk: Drone. droneID) , pathID
(fk: Path.pathID) , starting time stamp, ending time stamp, video length, number of
videos, state)

  Alternate keys:
  
  - username, starting timestamp
  
  - username, ending timestamp
  
  - droneID, starting timestamp
  
  - droneID, ending timestamp
  
  Note: state is 0 when a mission is ready, 1 when it's running, and 2 when it's finished.
  
**Drone** ( droneID , specifications)

**Path** ( pathID , areaID ( fk : Area.areaID) , number of steps)

**Path Steps** ( pathID ( fk : Path.pathID) , step number , latitude, longitude)

**Area** ( areaID , country, city, name of area)

**Object Kind** ( object name , property1, property2)

**Is found in** ( areaID ( fk : Area.areaID) , object name (fk: Object Kind.object name) )

**Video** ( video url , missionID (fk: Mission.missionID) , video name, starting time, latitude,
longitude)

  Alternate key:
  
  - missionID, starting timestamp
    
  Note: starting time is relative to the start of the mission (we use seconds in our implementation).
  
**Sighting** ( sighting url , video url (fk: Video.video url) , time of appearance, number of
objects)

  Alternate key:
  
  - Video url, time of appearance
    
  Note: Time of appearance is the number of seconds from the start of the video until this sighting.
  
**Detected Object** ( sighting url (fk: sighting.sighting url) , object number , property1 value,
property2 value, object name (fk: Object Kind.object name), accuracy (i.e. confidence) , url)

### UI
PHP is used for the backend, while Javascript, HTML, and CSS are used for the front end. The layout for the notification was obtained from https://www.jqueryscript.net/other/Simple-Yet-Fully-Customizable-jQuery-Notification-Plugin-notify.html. The instructions for running the UI are as follows:

1. Launch the database schema on a MySQL server.
2. Install Xampp.
3. Inside the Xampp folder, go to the htdocs folder, delete everything and place the folder Turtles in there.
4. Inside Turtles, open resources/db.php and enter the database connection credentials appropriately.
5. In order to use the Javascript Google Maps API, you will need to obtain a key from Google. Once you have the key, go to each of the following files: findingsMap.php frame.php newPath.php resultsByMission.php, and insert your key in the links inside the statements where Google Maps is imported.
6. Open resources/constants.php and specify the max flight time of the drone (in seconds), and the length of each transmitted video (this is, of course, originally decided by the communication system).
7. In newMission.php, set the limits for the height and speed of the drone by changing the min and max attributes of the height and speed fields in the form.
8. In newPath.php, at line 176, replace SERVER_ADRRESS:PORT with the address and port number on which new missions are received at the server side.
9. Launch the Apache server from Xampp's control.



### Server Controller 
This system is responsible for the communication between the UI, storage system,
detection system, and the drone Raspberry pi systems. The end user can assign new mission
to one of the registered drones in the system, as illustrated in Figure 6.7, through the CMST UI.
Moreover, the system store the mission details to the Database. To ensure the security
between the Raspberry pi system and the Server Controller, the serial number (can be
replaced with encryption key) of the pi is used to verify the identity upon each request
between the drone Raspberry pi system and the server. Upon starting the mission,
synchronized communication between the Raspberry pi and the detection system is initiated.
Moreover, it is responsible for storing the data received from the Raspberry pi systems to the
storage, and invoking the detection system.


You can find the Server Main Controller in the following directory 
```
Server\MainServer\MainServer.py
```

The Server is Flask based server, main libraries to import :
```
#Flask server dependencies
from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_cors import CORS, cross_origin


import os #Operating system library 
import urllib #HTTP requests
from time import sleep #sleep 
import glob
import json #parse json data
import sys #run system commands 
import requests #send HTTP requests
import uu #incode and decode data (used to transmit the video and image)
import pickle #store json file into file, and extract it (also for dictionaries)
import subprocess #run another program in the background
import mysql.connector #connect to the DB
from datetime import datetime #check the current time 
from shutil import copyfile #copy files

```
To Run the Main server you write the following command 
```
python MainServer.py
```
(Make sure that MainServer Port is different from other programs ports 'in this case 5000'):
```
app.run(host='0.0.0.0', debug=True, port=5000)
```

### Detection System
The system is responsible for analysing the data sent by the Raspberry pi system (for each
mission, separately, in parallel), then sends the results to the storage system. On one hand, the
system runs the trained detection model (it analyses the video) and store only the detected
frames, and then crop the detected objects in those frames. On the other hand, the system
takes the detected objects and runs the classification model, which is responsible for
classifying the detected turtle into Green sea turtle or Loggerhead sea turtle, with the
classification accuracy for that object. The system eliminates the extra frames in the same
region (it calculates the region according to the speed of the drone, height of the drone, and
the field of view -calculated in Variables to be considered section).


The system capture the specified data (image, video), according to the mission duration,
then save it locally on the Raspberry pi. Upon the acknowledgement from the server the
system deletes the received images or videos, and send the following one in order. The
acknowledgement mechanism insures that Raspberry pi system and the server are
synchronized.

You can find the Server Main Controller in the following directory 
```
Server\DetectionSystem\DetectionSystem.py
```

The Server is Flask based server, main libraries to import :
```
#Flask server dependencies
from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_cors import CORS, cross_origin


import os #Operating system library 
import urllib #HTTP requests
from time import sleep #sleep 
import glob
import json #parse json data
import sys #run system commands 
import requests #send HTTP requests
import uu #incode and decode data (used to transmit the video and image)
import pickle #store json file into file, and extract it (also for dictionaries)
import subprocess #run another program in the background
import mysql.connector #connect to the DB
from datetime import datetime #check the current time 
from shutil import copyfile #copy files

```
To Run the Main server you write the following command 
```
python DetectionSystem.py
```
(Make sure that Detection Port is different from other programs ports 'in this case 5000'):
```
app.run(host='0.0.0.0', debug=True, port=5000)
```

Note that in this case MainServer.py and DetectionSystem.py ports are the same (will cause an error). Solution 
```
Change the Port number for one of them (recommended).

Add the codes of MainServer.py into DetectionSystem.py and run it only (Merging both)
```

CommunicationWithDetectionClassificationStorage.py program should be in the same directory as DetectionSystem.py as it will be invoked by it. 

### Raspberry Pi system
RPi Main Controller : The program is working as orchestrate of the RPi. It
communicates regularly with the Server (before receiving, during, and after the
mission). The program invoke other dedicated programs for these tasks (Its main
function is retrieving data from the server and fed the required information to the
dedicated programs). The program allows only one mission at a time. The invocation
function and retrieving data was tested.

RPi Server Transmission : The program is responsible for the communication with the
Server (Main controller, and detection system). The program updates the status of the
system with the Main server (location, number of videos generated, missionID, pi serial
140number). Moreover, it checks the generated videos, convert them into format that is
recognizable by the server, and then transmitted to the detection system. Upon
updating the status with the main server the program deletes the local version of the
data (to utilize the limited memory of the pi). Finally after the completion of the
mission, it prepares the system for receiving new mission (deletes related mission
details, as it uses it for failing scenarios to re transmit data and overcome other
scenarios).

Recording system : the program is responsible for recording the videos (as specified),
and meta data of the videos (starting time, location of the video, size of the video, and
ending time). The system was tested and it works in the backend during the
transmission, however we noticed that when you have frequent videos (short sizes) it
tends to lose some frames, as the switch between storing one video to start recording
the following one cause lose of couple of frames.


You can find the subprograms inside the following directory :
```
RaspberryPi
```

The main program that Control the flow inside the Raspberry pi is :
```
RPiClient-based.py
```


Its dependencies :
```
import requests
from time import sleep
import pickle # to store and retrieve dictionaries from files
import json
import os

```


To run it (make sure that all other programs are in the same directory, and videoBuffer folder is created):
```
python RPiClient-based.py
```

The program checks new mission from the server, and run only once (so you can assign it on boot, and whenever you boot the system, it will start automatically looking for new mission, and once it gets one, will complete it "while optimizing the local space").


The other subsystems :
```
ConfirmReceivingMission.py #confirm starting mission with the server, and the ending time as well
ServerTransmission.py #Alawys update the status of the RPi with the server, and transmit new collected data
StartRecording.py #Records the data and store it in the videoBuffer directory
```


### General Guidelines
Before each function (method) written There are comments that show the functionality, data received and returned, and referenced that were used to build the function.

The following link contains detailed report about the system. Check it out ;)
```
https://drive.google.com/open?id=1Unnv-ZMP0wXCVVDK97MjShFYoyieVPIg
```


## Authors

* **Ahmed DARWISH** - *Computer Engineering Group* - [Ahmed DARWISH](https://www.linkedin.com/in/ahmed-darwish-4a673565/)
* **Khaled ELDOWA** - *Computer Engineering Group* - [Khaled ELDOWA](https://gitlab.com/Khaled-Eldowa)
* **Furkan Gokturk OZTIRYAKI** - *Aerospace Engineering Group* - [Furkan Gokturk OZTIRYAKI](https://www.linkedin.com/in/furkan-%C3%B6ztiryaki-b56814182/)
* **Saif Ul HASSAN** - *Aerospace Engineering Group* - [Saif Ul HASSAN](https://www.linkedin.com/in/saif-hassan-992bb012b)
* **Mohamed BADAWY** - *Electrical and Electronics Engineering Group* - [Mohamed BADAWY](https://www.linkedin.com/in/mohamed-badawy-10a472133/)
* **Zafer ATTAL** - *Electrical and Electronics Engineering Group* - [Zafer ATTAL](https://www.linkedin.com/in/zafer-attal-651446162/)

## Acknowledgments
This work is sponsored by Cyprus Wildlife Research Institute (CWRI). Our project team would like to acknowledge CWRI for supporting us to buy the hardware components required in the project. We also would like to thank Chantal Kohl and Stefanie Kramer from Humboldt University for supplying us some sea turtle images and videos for experimentation in our project
