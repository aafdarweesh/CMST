class DroneConfigurations:
    def __init__(self):
        self.Path =  {} #pinpoints on the map
        self.Height = 10 #m
        self.Speed = 3 #m/s

    #set the path of the drone
    def setPath(path):
        self.Path = path

    #set the height of the drone
    def setHeight(height):
        self.Height = height

    #set the speed of the drone
    def setSpeed(speed):
        self.Speed = speed

    #get the path of the drone
    def getPath():
        return self.Path

    #get the height of the drone
    def getHeight():
        return self.Height

    #get the speed of the drone
    def getSpeed():
        return self.Speed
