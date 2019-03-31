import sys
sys.path.append('../Common/')

import json

import DroneConfigurations
import User

class Mission :
	def __init__(self, drone, user, missionID):
		self.MissionTime =  ""
		self.DroneConfigurations = drone
		self.UserID = user.getID()
		self.MissionID =  missionID
		self.EstimatedMissionDuration = 0

	#set the mission start time
	def setMissionStartTime(self, startTime):
		self.MissionTime = startTime

	#set estimated mission duration
	def setEstimatedMissionDuration(self, duration):
		self.EstimatedMissionDuration = duration

	#get mission id
	def getMissionID(self):
		return self.MissionID

	#get the mission start time
	def getMissionStartTime(self):
		return self.MissionTime

	#get estimated mission duration
	def getEstimatedMissionDuration(self):
		return self.EstimatedMissionDuration
