# 用來測試 將資料插入資料庫
import time
import dbconfig

# 定義變數
photoPath = ""
label = "Plastic"
mydb = dbconfig.mydb
mycursor = mydb.cursor() # 獲取遊標,接下來用cursor提供的方法

# 拍照
def takePhoto(path, label):
    nowTime = str(int(time.time())) # 時戳
    path = "./photo/" + nowTime +".jpg"
    label = "Plastic"
    return path, label

# 將資料插入資料庫
def insertPhotoToDB(path, label):
    sql = "INSERT INTO trash (photoPath, label) VALUES (%s, %s)"
    val = (path, label)
    # 執行sql語句
    mycursor.execute(sql, val)
    # 提交到資料庫執行
    mydb.commit()
    # 關閉遊標
    mycursor.close()
    # 關閉資料庫連線
    mydb.close()

def main():
    # 連線連至資料庫
    dbconfig
    # 拍照，並將圖片路徑存入資料庫
    trashPhotoPath, trashLabel = takePhoto(photoPath, label)
    insertPhotoToDB(trashPhotoPath, trashLabel)
if __name__ == "__main__" :
    main()