def get_pi_temperature():
    tempfile = open("/sys/bus/w1/devices/28-001451eba1ff/w1_slave")
    thetext = tempfile.read()
    tempfile.close()
    tempdata = thetext.split("\n")[1].split(" ")[9]
    temperature = float(tempdata[2:])
    temperature = temperature / 1000
    return temperature
