import sys
sys.path.append('../Common/')

import Mission
import DroneConfigurations
import User

#test User
print("User Test:")
user = User.User(1)

#before
print("Test Name : "" == " + user.getName())
print("Test Surname : "" == " + user.getSurname())
print("Test ID : 1 == " + str(user.getID()))

print("-----------------------------------------------------")

#after
user.setName("Name")
print("Test Name : Name == " + user.getName())
user.setSurname("Surname")
print("Test Surname : Surname == " + user.getSurname())
print("Test ID : 1 == " + str(user.getID()))

print("\n\n\n")

#test DroneConfigurations
print("DroneConfigurations Test:")
drone = DroneConfigurations.DroneConfigurations()

#before
print("Test Path : {} == " + str(drone.getPath()))
print("Test Speed : 3 == " + str(drone.getSpeed()))
print("Test Height : 10 == " + str(drone.getHeight()))

print("-----------------------------------------------------")

#after
drone.setPath({"a" : "a", "b" : "b"})
print("Test Path : {'a' : 'a', 'b' : 'b'} == " + str(drone.getPath()))
drone.setSpeed(5)
print("Test Speed : 5 == " + str(drone.getSpeed()))
drone.setHeight(11)
print("Test Height : 11 == " + str(drone.getHeight()))

print("\n\n\n")

#test Mission
print("Mission Test:")
mission = Mission.Mission(drone, user)

#before
print("Test MissionStartTime : "" == " + mission.getMissionStartTime())

print("-----------------------------------------------------")

#after
mission.setMissionStartTime('2019-03-20 23:05:24.310928')
print("Test MissionStartTime : 2019-03-20 23:05:24.310928 == " + mission.getMissionStartTime())

print("\n\n\n")
