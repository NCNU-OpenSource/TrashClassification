## Concept Development
> **發展理念：為什麼要開發這個東西？有什麼用？**
- 丟垃圾時，偶爾會不清楚手上的垃圾屬於哪個分類，就呆站在垃圾桶前陷入無窮迴圈的沉思，導致在垃圾桶前大排長龍，甚至最終還是丟錯了垃圾。
- 我們開發的這個辨識回收種類的儀器，旨意就是在解決這項問題，除了讓垃圾桶前的人潮不會擠的水洩不通，也可以讓垃圾正確分類，使地球更美好XD
::: info
暨大宿舍生最大的噩夢，就是每次倒垃圾的時候，只要沒有正確的垃圾分類觀念，隨之而來的即是阿伯「伶刀西郎」的親切問候(哭)，所以為了避免家人遭受無辜的挨罵，我們決定做一個自動分類垃圾的神器，相信有了它，我們將不再恐懼倒垃圾，也不用擔心阿伯有天會氣到中風！
:::
## Implementation Resources
> **應用到的資源：樹莓派？(硬體、軟體？)<有用到都要列出來>、買的詳列從哪買的(價錢)**
- 軟體
    - Lobe(線上資源，免費): 影像辨識模型訓練
    - Raspberry Pi OS(樹莓派的作業系統)
- 硬體
    - [pi Camera X 1 ($1020)](https://shopee.tw/%E6%A8%B9%E8%8E%93%E6%B4%BERaspberry-Pi-%E5%8E%9F%E5%BB%A0%E7%9B%B8%E6%A9%9F%E9%85%8D%E4%BB%B6-Raspberry-Pi-camera-module-v2-i.143152281.4228122711)
    - 樹莓派(pi4) X 1 ($2360)
    - 杜邦線(公公、公母、母母)數條 (borrow)
    - 按鈕 X 1 (borrow)
    - LED燈泡 X 6 (borrow)
    - [麵包板 X 2 (一塊 $50)](https://shopee.tw/-%E7%92%B0%E5%B3%B6%E7%A7%91%E6%8A%80-%E9%BA%B5%E5%8C%85%E6%9D%BF830%E5%AD%94%E7%B4%85%E8%97%8D%E7%B7%9A%E7%84%A1%E7%84%8A%E9%BA%B5%E5%8C%85%E6%9D%BF%E5%85%8D%E7%84%8A%E5%BC%8F%E6%B8%AC%E8%A9%A6%E9%9B%BB%E8%B7%AF%E6%9D%BF%E8%90%AC%E8%83%BD%E6%9D%BF-i.280233910.4548815084
)
    - 電阻 X 8 (borrow)
    - 樹莓派的鍵盤 X 1 ($720)
    - 樹莓派的滑鼠 X 1 ($350)
    - [馬達 X 2 (一顆 $150)](https://shopee.tw/%E3%80%90%E7%92%B0%E5%B3%B6%E7%A7%91%E6%8A%80%E3%80%91(F3-3-4)%E2%98%85%E5%85%A8%E8%87%BA%E7%8F%BE%E8%B2%A8%E2%98%85-MG996-MG996R-13KG-%E5%A4%A7%E6%89%AD%E5%8A%9B%E8%88%B5%E6%A9%9F-%E6%A9%9F%E5%99%A8%E4%BA%BA-%E9%87%91%E5%B1%AC%E9%BD%92%E8%BC%AA%E8%88%B5%E6%A9%9F-%E4%BC%BA%E6%9C%8D%E9%A6%AC-i.280233910.7843762681
)
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
> **使用了哪些現有的函式庫或軟體 要在這個部分說明條列**
- 基於影像辨識
- 主程式 `trashClassification.py`
    - [主程式-參考網址](https://www.hackster.io/jenfoxbot/make-a-pi-trash-classifier-with-ml-e037a6)
    - 根據上方網址的程式碼做更改，新增馬達轉動的功能、將照片路徑加入資料庫

## Implementation Process
> **實作過程**
- 在家目錄下 clone 我們的檔案
    - `cd ~`
    - `git clone https://github.com/Huei-Lin-Lin/TrashClassification.git`
    - `sudo apt-get update`
    - `sudo apt-get install python3.6`
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
- 打開 `trash.py`

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
	- 打開 `Motor.py` 的完整程式
- ==**step 2**== 再將程式引用到主程式之前，我們先了解這次兩顆馬達的實際應用範圍，我們用以下這張圖來解釋:
    ![](https://i.imgur.com/lIL3Mlo.png)
    > p.s. 紅色的馬達負責做水平的180度旋轉，藍色的馬達負責做左右傾倒，讓平台傾倒上方的垃圾
-  ==**step 3**== 接著我們回到主程式 `trashClassification.py` ，首先我們要先加上這行，引入寫好的馬達物件
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
-  ==**step 5**== 運行馬達測試程式 `motortest.py`，讓我們查看馬達是否能動
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

### 垃圾分類桶構造
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
* 執行測試檔案 `trashPhoto.py`
    * `cd ~/TrashClassification/`
    * `python3 trashPhoto.py`
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
### 執行主程式 `trashClassification.py`
- `cd ~/TrashClassification/`
- `python3 trashClassification.py`

## Knowledge from Lecture
> **從我們這堂課那部分學到的：**
- 我們使用 ssh 連線到樹莓派裡 => [課堂教學：ssh連線](https://hackmd.io/@ncnu-opensource/By4H6JLNW/%2Fwl1BJaOIRQqavZ5rn0jMNQ?type=book)
- 樹莓派 => [課堂教學：樹莓派](https://hackmd.io/@ncnu-opensource/By4H6JLNW/https%3A%2F%2Fhackmd.io%2FNpR3bL4UQViidcrJaqYlpw%3Fview?type=book)
- 我們使用 Apache2 => [課堂教學：Web Sever](https://hackmd.io/@ncnu-opensource/By4H6JLNW/%2FI_xmNNBvSEWLw0mcMDhcMA?type=book)
## Usage
> **解釋怎麼使用：**
- Step 1
    - 放入要辨識的垃圾到平台上
- Step 2
    - 執行主程式 
    - `cd ~/TrashClassification/`
    - `python3 trashClassification.py`
- Step 3
    - 長按 3 秒按鈕，使其開始辨識
- Step 3
    - 等待平台自動分類並傾倒垃圾至正確的垃圾袋 
- Step 4
    - 觀察麵包板上的 LED 燈（會顯示正確分類）
- Step 5
    - 觀察網頁上的垃圾快照與分類結果

## Job Assignment
> **作業分配：《組員貢獻多少%資源》**
- 後端: `林惠霖`
    -  (python) 每次拍完照片就將照片 insert 到資料庫裡
    -  PHP: fetch 資料
    -  建資料庫
- 前端: `王俞文`
    -  網頁頁面: 標籤、照片
    -  抓後端的資料
- 馬達控制: `王念祖`
    -  python 程式碼馬達控制
    -  自動化馬達平台架設
- 訓練模型: `黃日亘`
    -  包含拍照、手動調整模型辨識結果
- 大家一起做
    -  將大家寫的東西合在一起、執行
    -  外觀: 支架、固定
    -  PPT、github 內容
    -  錄實作影片
## References
> **我在網路上有參考到什麼資料：《詳列：不管線上資源或線下詢問》**
### 線上資源
- 此實作參考教程：https://www.hackster.io/jenfoxbot/make-a-pi-trash-classifier-with-ml-e037a6
- 按鈕
- 應用的影像辨識軟體「Lobe」：https://www.lobe.ai/
- 什麼是「TensorFlow Lite」：https://www.tensorflow.org/lite/guide?hl=zh-tw
- 前端-bootstrap：https://getbootstrap.com/
- 怎麼將pwn包成物件 https://stackoverflow.com/questions/55714636/how-can-i-use-raspberry-pi-gpio-setup-and-pwm-commands-in-init-function-of-a

### 線下詢問
- 郭子緯：詢問如何呈現辨識資料 => 用網頁呈現~
- 墊腳石的店員: 要超大紙箱