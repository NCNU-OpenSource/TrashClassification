import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",   # 資料庫主機地址
    user="raspberrypi",        # 資料庫使用者名稱
    passwd="raspberrypi_password",    # 資料庫密碼
    database="raspberrypi"   # 直連資料庫，如果資料庫不存在，會輸出錯誤資訊
)

# 印出連線結果
print(mydb) 