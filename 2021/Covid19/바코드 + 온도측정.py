import board
import busio as io
import adafruit_mlx90614
from evdev import InputDevice, categorize, ecodes  
from time import sleep
import os
from gtts import gTTS



scancodes = {
    # Scancode: ASCIICode
    0: None, 1: u'ESC', 2: u'1', 3: u'2', 4: u'3', 5: u'4', 6: u'5', 7: u'6', 8: u'7', 9: u'8',
    10: u'9', 11: u'0', 12: u'-', 13: u'=', 14: u'BKSP', 15: u'TAB', 16: u'q', 17: u'w', 18: u'e', 19: u'r',
    20: u't', 21: u'y', 22: u'u', 23: u'i', 24: u'o', 25: u'p', 26: u'[', 27: u']', 28: u'CRLF', 29: u'LCTRL',
    30: u'a', 31: u's', 32: u'd', 33: u'f', 34: u'g', 35: u'h', 36: u'j', 37: u'k', 38: u'l', 39: u';',
    40: u'"', 41: u'`', 42: u'LSHFT', 43: u'\\', 44: u'z', 45: u'x', 46: u'c', 47: u'v', 48: u'b', 49: u'n',
    50: u'm', 51: u',', 52: u'.', 53: u'/', 54: u'RSHFT', 56: u'LALT', 57: u' ', 100: u'RALT'
}

capscodes = {
    0: None, 1: u'ESC', 2: u'!', 3: u'@', 4: u'#', 5: u'$', 6: u'%', 7: u'^', 8: u'&', 9: u'*',
    10: u'(', 11: u')', 12: u'_', 13: u'+', 14: u'BKSP', 15: u'TAB', 16: u'Q', 17: u'W', 18: u'E', 19: u'R',
    20: u'T', 21: u'Y', 22: u'U', 23: u'I', 24: u'O', 25: u'P', 26: u'{', 27: u'}', 28: u'CRLF', 29: u'LCTRL',
    30: u'A', 31: u'S', 32: u'D', 33: u'F', 34: u'G', 35: u'H', 36: u'J', 37: u'K', 38: u'L', 39: u':',
    40: u'\'', 41: u'~', 42: u'LSHFT', 43: u'|', 44: u'Z', 45: u'X', 46: u'C', 47: u'V', 48: u'B', 49: u'N',
    50: u'M', 51: u'<', 52: u'>', 53: u'?', 54: u'RSHFT', 56: u'LALT',  57: u' ', 100: u'RALT'
}

def ParseBarcode(devicePath):

    dev = InputDevice(devicePath)
    dev.grab() 

    x = ''
    caps = False
    for event in dev.read_loop():
        if event.type == ecodes.EV_KEY:
            data = categorize(event)  
            if data.scancode == 42:
                if data.keystate == 1:
                    caps = True
                if data.keystate == 0:
                    caps = False

            if data.keystate == 1: 
                if caps:
                    key_lookup = u'{}'.format(capscodes.get(data.scancode)) or u'UNKNOWN:[{}]'.format(data.scancode)  
                else:
                    key_lookup = u'{}'.format(scancodes.get(data.scancode)) or u'UNKNOWN:[{}]'.format(data.scancode)  


                if (data.scancode != 42) and (data.scancode != 28):
                    x += key_lookup

                if(data.scancode == 28):
                    new_barcode = True
                    print(x)
                    return(x)
        

def message():

    
    i2c = io.I2C(board.SCL,board.SDA, frequency=100000)
    mlx = adafruit_mlx90614.MLX90614(i2c)             
    ambientTemp = "{:.2f}".format(mlx.ambient_temperature)
    targetTemp = "{:.2f}".format(mlx.object_temperature + 5)
    print("주변 온도 : ", ambientTemp, " C")
    print("손목 온도: ", targetTemp, " C")
    tts = gTTS(
    text = (targetTemp +' 도'),
    lang = 'ko' , slow =False
    )
    tts.save('temp.mp3')
    if float(targetTemp) >= 30.0 and float(targetTemp) <= 37.5: #healthy:
        print("pass")
        os.system("mpg321 temp.mp3")
        os.system("mpg321 pass.mp3")
    else:
        print("failure")
        os.system("mpg321 temp.mp3")
        os.system("mpg321 nonpass.mp3")

if __name__ == "__main__":
    count = 0
    
    while True:
        print('b')
        
        barcode = ParseBarcode("/dev/input/event0")
        new_barcode = '8809' in barcode
        pyeongtaek = '8809706090825' in barcode
        damyang = '8809706090856' in barcode
        gwangju = '8809706090849' in barcode
        busan = '8809706090832' in barcode
        seoul = '8809706090818' in barcode
        print(new_barcode)
        if new_barcode == True :
            if pyeongtaek == True:
                os.system("mpg321 pyeongtaek.mp3")
                message()
            elif damyang == True:
                os.system("mpg321 damyang.mp3")
                message()
            elif gwangju == True:
                os.system("mpg321 gwangju.mp3")
                message()
            elif busan == True:
                os.system("mpg321 busan.mp3")
                message()
            elif seoul == True:
                os.system("mpg321 seoul.mp3")
                message()
                
        else :
            
            print("Retry")
            count = count + 1
            print(count)
            if count >= 5 :
                os.system("mpg321 nonpass.mp3")
                count = 0
            else:
                os.system("mpg321 retry.mp3")
        
else:
    print("임포트되어 사용됨")
    print(__name__)


        


