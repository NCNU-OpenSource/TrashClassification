<?php
// 連線資料庫用的副程式
$host = '127.0.0.1'; // 執行 DB Server 的主機
$user = 'raspberrypi'; // 登入 DB 用的 DB帳號
$pass = 'raspberrypi_password'; // 登入 DB 用的 DB密碼
$dbName = 'raspberrypi'; // 使用的資料庫名稱

// $db 即為未來執行 SQL 指令所使用的物件
$db = mysqli_connect($host, $user, $pass, $dbName) or die('Error with MySQL connection'); //跟MyMSQL連線並登入
//設定編碼為 unicode utf
mysqli_query($db,"SET NAMES utf8");
?>
