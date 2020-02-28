<?php
//날짜를 변수에 저장
$year=date("Y");
$mon=date("n");
$day=date("j");
$DOW=date('w');

$PDOW=$DOW+7;
$Lastmon=date("n",strtotime("-".$PDOW." days"));
$Lastday=date("j",strtotime("-".$PDOW." days"));

//mysql의 정보를 변수에 저장
$servername = "localhost";
$username = "root";
$password = "111111";
$dbname = "pid";

//mysql에 접속한다.
$mysqli = new mysqli($servername, $username, $password, $dbname);

//서버에 접속 실패시 프린트하고 종료
if ($mysqli->connect_errno) {
    printf("Connect failed: %s\n", $mysqli->connect_error);
    exit();
}

//수집해올 DB를 SQL문으로 SELECT
if ($Lastmon==$mon) {
  $sql= "SELECT year, mon, day, SUM(act) AS act FROM (SELECT year, mon, day, hour, MAX(act) AS act FROM sens WHERE year=" .(int)$year. " AND hour>=7 AND hour<=21 GROUP BY year, mon, day, hour)A WHERE (mon=" .(int)$Lastmon. " AND day>=".(int)$Lastday. ") AND (mon=" .(int)$mon. " AND day<=".(int)$day. ") GROUP BY year, mon, day";
}
else {
  $sql= "SELECT year, mon, day, SUM(act) AS act FROM (SELECT year, mon, day, hour, MAX(act) AS act FROM sens WHERE year=" .(int)$year. " AND hour>=7 AND hour<=21 GROUP BY year, mon, day, hour)A WHERE (mon=" .(int)$Lastmon. " AND day>=".(int)$Lastday. ") OR (mon=" .(int)$mon. " AND day<=".(int)$day. ") GROUP BY year, mon, day";
}

//쿼리문을 이용하여 result에 db에서 select한 값을 저장한다. (객체지향 메쏘드이용)
$result = $mysqli->query($sql);

$i=0;
$array = array(0,0,0,0,0,0,0,0,0,0,0,0,0,0);

while ($row = $result->fetch_assoc()) {
  $array[$i]=$row["act"];
  $i=$i+1;

  }
?>















<!DOCTYPE html>
<html>
<head>
  <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
  <script type="text/javascript">
    google.charts.load('current', {'packages':['corechart']});
    google.charts.setOnLoadCallback(drawChart);

    function drawChart() {
      var data = google.visualization.arrayToDataTable([
        <?php
        echo "['DayOfWeek', 'LastWeek', 'ThisWeek'],['Sun', " .$array[0]. ", " .$array[7]. "],['mon', " .$array[1]. ", " .$array[8]. "],['Tue', " .$array[2]. ", " .$array[9]. "],['Wen', " .$array[3]. ", " .$array[10]. "],['Tur', " .$array[4]. ", " .$array[11]. "],['Fri', " .$array[5]. ", " .$array[12]. "],['Sat', " .$array[6]. ", " .$array[13]. "]"
        ?>
      ]);



      var options = {
        title: 'Company Performance',
        curveType: 'function',
        legend: { position: 'bottom' },
        vAxis: {
          viewWindow: {
            min: 0
          }
        }
      };

      var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));

      chart.draw(data, options);
    }
  </script>
</head>
<body>
  <div id="curve_chart" style="width: 900px; height: 500px"></div>
</body>
</html>
