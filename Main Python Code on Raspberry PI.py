# MPU6050 9-DoF Example Printout

from mpu9250_i2c import *

time.sleep(1) # Necessary Delay required to settle the sensor

import time
import pyrebase
from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import time as t
import json


config = {
  "apiKey": "iSh9tO0dMR7siZe37cHuIInuROFWy3ZmbMqjaC5p",
  "authDomain": "androidhivefyp.firebaseapp.com",
  "databaseURL": "https://androidhivefyp-default-rtdb.firebaseio.com/",
  "storageBucket": "androidhivefyp.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()



#Define ENDPOINT, CLIENT_ID, PATH_TO_CERTIFICATE, PATH_TO_PRIVATE_KEY, PATH_TO_AMAZON_ROOT_CA_1, MESSAGE, TOPIC, and RANGE
ENDPOINT = "ah57gycwdcm4b-ats.iot.us-east-1.amazonaws.com"
CLIENT_ID = "testDevice"
PATH_TO_CERTIFICATE = "Certificate/04de948f53ffaed4e71e1f4f5549984c48d576c0eee982a699acffe7d589f709-certificate.pem.crt"
PATH_TO_PRIVATE_KEY = "Certificate/04de948f53ffaed4e71e1f4f5549984c48d576c0eee982a699acffe7d589f709-private.pem.key"
PATH_TO_AMAZON_ROOT_CA_1 = "Certificate/root.pem"
MESSAGE = "Sensor Data"
TOPIC = "test/testing"
RANGE = 20

print("recording data and sending to server")
print("----------------------------------------")
print()

# Spin up resources
event_loop_group = io.EventLoopGroup(1)
host_resolver = io.DefaultHostResolver(event_loop_group)
client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
mqtt_connection = mqtt_connection_builder.mtls_from_path(
            endpoint=ENDPOINT,
            cert_filepath=PATH_TO_CERTIFICATE,
            pri_key_filepath=PATH_TO_PRIVATE_KEY,
            client_bootstrap=client_bootstrap,
            ca_filepath=PATH_TO_AMAZON_ROOT_CA_1,
            client_id=CLIENT_ID,
            clean_session=False,
            keep_alive_secs=6
            )
print("Connecting to {} with client ID '{}'...".format(
        ENDPOINT, CLIENT_ID))
# Make the connect() call
connect_future = mqtt_connection.connect()
# Future.result() Waits for result availability
connect_future.result()
print("Connected!")
# Send the message to the server as many times as you'd like..
print('Begin Publish')

while 1:
    try:
        ax,ay,az,wx,wy,wz = mpu6050_conv() # reading and coverting the data
    except:
        continue
    
    print('{}'.format('-'*30))
    print('accel [g]: x = {0:2.2f}, y = {1:2.2f}, z {2:2.2f}= '.format(ax,ay,az))
    print('gyro [dps]:  x = {0:2.2f}, y = {1:2.2f}, z = {2:2.2f}'.format(wx,wy,wz))
    print('{}'.format('-'*30))
    data = {
    "ax": ax,
    "ay": ay,
    "az": az,
    "gx": wx,
    "gy": wy,
    "gz": wz,
    }
    #dataaws = "{} [{}]".format(MESSAGE, i+1)
    message = {"message" : data}
    mqtt_connection.publish(topic=TOPIC, payload=json.dumps(message), qos=mqtt.QoS.AT_LEAST_ONCE)
    print("Published: '" + json.dumps(message) + "' to the topic: " + "'test/testing'")

    db.child("9250").set(data)
    time.sleep(1)