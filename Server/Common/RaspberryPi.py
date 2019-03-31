class RaspberryPi:
    def __init__(self):
        self.SerialNumber = ""
        self.IP = ""

    #set the serial number of the Raspberry pi
    def setSerialNumber(self, serialNumber):
        self.SerialNumber = serialNumber

    #set the IP of the RaspberryPi
    def setIP(self, ip):
        self.IP = ip

    #get the Serial Number of the RaspberryPi
    def getSerialNumber(self):
        return self.SerialNumber

    #get the IP of the RaspberryPi
    def getIP(self):
        return self.IP
