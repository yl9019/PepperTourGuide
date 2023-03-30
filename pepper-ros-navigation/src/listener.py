#!/usr/bin/env python
import rospy
import time
from naoqi import ALProxy
from std_msgs.msg import String
from PIL import Image, ImageDraw, ImageFont
from animation_provider import process_keywords
IP = "192.168.0.102"

tts = ALProxy("ALAnimatedSpeech", IP, 9559)
leds=ALProxy("ALLeds",IP,9559)

tablet_service = ALProxy("ALTabletService", IP, 9559)

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)
    pk = process_keywords(data.data)
    print("------------------------------key word---------------------------------")
    print(pk)
    tts.say(pk)

    # display(data.data)
    
def led_callback(data):
    leds.fadeRGB("FaceLeds",data.data,1)



def listener():
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber('speak', String, callback)
    rospy.Subscriber('leds', String, led_callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()



# def display(str):
#     text = str
#     font = ImageFont.truetype("arial.ttf", 36)

#     image = Image.new('RGB', (200, 100), color = (255, 255, 255))

#     draw = ImageDraw.Draw(image)
#     text_size = draw.textsize(text, font)
#     text_position = ((200 - text_size[0]) / 2, (100 - text_size[1]) / 2)
#     draw.text(text_position, text, fill=(0, 0, 0), font=font)

#     image.save('output.png')

#     image_path = 'output.png'
#     tablet_service.showImage(image_path)

#     time.sleep(5)

#     tablet_service.hideImage()

if __name__ == '__main__':
    listener()

