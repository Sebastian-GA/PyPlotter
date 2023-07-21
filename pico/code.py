from machine import ADC, Pin
from utime import sleep

num_samples = 500
factor_16 = 3.3 / (65535)

def main():
    adc_signal = ADC(26)
    adc_gnd_ref = ADC(27)
    
    # See page 17 on datasheet
    tp4 = Pin(23, Pin.OUT)
    tp4.high()
    
    while True:
        sum_volt = 0
        sum_gnd = 0
        for _ in range(num_samples):
            sum_volt += adc_signal.read_u16()
            sum_gnd += adc_gnd_ref.read_u16()
            sleep(0.001)
        volt_signal = sum_volt * factor_16 / num_samples
        volt_gnd = sum_gnd * factor_16 / num_samples
        
        print("Raw: " + str(volt_signal))
        print("Gnd: " + str(volt_gnd))
        print("R-G: " + str(volt_signal - volt_gnd))
        # Temp
        m = 35.87463795
        y = -0.406507984
        temp = volt_signal * m + y
        print("Temp: " + str(temp))
        print("----")
        sleep(0.2)
        
if __name__ == '__main__':
    main()
