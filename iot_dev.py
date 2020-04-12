import os
import asyncio
from azure.iot.device.aio import IoTHubDeviceClient
import config

async def main():
    # Fetch the connection string from an enviornment variable
    conn_str = config.device_connect

    # Create instance of the device client using the authentication provider
    device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

    # Connect the device client.
    await device_client.connect()

    # Send a single message
    print("Sending message...")
    await device_client.send_message("This is a message that is being sent")
    print("Message successfully sent!")

    # finally, disconnect
    await device_client.disconnect()


asyncio.run(main())