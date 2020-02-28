<!-- <?php
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

$sql= "SELECT year, mon, sum(act) AS act FROM (SELECT year, mon, day, sum(act) AS act FROM (SELECT year, mon, day, hour, MAX(act) AS act FROM sen WHERE year=".(int)$year. " AND hour>=7 AND hour<=21 GROUP BY year, mon, day, hour)GROUP BY year, mon, day)GROUP BY year, mon";
//쿼리문을 이용하여 result에 db에서 select한 값을 저장한다. (객체지향 메쏘드이용)
$result = $mysqli->query($sql)

?> -->















<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>google chart</title>

    <!-- 구글차트 스크립트 선언 -->
        <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
        <button id="change-chart">Change to Classic</button>


        <script type="text/javascript">
            //차트 그리기
            google.charts.load('current', {'packages':['line', 'corechart']});
            google.charts.setOnLoadCallback(drawChart);

          function drawChart() {

            var button = document.getElementById('change-chart');
            var chartDiv = document.getElementById('chart_div');

            var data = new google.visualization.DataTable();
            data.addColumn('date', 'Month');
            data.addColumn('number', "Average Temperature");
            data.addColumn('number', "Average Hours of Daylight");

            data.addRows([
              [new Date(2014, 0),  -.5,  5.7],
              [new Date(2014, 1),   .4,  8.7],
              [new Date(2014, 2),   .5,   12],
              [new Date(2014, 3),  2.9, 15.3],
              [new Date(2014, 4),  6.3, 18.6],
              [new Date(2014, 5),    9, 20.9],
              [new Date(2014, 6), 10.6, 19.8],
              [new Date(2014, 7), 10.3, 16.6],
              [new Date(2014, 8),  7.4, 13.3],
              [new Date(2014, 9),  4.4,  9.9],
              [new Date(2014, 10), 1.1,  6.6],
              [new Date(2014, 11), -.2,  4.5]
            ]);

            var materialOptions = {
              chart: {
                title: 'Average Temperatures and Daylight in Iceland Throughout the Year'
              },
              width: 900,
              height: 500,
              series: {
                // Gives each series an axis name that matches the Y-axis below.
                0: {axis: 'Temps'},
                1: {axis: 'Daylight'}
              },
              axes: {
                // Adds labels to each axis; they don't have to match the axis names.
                y: {
                  Temps: {label: 'Temps (Celsius)'},
                  Daylight: {label: 'Daylight'}
                }
              }
            };

            var classicOptions = {
              title: 'Average Temperatures and Daylight in Iceland Throughout the Year',
              width: 900,
              height: 500,
              // Gives each series an axis that matches the vAxes number below.
              series: {
                0: {targetAxisIndex: 0},
                1: {targetAxisIndex: 1}
              },
              vAxes: {
                // Adds titles to each axis.
                0: {title: 'Temps (Celsius)'},
                1: {title: 'Daylight'}
              },
              hAxis: {
                ticks: [new Date(2014, 0), new Date(2014, 1), new Date(2014, 2), new Date(2014, 3),
                        new Date(2014, 4),  new Date(2014, 5), new Date(2014, 6), new Date(2014, 7),
                        new Date(2014, 8), new Date(2014, 9), new Date(2014, 10), new Date(2014, 11)
                       ]
              },
              vAxis: {
                viewWindow: {
                  max: 30
                }
              }
            };

            function drawMaterialChart() {
              var materialChart = new google.charts.Line(chartDiv);
              materialChart.draw(data, materialOptions);
              button.innerText = 'Change to Classic';
              button.onclick = drawClassicChart;
            }

            function drawClassicChart() {
              var classicChart = new google.visualization.LineChart(chartDiv);
              classicChart.draw(data, classicOptions);
              button.innerText = 'Change to Material';
              button.onclick = drawMaterialChart;
            }

            drawMaterialChart();

          }

        </script>

  </head>
  <body>
    <div id="chart_div"></div>
  </body>
</html>
