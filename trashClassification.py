# ------------------------------------------------------------------------
# Trash Classifier ML Project
# Please review ReadMe for instructions on how to build and run the program
#
# (c) 2020 by Jen Fox, Microsoft
# MIT License
# --------------------------------------------------------------------------
from Motor import Motor

#import Pi GPIO library button class
from gpiozero import Button, LED, PWMLED
from picamera import PiCamera
from time import sleep

from lobe import ImageModel
import time
import dbconfig

#Create input, output, and camera objects
button = Button(2)

yellow_led = LED(17) # Paper
blue_led = LED(27) # PET bottle
green_led = LED(22) # ElecAppliances
red_led = LED(23) # Plastic
white_led = PWMLED(24) # Status light and retake photo
other_led = LED(18) 

camera = PiCamera()
# 照片插入資料庫
# photoPath = ""
label = ""
mydb = dbconfig.mydb
mycursor = mydb.cursor() # 獲取遊標,接下來用cursor提供的方法

# Load Lobe TF model
# --> Change model file path as needed
model = ImageModel.load('/home/pi/Lobe/model')
# Take Photo
def take_photo(path):
    nowTime = str(int(time.time())) # 時戳
    shortPath = "./photo/" + nowTime + ".jpg"
    path = "/var/www/html/photo/" + nowTime + ".jpg"

    # Quickly blink status light
    white_led.blink(0.1,0.1)
    sleep(2)
    print("Pressed")
    white_led.on()
    # Start the camera preview
    camera.start_preview(alpha=200)
    # wait 2s or more for light adjustment
    sleep(3)
    # Optional image rotation for camera
    # --> Change or comment out as needed
    #camera.rotation = 270
    camera.rotation = 0
    #Input image file path here
    # --> Change image path as needed
    camera.capture(path)
    #Stop camera
    camera.stop_preview()
    white_led.off()
    sleep(1)
    return path, shortPath

# Identify prediction and turn on appropriate LED
def led_select(label):
    print(label)
    motor1 = Motor(4)
    motor2 = Motor(25)
    if label == "Paper": # front
        yellow_led.on()
        motor1.change_duty_cycle(180)
        motor2.change_duty_cycle(150)
        sleep(5)
        motor2.change_duty_cycle(90)

    if label == "ElecAppliances": #back
        blue_led.on()
        motor1.change_duty_cycle(90)
        motor2.change_duty_cycle(30)
        sleep(5)
        motor2.change_duty_cycle(90)

    if label == "Plastic": #left
        green_led.on()
        motor1.change_duty_cycle(90)
        motor2.change_duty_cycle(150)
        sleep(5)
        motor2.change_duty_cycle(90)

    if label == "PET bottle": #right
        red_led.on()
        motor1.change_duty_cycle(180)
        motor2.change_duty_cycle(30)
        sleep(5)
        motor2.change_duty_cycle(90)

    if label == "other":
        other_led.on()
        sleep(5)
    else:
        yellow_led.off()
        blue_led.off()
        green_led.off()
        red_led.off()
        white_led.off()

# 將資料插入資料庫
def insertPhotoToDB(path, label):
    sql = "INSERT INTO trash (photoPath, label) VALUES (%s, %s)"
    val = (path, label)
    # 執行sql語句
    mycursor.execute(sql, val)
    # 提交到資料庫執行
    mydb.commit()
    # 關閉遊標
    #mycursor.close()
    # 關閉資料庫連線
    #mydb.close()

def main():
# Main Function
    yellow_led.off()
    white_led.off()
    blue_led.off()
    green_led.off()
    red_led.off()
    other_led.off()
    try:
        while True:
            print("raspberry is on")
            if button.is_pressed:
                print("button.is pressed")
                #other_led.off()
                photoPath, shortPath = take_photo("")
                # Run photo through Lobe TF model
                result = model.predict_from_file(photoPath)
                label = result.prediction
                # --> Change image path
                led_select(result.prediction)
                # 插入資料庫
                insertPhotoToDB(shortPath, label)
            else:
                print("button is not pressed")
                # Pulse status light
                white_led.pulse(2,1)
            sleep(1)
    except KeyboardInterrupt:
        print('關閉程式')

main()
