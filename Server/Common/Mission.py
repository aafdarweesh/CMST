import sys
sys.path.append('../Common/')


import DroneConfigurations
import User

class Mission :
	def __init__(self, drone, user):
		self.MissionTime =  ""
		self.DroneConfigurations = drone
		self.userID = user.getID()

	#set the mission start time
	def setMissionStartTime(self, startTime):
		self.MissionTime = startTime

	#get the mission start time
	def getMissionStartTime(self):
		return self.MissionTime
