# Base code to connect to a bluetooth device and read data (Xiaomi Mijia LYWSD03MMC)
# thanks to https://github.com/JsBergbau/MiTemperature2
# and http://ianharvey.github.io/bluepy-doc/index.html

from bluepy import btle


# prepare bluetooth connection and setting
def btle_connect(address):
    
    # connect with bluetooth
    p = btle.Peripheral(deviceAddr=address)
    
    # adjust settings
    val = b'\x01\x00'
    p.writeCharacteristic(0x0038, val, True) #enable notifications of Temperature, Humidity and Battery voltage
    p.writeCharacteristic(0x0046, b'\xf4\x01\x00', True)

    # set delegate object to call
    p.withDelegate(MyDelegate("abc"))
    
    return p


class MyDelegate(btle.DefaultDelegate):
    def __init__(self, params):
        
        btle.DefaultDelegate.__init__(self)
        
        # ... initialise here
        self.temperature  = None
        self.humidity     = None
        self.batt_vol     = None
        self.batt_percent = None

        
        
    def handleNotification(self, cHandle, data):   
        # ... perhaps check cHandle
        # ... process 'data'
#         print(f'RAW BYTES           : {data}')
#         print(f'RAW BYTES - TEMP    : {data[0:2]}')
#         print(f'RAW BYTES - HUMIDITY: {data[2:3]}')
#         print(f'RAW BYTES - BATTERY : {data[3:5]}')
        
        self.temperature  = int.from_bytes(data[0:2],byteorder='little',signed=True)/100
        self.humidity     = int.from_bytes(data[2:3],byteorder='little')
        self.batt_vol     = int.from_bytes(data[3:5],byteorder='little')/1000
        # cap battery % to 100 when voltage > 3 -- 0 when battery = 2.1
        self.batt_percent = min(int(round((self.batt_vol - 2.1), 2) * 100), 100)
        
#         print(f'Temperature    : {self.temperature}')
#         print(f'Humidity       : {self.humidity}')
#         print(f'Battery Voltage: {self.batt_vol}')
#         print(f'Battery Ramain : {self.batt_percent}')
