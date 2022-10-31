from bluepy.btle import Peripheral, UUID
from bluepy.btle import Scanner, DefaultDelegate
import time

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print("Discovered device", dev.addr)
        elif isNewData:
            print("Received new data from", dev.addr)

scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(10.0)
n=0
addr = []
for dev in devices:
    print("%d: Device %s (%s), RSSI=%d dB" % (n, dev.addr, dev.addrType, dev.rssi))
    addr.append(dev.addr)
    n += 1
    for (adtype, desc, value) in dev.getScanData():
        print(" %s = %s" % (desc, value))

number = input('Enter your device number: ')
print('Device', number)
num = int(number)
print(addr[num])
#
print("Connecting...")
dev = Peripheral(addr[num], 'random')
class MyDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
    def handleNotification(self, cHandle, data):
        hr = int.from_bytes(data, "big")
        print(f"Heart Rate: {hr}")

dev.setDelegate(MyDelegate())
print("Services...")
for svc in dev.services:
    print (str(svc))
#
try:
    heartrate = dev.getServiceByUUID(UUID(0x180D))
    button = dev.getServiceByUUID(UUID(0xA000))
    for ch in heartrate.getCharacteristics():
        print(str(ch))
    for ch in button.getCharacteristics():
        print(str(ch))
#
    hr = dev.getCharacteristics(uuid=UUID(0x2A37))[0]
    bt = dev.getCharacteristics(uuid=UUID(0xA001))[0]

    for descriptor in dev.getDescriptors(heartrate.hndStart, heartrate.hndEnd):
        if (descriptor.uuid == 0x2902):
            cccd = descriptor.handle
    dev.writeCharacteristic(cccd, bytes([1, 0]))
    print(f"CCCD is set to {dev.readCharacteristic(cccd)}.")
    while 1:
       dev.waitForNotifications(1)
       if bt.read() == bytes([1]):
           print("Button    : Pressed")
       else:
           print("Button    : Released")

finally:
    dev.disconnect()
