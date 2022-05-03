import aliLink,mqttd,rpi
import time,json
import Adafruit_DHT
import time
import buzzer_1
import gas_sensor
import relay
from threading import Thread
pin = 19  	# DHT11 
Buzzer = 20    
# GPIO
sensor = Adafruit_DHT.DHT11
ProductKey = 'a11lzCDSgZP'
DeviceName = 'IU6aSETyiImFPSkpcywm'
DeviceSecret = "2551eb5f630c372743c538e9b87bfe6d"
ProductKey = 'a11lzCDSgZP'
DeviceName = 'IU6aSETyiImFPSkpcywm'
DeviceSecret = "2551eb5f630c372743c538e9b87bfe6d"
POST = '/sys/a11lzCDSgZP/IU6aSETyiImFPSkpcywm/thing/event/property/post'  
POST_REPLY = '/sys/a11lzCDSgZP/IU6aSETyiImFPSkpcywm/thing/event/property/post_reply'
SET = '/sys/a11lzCDSgZP/IU6aSETyiImFPSkpcywm/thing/service/property/set'  
# Message callback (callback function for sending messages from the cloud)
def on_message(client, userdata, msg):
    #print(msg.payload)
    Msg = json.loads(msg.payload)
#Connection callback (callback function after establishing a link with Aliyun)
def on_connect(client, userdata, flags, rc):
    pass
# Connection Information
Server,ClientId,userNmae,Password = aliLink.linkiot(DeviceName,ProductKey,DeviceSecret)
# mqtt connection
mqtt = mqttd.MQTT(Server,ClientId,userNmae,Password)
mqtt.subscribe(SET) 			# The subscriber delivers the message topic
mqtt.begin(on_message,on_connect)
# Obtain information and report system parameters every 2 seconds
while True:
    #Obtaining indicator Status
    power_stats=int(rpi.getLed())
    if(power_stats == 0):
        power_LED = 0
    else:
        power_LED = 1
    # CPU information
    CPU_temp = float(rpi.getCPUtemperature()) 
    CPU_usage = float(rpi.getCPUuse())       
    # RAM information
    RAM_stats =rpi.getRAMinfo()
    RAM_total =round(int(RAM_stats[0]) /1000,1)    
    RAM_used =round(int(RAM_stats[1]) /1000,1)
    RAM_free =round(int(RAM_stats[2]) /1000,1)
    # Disk imformation
    DISK_stats =rpi.getDiskSpace()
    DISK_total = float(DISK_stats[0][:-1])
    DISK_used = float(DISK_stats[1][:-1])
    DISK_perc = float(DISK_stats[3][:-1])
    #humidity， temperature
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    # Buzzer
    buzzer = 0
    # Smoke sensor
    gas = gas_sensor.gas()
    # Build a message structure consistent with the cloud model
    updateMsn = {
        'cpu_temperature':CPU_temp,
        'cpu_usage':CPU_usage,
        'RAM_total':RAM_total,
        'RAM_used':RAM_used,
        'RAM_free':RAM_free,
        'DISK_total':DISK_total,
        'DISK_used_space':DISK_used,
        'DISK_used_percentage':DISK_perc,
        'PowerLed':power_LED,
        'temperature':temperature,
        'humidity':humidity,
        'window':window,
        'LCD':LCD,
        'buzzer':buzzer,
        'gas':gas
    }
    JsonUpdataMsn = aliLink.Alink(updateMsn)
    print(JsonUpdataMsn)

    mqtt.push(POST,JsonUpdataMsn) # Regularly push Alink protocol data constructed by us to The IOT of Ali Cloud

    time.sleep(3)