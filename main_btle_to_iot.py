import asyncio
from azure.iot.device.aio import IoTHubDeviceClient

import time
import json 
import datetime 

import config
from base_btle import btle_connect



# get list of bluetooth devices
btle_devices = config.btle_devices


# prepare payload
def get_payload(device_name, temperature, humidity):
    timestamp   = datetime.datetime.now()
    timestamp   = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    device_name = device_name
    temperature = temperature
    humidity    = humidity
    payload     = {'timestamp'   : timestamp,
                   'device_name' : device_name,
                   'temperature' : temperature,
                   'humidity'    : humidity
                  }
    return json.dumps(payload)


# send telemetry from a device to IoT Hub
async def btle_telemetry(device_name):
    
    # connect and prepared device
    dev     = btle_connect(btle_devices[device_name])
    
    # read data if notification received
    if dev.waitForNotifications(120):
        # Get payload
        payload = get_payload(device_name, dev.delegate.temperature, dev.delegate.humidity)
        # print(payload) 

        # Fetch the connection string from an enviornment variable
        conn_str = config.device_connect

        # Create instance of the device client using the authentication provider
        device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)
    
        # Connect the device client.
        await device_client.connect()

        # Send a single message
        print(f"Sending message from {device_name} ...")
        # await device_client.send_message("This is a message that is being sent: " + payload)
        await device_client.send_message(payload)
        print("Message successfully sent!")

        # finally, disconnect
        await device_client.disconnect()

    # disconnect
    dev.disconnect()

    # make sure disconnection is completed
    time.sleep(10)


# loop to send telemetry from all devices
for device_name in btle_devices:
    try:
        asyncio.run(btle_telemetry(device_name))
    except:
        continue
