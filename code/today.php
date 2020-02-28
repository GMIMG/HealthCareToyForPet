<?php
//날짜를 변수에 저장
$year=date("Y");
$mon=date("n");
$day=date("j");

//mysql의 정보를 변수에 저장
$servername = "localhost";
$username = "pi";
$password = "1234";
$dbname = "pid";

//mysql에 접속한다.
$mysqli = new mysqli($servername, $username, $password, $dbname);

//서버에 접속 실패시 프린트하고 종료
if ($mysqli->connect_errno) {
    printf("Connect failed: %s\n", $mysqli->connect_error);
    exit();
}

//수집해올 DB를 SQL문으로 SELECT
$sql= "SELECT hour, MAX(act) AS act FROM sen WHERE year=".(int)$year. " AND mon=" .(int)$mon. " AND day=".(int)$day." AND hour>=7 AND hour<=21 GROUP BY year, mon, day, hour";
//쿼리문을 이용하여 result에 db에서 select한 값을 저장한다. (객체지향 메쏘드이용)
$result = $mysqli->query($sql)

?>















<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>google chart</title>

    <!-- 구글차트 스크립트 선언 -->
        <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
        <script type="text/javascript">
            //차트 그리기
            google.charts.load('current', {packages: ['corechart', 'bar']});
            google.charts.setOnLoadCallback(drawBasic);
            //차트에 들어갈 정보를 함수로 수집 (column차트-> 구글차트 사이트 참고)
            function drawBasic() {
                var data = new google.visualization.DataTable();
                data.addColumn('timeofday', 'Time of Day');
                data.addColumn('number', 'Act');
                data.addRows([
                  <?php
                  /* fetch associative array, array가 끝날때까지 row에 result를 순서대로 가져오기 */
                  while ($row = $result->fetch_assoc()) {//[{v: ["0, 0, 0], f: '0 pm'}," 0"], 식의 json형식 array
                    echo "[{v: [" .$row["hour"]. ", 0, 0], f: '" .$row["hour"]. "'}," .$row["act"]. "],";
                    }
                            /* free result set */
                            $result->free(); //result리셋
                            /* close connection */
                            $mysqli->close(); //db close
                ?>
              ]);

                var options = {//차트옵션
                 title: 'Act in today',
                 hAxis: {
                   title: 'Time of Day',
                   format: 'h:mm a',
                   viewWindow: {
                     min: [6, 00, 0],
                     max: [22, 00, 0]
                   }
                 },
                 vAxis: {
                   title: 'Act'
                 }
                };

                var chart = new google.visualization.ColumnChart(
                 document.getElementById('chart_div'));

                chart.draw(data, options);
            }



        </script>

  </head>
  <body>
    <div id="chart_div"></div>
  </body>
</html>
