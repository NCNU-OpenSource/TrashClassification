<?php
require_once("connectDB.php");

function getTrashInfo($label){
    global $db;
    $arr_fl_data = [];
    // 抓篩選資料
    if($label != ""){
        $sql = "SELECT `photoPath`, `label`, `time` FROM `trash` WHERE `label` = \"$label\" ORDER BY `time` DESC ";
    }
    // 抓所有資料
    else{
        $sql = "SELECT `photoPath`, `label`, `time` FROM `trash` ORDER BY `time` DESC";
    }
    // $result 從DB中取出結果集
    $result = $db->query($sql);
    if ($result -> num_rows > 0) {
        while($row = $result->fetch_assoc()) {
            $trash = 
                array("photoPath" => $row["photoPath"], 
                "label" => $row["label"],
                "time" => $row["time"]
            );
            array_push($arr_fl_data,$trash);
        }
        // 轉json
        // $final = json_encode($arr_fl_data, JSON_FORCE_OBJECT);
        // echo $arr_fl_data;
    }
    else{
        echo "0 結果";
        // $final = null;
    }
    return $arr_fl_data;
}
?>