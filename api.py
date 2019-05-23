from flask import Flask, render_template, url_for
from flask_cors import CORS
from threading import Timer
import temperature as temp
from datetime import datetime
import os
import atexit


app = Flask(__name__)
CORS(app)


class DualValueFixedLengthLinkedList:
    def __init__(self, maxLength):
        self.maxLength = maxLength
        self.head = None
        self.tail = None
        self.currentLength = 0

    def add(self, node):
        if (self.currentLength == 0):
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = node

        self.currentLength += 1

        if (self.currentLength > self.maxLength):
            self.removeHead()

    def removeHead(self):
        self.head = self.head.next
        self.currentLength -= 1

        if (self.head == None):
            self.tail = None

    def asCsv(self):
        current = self.head

        output = "Time,Temperature\n"

        while (current != None):
            output += str(current.value1) + "," + str(current.value2) + "\n"
            current = current.next

        return output

    def dumpToFile(self, filename):
        f = open(filename, "w")

        f.write(self.asCsv())

        f.close()


class DualValueNode:
    def __init__(self, value1, value2):
        self.value1 = value1
        self.value2 = value2
        self.next = None


data = DualValueFixedLengthLinkedList(12 * 60) # Will record every minute, so hold 12 hours of data

t = None

def recordPeriodicTemperature():
    currentTemp = temp.get_pi_temperature()
    currentTime = datetime.now().replace(microsecond=0)

    data.add(DualValueNode(currentTime, currentTemp))

    t = Timer(60, recordPeriodicTemperature)
    t.start()


@app.route("/data")
def getData():
    return data.asCsv()


def exitHandler():
    t.cancel()
    data.dumpToFile("cached.csv")


def preloadData(filename):
    f = open(filename)

    for (line in f.readlines()):
        if (line.startswith("Time,")):
            continue

        split_line = line.split(",")
        timestamp = split_line[0]
        temperature = split_line[1]

        data.add(DualValueNode(currentTime, currentTemp))

    f.close()


if __name__ == "__main__":
    atexit.register(exitHandler)
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')

    preloadData("cached.csv")
    recordPeriodicTemperature()

    app.run(host="0.0.0.0", port=8082, debug=True)
