import time
# import RPi.GPIO as GPIO
from tb_device_mqtt import TBDeviceMqttClient

import json


THINGSBOARD_HOST = 'thingsboard.cloud'
ACCESS_TOKEN = '3atyg8kyEx7XctrvhfxDMVLD'


# We assume that all GPIOs are LOW
gpio_state = {7: False, 11: False, 12: False, 13: False, 15: False, 16: False, 18: False, 22: False, 29: False,
              31: False, 32: False, 33: False, 35: False, 36: False, 37: False, 38: False, 40: False}


def get_gpio_status():
    # Encode GPIOs state to json
    return json.dumps(gpio_state)

def set_gpio_status(pin, status):
    # Output GPIOs state
    # GPIO.output(pin, GPIO.HIGH if status else GPIO.LOW)
    print(f"changing gpio {pin} to {status}")
    # Update GPIOs state
    gpio_state[pin] = status
    
    

# dependently of request method we send different data back
my_client = None
def on_server_side_rpc_request(request_id, request_body):
    global my_client
    print(request_id, request_body)
    
    if request_body['method'] == 'getGpioStatus':
        # Reply with GPIO status
        my_client.send_rpc_reply(request_id, get_gpio_status())
        pass
    elif request_body['method'] == 'setGpioStatus':
        # Update GPIO status and reply
        set_gpio_status(request_body['params']['pin'], request_body['params']['enabled'])
        my_client.send_rpc_reply(request_id, get_gpio_status())
        pass
    
    
# Using board GPIO layout
# GPIO.setmode(GPIO.BOARD)
# for pin in gpio_state:
#     # Set output mode for all GPIO pins
#     GPIO.setup(pin, GPIO.OUT)

client = TBDeviceMqttClient(host=THINGSBOARD_HOST, username=ACCESS_TOKEN)
my_client = client
client.set_server_side_rpc_request_handler(on_server_side_rpc_request)
client.connect()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    # GPIO.cleanup()
    pass


    
    