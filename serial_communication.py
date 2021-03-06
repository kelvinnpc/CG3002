import serial
import time

ser = serial.Serial('/dev/ttyAMA0', 115200)

class serial_communication:
    def __init__(self):
        ready = self.handshake()
        while ready == False:
            print('no handshake')
            ready = self.handshake()
        while ready:
            global rcv
            global los
            data = self.readlineCR()
            if (data == '0'):
                print(rcv)
                los = len(rcv)
            if (data == '1'):
                print(rcv)
                if(los == int(rcv)):
                    print('size is correct')
                else :
                    print ('size is wrong')
                los = ""
            if (data == '2'):
                print('checksum is {}'.format(rcv))
                
                
   
    def handshake(self):
        ser.write('0'.encode())
        ack1 = ser.read().decode('ascii')
        if ack1 == '1':
            ser.write('1'.encode())
            print('handshake pass')
            return True
        else:
            print("\r\n\Handshake not completed!")
            return False
        

    def readlineCR(self):
        global rcv
        rcv = ""
        checksum = 0
        while True:
            ch = ser.read().decode('ascii')
            if(ch == 'd'):
                return '0'
            if(ch == 's'):
                return '1'
            if (ch == 'c'):
                return '2'
            rcv += ch
            
    
my_serial_communication = serial_communication()
