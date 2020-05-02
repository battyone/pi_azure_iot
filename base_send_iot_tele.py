import os
import asyncio
from azure.iot.device.aio import IoTHubDeviceClient
import config

import json 
import datetime 

def get_payload():
    timestamp   = datetime.datetime.now()
    timestamp   = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    device_name = 'test'
    temperature = 99
    humidity    = 99
    payload     = {'timestamp'   : timestamp,
                   'device_name' : device_name,
                   'temperature' : temperature,
                   'humidity'    : humidity
                  }
    return json.dumps(payload)


async def main():
    # Get payload
    payload = get_payload()
    # print(payload)

    # Fetch the connection string from an enviornment variable
    conn_str = config.device_connect

    # Create instance of the device client using the authentication provider
    device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

    # Connect the device client.
    await device_client.connect()

    # Send a single message
    print("Sending message...")
    # await device_client.send_message("This is a message that is being sent: " + payload)
    await device_client.send_message(payload)
    print("Message successfully sent!")

    # finally, disconnect
    await device_client.disconnect()


asyncio.run(main())
