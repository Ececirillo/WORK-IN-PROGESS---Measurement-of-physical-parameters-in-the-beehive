import time
from machine import I2C, Pin

#I2C Confuguration
i2c = I2C(0, scl=Pin(17), sda=Pin(16))
SHT40_ADDR = 0x44

def leggi_sensore():
    try:
        i2c.writeto(SHT40_ADDR, b'\xfd')
        time.sleep_ms(10)
        
        #read
        data = i2c.readfrom(SHT40_ADDR, 6)
        
        #temp
        t_raw = data[0] << 8 | data[1]
        temp = -45 + 175 * t_raw / 65535.0
        
        #hum
        h_raw = data[3] << 8 | data[4]
        hum = -6 + 125 * h_raw / 65535.0
        
        return round(temp, 2), round(hum, 2)
    except Exception as e:
        print("Errore di comunicazione con l'SHT40:", e)
        return None, None

# 2 sec cycle
while True:
    t, h = leggi_sensore()
    if t is not None and h is not None:
        print(f"Temperatura: {t} °C  |  Umidità: {h} %")
    else:
        print("Impossibile leggere i dati dal sensore.")
    
    time.sleep(2)
