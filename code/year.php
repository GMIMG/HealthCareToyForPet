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
$sql= "SELECT year, mon, sum(act) AS act FROM (SELECT year, mon, day, sum(act) AS act FROM (SELECT year, mon, day, hour, MAX(act) AS act FROM sen WHERE year=".(int)$year. " AND hour>=7 AND hour<=21 GROUP BY year, mon, day, hour)A GROUP BY year, mon, day)B GROUP BY year, mon";
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
            google.charts.load('current', {'packages':['bar', 'corechart']});
            google.charts.setOnLoadCallback(drawChart);

          function drawChart() {
            var chartDiv = document.getElementById('chart_div');

            var data = new google.visualization.DataTable();
            data.addColumn('date', 'Month');
            data.addColumn('number', "Sum of monthly act");


            data.addRows([
              <?php
              /* fetch associative array, array가 끝날때까지 row에 result를 순서대로 가져오기 */
              while ($row = $result->fetch_assoc()) {//[{v: ["0, 0, 0], f: '0 pm'}," 0"], 식의 json형식 array
              $tem = $row["mon"]-1;

                echo "[new Date(" .$row["year"]. ", " .$tem. "), " .$row["act"]. "],";
                }
                        /* free result set */
                        $result->free(); //result리셋
                        /* close connection */
                        $mysqli->close(); //db close
            ?>
            ]);

            var classicOptions = {
              title: 'Act data in this year',
              width: 900,
              height: 500,
              // Gives each series an axis that matches the vAxes number below.
              series: {
                0: {targetAxisIndex: 0},

              },
              vAxes: {
                // Adds titles to each axis.
                0: {title: 'ACT'},
              },
              hAxis: {
                ticks: [new Date(2018, 0), new Date(2018, 1), new Date(2018, 2), new Date(2018, 3),
                        new Date(2018, 4),  new Date(2018, 5), new Date(2018, 6), new Date(2018, 7),
                        new Date(2018, 8), new Date(2018, 9), new Date(2018, 10), new Date(2018, 11)
                       ]
              },
              vAxis: {
                viewWindow: {

                }
              }
            };

            function drawClassicChart() {
              var classicChart = new google.visualization.ColumnChart(chartDiv);
              classicChart.draw(data, classicOptions);
            }

            drawClassicChart();

          }

        </script>

  </head>
  <body>
    <div id="chart_div"></div>
  </body>
</html>
