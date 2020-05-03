import asyncio
from azure.iot.device.aio import IoTHubDeviceClient

import time
import json 
import datetime 

import config
from base_btle import btle_connect


# prepare payload from a bluetooth device
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


# construct a dict of payloads from all devices
def get_payloads(btle_devices):
    payloads = dict()

    # loop to get payloads from all bluetooth devices
    for device_name in btle_devices:
        # print(device_name)

        try:
            # connect and prepared bluetooth device
            dev     = btle_connect(btle_devices[device_name])

            # read data if notification received
            if dev.waitForNotifications(120):
                # Get payload from this device
                payload = get_payload(device_name, dev.delegate.temperature, dev.delegate.humidity)
                # print(payload) 

                # append to payloads
                payloads.update({device_name: payload})
                # print(payloads)

            # disconnect bluetooth device
            dev.disconnect()

            # make sure disconnection is completed
            time.sleep(10)

        except:
            continue
    
    return payloads


# send telemetry from a device to IoT Hub
async def btle_telemetry(payloads):
    # Fetch the connection string from an enviornment variable
    conn_str = config.device_connect

    # Create instance of the device client using the authentication provider
    device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

    # Connect the device client.
    await device_client.connect()

    for device in payloads:
        # Send a single message
        print(f"Sending message from {device} ...")
        # await device_client.send_message("This is a message that is being sent: " + payload)
        await device_client.send_message(payloads[device])
        print("Message successfully sent!")

    # finally, disconnect
    await device_client.disconnect()


# get list of bluetooth devices
btle_devices = config.btle_devices

# get list of payloads
payloads = get_payloads(btle_devices)

# send payloads
asyncio.run(btle_telemetry(payloads))