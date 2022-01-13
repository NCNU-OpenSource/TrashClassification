<?php
require("trashModel.php");
?>
<!DOCTYPE html>
<html lang="zh-Hant-TW">

<head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>垃圾辨識結果</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Luxurious+Roman&display=swap');
    </style>
    <style type="text/css">
        h1 {
            font-family: 'Luxurious Roman', cursive;
        }

    </style>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
</head>

<body>
    <div class="container">
        <div class="h1 m-auto">
            <h1>Trash Classification</h1>
        </div>
        <div id="myForm">
            <form id="trashForm" method="post" action="listUI.php">
                <!-- <input name="act" type="hidden" value='getTrashInfo' /> -->
                <div class="row">
                    <div class="col-4">
                        <select name="label" class="form-select" aria-label="Default select example">
                            <option value="all">全部</option>
                            <option value="Paper">紙類</option>
                            <option value="PET bottle">寶特瓶</option>
                            <option value="ElecAppliances">電器用品</option>
                            <option value="Plastic">塑膠</option>
                            <option value="other">其他</option>
                        </select>
                    </div>
                    <div class="col-2">
                        <input class="btn btn-success" type="submit" value="查詢">
                    </div>
                </div>
            </form>
        </div>

        <!-- main working div-->
        <div id="trashTabel">
            <p></p>
        </div>

</body>

</html>

<?php
if (isset($_POST['label'])) {
    $label = $_POST['label'];
} else {
    $label = "";
}

//echo $label;
if ($label == "all") {
    $result = getTrashInfo("");
    //echo $label;
} else {
    $result = getTrashInfo($label);
    //echo $label;
}

// $result 是所有的垃圾資料
// $trash 是$result其中 "一筆" 垃圾資料
echo "<table class=\"table table-striped table-hover table-bordered\" width=\"200\" border=\"1\">";
echo "<tr class=\"text-center\"><td class=\"col-2\">標籤</td><td class=\"col-7\">照片</td><td>時間</td></tr>";
foreach ($result as $trash) {
    echo "<tr><td>", $trash['label'],
    "</td><td>", "<img src=\"", $trash['photoPath'], "\" class=\"mx-auto d-block rounded\" width=\"50%\" alt=\"Responsive image\">",
    // "</td><td>", $trash['photoPath'],
    "</td><td>", $trash['time'];
    echo "</td></tr>";
}
echo "</table>";
?>