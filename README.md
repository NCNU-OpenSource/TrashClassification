## Concept Development
> **發展理念：為什麼要開發這個東西？有什麼用？**[color=red]
- 丟垃圾時，偶爾會不清楚手上的垃圾屬於哪個分類，就呆站在垃圾桶前陷入無窮迴圈的沉思，導致在垃圾桶前大排長龍，甚至最終還是丟錯了垃圾。
- 我們開發的這個辨識回收種類的儀器，旨意就是在解決這項問題，除了讓垃圾桶前的人潮不會擠的水洩不通，也可以讓垃圾正確分類，使地球更美好XD
::: info
暨大宿舍生最大的噩夢，就是每次倒垃圾的時候，只要沒有正確的垃圾分類觀念，隨之而來的即是阿伯「伶刀西郎」的親切問候(哭)，所以為了避免家人遭受無辜的挨罵，我們決定做一個自動分類垃圾的神器，相信有了它，我們將不再恐懼倒垃圾，也不用擔心阿伯有天會氣到中風！
:::
## Implementation Resources
> **應用到的資源：樹莓派？(硬體、軟體？)<有用到都要列出來>、買的詳列從哪買的(價錢)**[color=red]
- 軟體
    - Lobe(線上資源，免費)： 影像辨識模型訓練
    - Raspberry Pi OS(樹莓派的作業系統)
- 硬體
    - pi Camera X 1 ($1020)
    - 樹莓派(pi4) X 1 ($2360)
    - 杜邦線(公公、公母、母母)數條 (borrow)
    - 按鈕 X 1 (borrow)
    - LED燈泡 X 6 (borrow)
    - 麵包板 X 2 (一塊 $50)
    - 電阻 X 8 (borrow)
    - 樹莓派的鍵盤 X 1 ($720)
    - 樹莓派的滑鼠 X 1 ($350)
    - 馬達 X 2 (一顆 $150)
- 外觀
    - 紙箱($30)
    - 竹筷子($)
    - 紙碗
    - 橡皮筋 
    - 雙面膠
    - 膠帶
    - 紙膠帶
    - 塑膠袋(垃圾袋)
## Existing Library/Software
> **使用了哪些現有的函式庫或軟體 要在這個部分說明條列**[color=red]
- 基於影像辨識
- 主程式 ==`trashClassification.py`==
    - [主程式-參考網址](https://www.hackster.io/jenfoxbot/make-a-pi-trash-classifier-with-ml-e037a6)
    - 根據上方網址的程式碼做更改，新增馬達轉動的功能、將照片路徑加入資料庫

## Implementation Process
> **實作過程**[color=red]
- 在家目錄下 clone 我們的檔案
    - `cd ~`
    - ==`git clone URL`==
### 樹莓派 與 LED 與 攝影鏡頭模組
- 樹莓派
- LED燈(杜邦線、麵包板、按鈕)
	- 總共6顆LED燈(5顆紅、1顆白)。
		- 分別代表 ElecAppliances、Paper、PET bottle、Plastic、other、顯示是否有在拍照。
	- 將LED燈接到麵包版上，透過杜邦線連到樹莓派上。
	- 其中一端經過電阻接到樹莓派的編號6腳位，也就是GND接地。另外一端分別是：
	![](https://www.raspberrypi.com.tw/wp-content/uploads/2014/09/connect-serial-to-raspberry-pi-model-b-plus.png =60%x)
		- ElecAppliances 👉 編號22的腳位。
		- Paper 👉 編號17的腳位。
		- PET bottle 👉 編號27的腳位。
		- Plastic 👉 編號23的腳位。
		- other 👉 編號24的腳位。
- 攝影鏡頭模組
![](https://i.imgur.com/uAMRAwv.jpg =40%x)
	- 直接連接到樹莓派上
	![](https://i.imgur.com/K25Bm5F.png =50%x)
### 軟體主程式
- **目的:** 藉由壓下按鈕讓pi camera拍完照，透過Lobe影像辨識的套件，並且將便是結果顯示正確地顯示在五個LED燈上，
- 打開主程式(trashClassification.py)
``` python=
- # ------------------------------------------------------------------------
# Trash Classifier ML Project
# Please review ReadMe for instructions on how to build and run the program
#
# (c) 2020 by Jen Fox, Microsoft
# MIT License
# --------------------------------------------------------------------------

#import Pi GPIO library button class
from gpiozero import Button, LED, PWMLED
from picamera import PiCamera
from time import sleep

from lobe import ImageModel
import time

#Create input, output, and camera objects
button = Button(2)

yellow_led = LED(17) # Paper
blue_led = LED(27) # PET bottle
green_led = LED(22) # ElecAppliances
red_led = LED(23) # Plastic
white_led = PWMLED(24) # Status light and retake photo
other_led = LED(18) 

camera = PiCamera()

label = ""
# Load Lobe TF model
# --> Change model file path as needed
model = ImageModel.load('/home/pi/Lobe/model')
# Identify prediction and turn on appropriate LED
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

def led_select(label):
    print(label)
    motor1 = Motor(4)
    motor2 = Motor(25)
    if label == "Paper": # front
        yellow_led.on()
        sleep(5)

    if label == "ElecAppliances": #back
        blue_led.on()
        sleep(5)


    if label == "Plastic": #left
        green_led.on()
        sleep(5)

    if label == "PET bottle": #right
        red_led.on()
        sleep(5)

    if label == "other":
        other_led.on()
        sleep(5)
    else:
        yellow_led.off()
        blue_led.off()
        green_led.off()
        red_led.off()
        white_led.off()

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
```
### LOBE
- 利用 Lobe 製作影像辨識模型之實作過程
    1. 先取得回收種類樣本照片(類別：ElecAppliances、Paper、PET bottle、Plastic、other)。
    2. 在本機端存成五個資料夾，檔名如類別名稱。
    3. 開啟 Lobe 點選 `import` 匯入資料夾 `dataset` 
	    ![](https://i.imgur.com/9aTjx09.png =50%x)
	4. 選擇「標籤名」如資料夾檔名`Label Using Folder Name`
        ![](https://i.imgur.com/KJ7mzC2.png =50%x)
	5. 依序匯入五個資料夾後，Lobe 上面就會有五個類別「標籤」
	    ![](https://i.imgur.com/KKzHZ0g.png =50%x)
	6. 等待自動訓練完成後，就可以點選匯出`Export`的`TensorFlow Lite`(支援Linux作業系統，讓裝置可執行訓練模型的工具)
        ![](https://i.imgur.com/r38d8N6.png =50%x)
    7. 把訓練好的模型資料夾透過隨身碟放到樹莓派裡面
    8. ==主程式碼==裡對應好對的路徑（`model = ImageModel.load('/home/pi/Lobe/model')`）

### 馬達
- **目的:** 為了搭建一個自動化的平台，放置垃圾進行影像辨識，並且得到分類結果之後，能夠傾倒垃圾到四個方位中正確的垃圾袋位置
- **硬體材料:** MG996R伺服馬達 X 2 ， 杜邦線 X 6
- **軟體程式:** python
- ==**step 1**== 首先在python的程式撰寫上，將馬達包成一個物件，之後讓主程式引用，這樣既可以實現多馬達的控制，也可以讓主程式不會太複雜。
	- 打開以下是`Motor.py` 的完整程式
	```python=
	import RPi.GPIO as GPIO
	import time 
	class Motor:
    	PWM_FREQ = 50
    	#STEP = 90 #rotate angle
    	def __init__(self,CONTROL_PIN)  :     
        	self.CONTROL_PIN = CONTROL_PIN
        	GPIO.setmode(GPIO.BCM)
        	GPIO.setup(self.CONTROL_PIN, GPIO.OUT)
        	self.pwm = GPIO.PWM(CONTROL_PIN, Motor.PWM_FREQ)
        	self.pwm.start(0)
        	print("Motor Set up already!!")
       
    	def change_duty_cycle(self,angle):
        	print('角度={: >3}'.format(angle))
        	duty_cycle = (0.05 * Motor.PWM_FREQ) + (0.19 * Motor.PWM_FREQ * angle / 180)
        	self.pwm.ChangeDutyCycle(duty_cycle)
        	time.sleep(0.3)
	```
- ==**step 2**== 再將程式引用到主程式之前，我們先了解這次兩顆馬達的實際應用範圍，我們用以下這張圖來解釋:
    ![](https://i.imgur.com/lIL3Mlo.png)
    > p.s. 紅色的馬達負責做水平的180度旋轉，藍色的馬達負責做左右傾倒，讓平台傾倒上方的垃圾
-  ==**step 3**== 接著我們回到主程式(`trashClassification.py`)，首先我們要先加上這行，引入寫好的馬達物件
	```python= 
	from Motor import Motor
	```
	- 接著在`def ledselect():`這個function裏頭我們宣告兩個物件，這邊我在樹梅派上的GPIO腳位分別是，底部的馬達選用4號，上面的馬達選用25號
	```python= 
	motor1 = Motor(4) #可依照自己接的腳位做調整
	motor2 = Motor(25) #可依照自己接的腳位做調整
	```
	- 在`def ledselect():`同樣的function內，將影像辨識出來的四個結果分別讓馬達做出對應的動作
	```python= 
	if label == "Paper": # back
        	yellow_led.on()
        	motor1.change_duty_cycle(180)
        	motor2.change_duty_cycle(150)
        	sleep(5)
        	motor2.change_duty_cycle(90)

    	if label == "ElecAppliances": #right
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

    	if label == "PET bottle": #front
        	red_led.on()
        	motor1.change_duty_cycle(180)
        	motor2.change_duty_cycle(30)
        	sleep(5)
        	motor2.change_duty_cycle(90)
	```
- ==**step 4**== 已經把程式寫好了，接下來就來實際讓馬達連接樹梅派看看
	![](https://i.imgur.com/yRNxAXm.png)
-  ==**step 5**== 運行以下的測試程式`motortest.py`，讓我們查看馬達是否能動
```python= 
import RPi.GPIO as GPIO
CONTROL_PIN = 4  # it means GPIO4 = 7
PWM_FREQ = 50
STEP=90 
 
GPIO.setmode(GPIO.BCM)
GPIO.setup(CONTROL_PIN, GPIO.OUT)
 
pwm = GPIO.PWM(CONTROL_PIN, PWM_FREQ)
pwm.start(0)
 
def angle_to_duty_cycle(angle=0):
    duty_cycle = (0.05 * PWM_FREQ) + (0.19 * PWM_FREQ * angle / 180)
    return duty_cycle
 
try:
    print('按下 Ctrl-C 可停止程式')
    for angle in range(0, 181, STEP):
        dc = angle_to_duty_cycle(angle)
        pwm.ChangeDutyCycle(dc)
        print('角度={: >3}, 工作週期={:.2f}'.format(angle, dc))
        time.sleep(2)
    for angle in range(180, -1, -STEP):
        dc = angle_to_duty_cycle(angle)
        print('角度={: >3}, 工作週期={:.2f}'.format(angle, dc))
        pwm.ChangeDutyCycle(dc)
        time.sleep(2)
    pwm.ChangeDutyCycle(angle_to_duty_cycle(90))
    while True:
        next
except KeyboardInterrupt:
    print('關閉程式')
finally:
    pwm.stop()
    GPIO.cleanup()
```
-  ==**step 6**== 現在準備來架設我們的...
	![](https://i.imgur.com/rAwWzpb.png =70%x)
	- 需要的材料有 竹筷 * 1，保麗龍 * 1，紙碗 * 1，白底的厚紙板 * 1
	- 首先先將白紙板裁成適合的正方形(20cm * 20cm)
	![](https://i.imgur.com/G9rncZX.png =70%x)
	- 再來將紙碗底部戳洞讓竹筷穿過，減兩塊小保麗龍上下固定，讓筷子跟紙碗的連接處不會亂動，在碗的邊緣黏上雙面膠與平台相黏，如下圖:
	![](https://i.imgur.com/9tuUCcb.png =50%x)
	- 再來將我們的第二顆伺服馬達的頭?用橡皮筋緊緊地與竹筷捆上，並且用膠帶纏上加固，如下圖
	- ![](https://i.imgur.com/eTyAtid.png =70%x)
    - 上方的平台加桿子已經做好了，接著是下方的兩顆伺服馬達，因為馬達在轉動時，可能自己也會因力量而導致自身不穩，所以我們想到用兩塊保麗龍，並中間割下一塊讓馬達可以放入，將其固定，接著依照設計圖將上下馬達用雙面膠貼黏，如下圖
    - ![](https://i.imgur.com/DuPi8U2.png =70%x)
    - 最後就是將平台與兩伺服馬達底座相結合，這一來，我們的自動傾倒平台就完成了!!
    - ![](https://i.imgur.com/asxX7L7.png)

## 垃圾分類桶構造
- ![](https://i.imgur.com/ga2Iayr.png)
- ![](https://i.imgur.com/Uyd4Id9.jpg)
### 網頁呈現(頁面、資料庫)
- [共筆連結 - 網頁呈現](https://hackmd.io/ZASSYvH3QDitgXAFZASm4w)
1. 安裝 Apache 伺服器
	* `sudo apt-get update`
	* `sudo apt-get install apache2`
	* `sudo service apache2 status`
	    * 可以看到 apache2 目前的狀態是開啟的，預設是開啟的
	    * ![](https://i.imgur.com/LCiVKI8.png)
2. 更改 Apache2 設定檔
	* `sudo service apache2 stop`
	* `sudo apt-get install vim`
	* `sudo vim /etc/apache2/ports.conf`
	    * 原本是 `Listen 80`，改成 `Listen 8081`
	    * ![](https://i.imgur.com/n3DgDwK.png)
	* 開啟 apache2  
	    * `sudo service apache2 start`  
	* 看
	    * `sudo service apache2 status`  
	    * `sudo netstat -ntupla`
	        * 可以看到 apache2 跑在 8081 上
	        * ![](https://i.imgur.com/7U0izmB.png)
3. 安裝 PHP 開發環境
	* `sudo apt-get install php libapache2-mod-php` 
	* `cd /var/www`
	* `sudo chown pi:root html`
	* `ls -l`
	* ![](https://i.imgur.com/NVJpEXI.png)
4. 安裝設定MySQL資料庫系統
	* 安裝需要用到的套件
		*  `sudo apt install mariadb-server php7.4-fpm php7.4-mysql`
5. 使用MySQL監視器:就是MySQL的CLI介面
	* `sudo mysql -u root`
	* 建立 `raspberrypi` 資料庫
		* ` CREATE DATABASE raspberrypi;`
	* 建立一個能夠針對 raspberrypi 資料庫操作的使用者
		* `@localhost`：這個使用者只能由這台本機登入  
		* `CREATE USER 'raspberrypi'@'localhost' IDENTIFIED BY 'raspberrypi_password';`
		* ![](https://i.imgur.com/HL2Fieu.png)
		* `GRANT ALL PRIVILEGES ON raspberrypi.* TO "raspberrypi"@"localhost";`
		* `FLUSH PRIVILEGES;`
		* `EXIT;`
		* ![](https://i.imgur.com/63mJV0y.png)
6. 安裝MySQL管理工具phpMyAdmin
    * 安裝phpMyAdmin
        * `sudo apt-get  install phpmyadmin`
    * 登入MySQL再輸入密碼
        * `sudo mysql –u raspberrypi –p` 
    * `sudo vim /etc/apache2/apache2.conf`
        * 到最下面輸入: `Include /etc/phpmyadmin/apache.conf` 再存檔
        * ![](https://i.imgur.com/upzF98Z.png)
    * `sudo service apache2 restart`
    * 打開瀏覽器輸入 `localhost:8081/phpmyadmin/`
    * ![](https://i.imgur.com/T0AeiAR.png)
* 用剛剛建立的使用者去登入
    * 帳號: `raspberrypi`
    * 密碼: `raspberrypi_password`
    * ![](https://i.imgur.com/yeSbqRw.png)
* 在 `raspberrypi` 的資料庫下新增一個 `trash` 的資料表
    * 結構如下 :point_down:
    * ![](https://i.imgur.com/9oq9wLW.png)
* 在 `dbconfig.py` 改資料庫相關資料
    * ![](https://i.imgur.com/1n5mM9r.png)
    * 如果忘了 MySQL 相關資料，可以到 `/etc/phpmyadmin` 下的 `config.inc.php` 看相關資料
    * ![](https://i.imgur.com/ZN8Wvp8.png)
* ==執行測試檔案 `trashPhoto.py`==
    * `cd ~/TrashClassification/`
    * `./trashPhoto.py`
        *  資料寫進資料庫了!
7. 編輯 HTML 網頁
    * 將剛剛下載 TrashClassification 中的 `listUI.php` 移至 `/var/www/html` 下
	    * `cd ~/TrashClassification/`
	    * `mv listUI.php /var/www/html`
	    * `mv connectDB.php /var/www/html`
	    * `mv trashModel.php /var/www/html`
8. 改 Apache 預設讀取哪個檔案
	* `sudo vim /etc/apache2/apache2.conf` 
	* 新增 `DirectoryIndex listUI.php`
	* ![](https://i.imgur.com/NYptDec.png)
	* `sudo service apache2 reload`
- 架好了 !
    - ![](https://i.imgur.com/vu6fWRC.png)

## Knowledge from Lecture
> **從我們這堂課那部分學到的：**[color=red]
- 
## Installation
> **開始教人家怎麼安裝：**[color=red]
- 安裝 Lobe => (官網：https://www.lobe.ai/)
## Usage
> **解釋怎麼使用：**[color=red]

- Step 1
    - 放入要辨識的垃圾到平台上
- Step 2
    - 長按 3 秒按鈕，使其開始辨識
- Step 3
    - 等待平台自動分類並傾倒垃圾至正確的垃圾袋 


       
## Job Assignment
> **作業分配：《組員貢獻多少%資源》**[color=red]
## References
> **我在網路上有參考到什麼資料：《詳列：不管線上資源或線下詢問》**[color=red]
### 線上資源
- 此實作參考教程：https://www.hackster.io/jenfoxbot/make-a-pi-trash-classifier-with-ml-e037a6
- 應用的影像辨識軟體「Lobe」：https://www.lobe.ai/
- 什麼是「TensorFlow Lite」: https://www.tensorflow.org/lite/guide?hl=zh-tw


### 線下詢問
- 郭子緯：詢問如何呈現辨識資料，用網頁呈現~