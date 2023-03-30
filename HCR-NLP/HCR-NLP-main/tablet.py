import rospy
import time
from naoqi import ALProxy
from std_msgs.msg import String
from PIL import Image, ImageDraw, ImageFont

IP = "192.168.43.68"

# tts = ALProxy("ALTextToSpeech", IP, 9559)

tablet_service = ALProxy("ALTabletService", IP, 9559)

# def callback(data):
#     rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)
#     tts.say(data.data)
# def listener():
#     rospy.init_node('listener', anonymous=True)

#     rospy.Subscriber('speak', String, callback)

#     # spin() simply keeps python from exiting until this node is stopped
#     rospy.spin()

# if __name__ == '__main__':
#     listener()


# Define the string and font

def display(str):
    text = str
    font = ImageFont.truetype("arial.ttf", 36)

    image = Image.new('RGB', (200, 100), color = (255, 255, 255))

    draw = ImageDraw.Draw(image)
    text_size = draw.textsize(text, font)
    text_position = ((200 - text_size[0]) / 2, (100 - text_size[1]) / 2)
    draw.text(text_position, text, fill=(0, 0, 0), font=font)

    image.save('output.png')

    image_path = 'output.png'
    tablet_service.showImage(image_path)

    time.sleep(5)

    tablet_service.hideImage()
