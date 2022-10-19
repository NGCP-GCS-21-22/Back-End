
import random
import time
import sys
from paho.mqtt import client as mqtt_client
from pynput import keyboard
from pynput.keyboard import Listener



#broker = "local-ip"
broker =  "broker.emqx.io"
port = 1883
topic = "python/mqtt"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
#Configure the local broker with this credential
username = 'test_user'
password = "test_password"

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    msg_count = 0
    while True:
        #Will go thru a mode of listening to Key presses
        if(sys.argv[1] == '0'):
            def on_press(key):
                key_result = format("Key Pressed: {0}".format(key))
                print(key_result)
                client.publish(topic, key_result)

            def on_release(key):
                print("Key Pressed: ".format(key))

                #Stop the Program with ESC
                if key == keyboard.Key.esc:
                    return False
            with Listener(on_press=on_press, on_release=on_release) as listener:
                listener.join()
        #Will go thru a mode of looping message counts
        elif(sys.argv[1] == '1'):
            time.sleep(1)
            msg = f"messages: {msg_count}"
            result = client.publish(topic, msg)
            status = result[0]
            if status == 0:
                print(f"Send {msg} to topic {topic}")
            else:
                print(f"Failed to send message to topic {topic}")
            msg_count += 1


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()