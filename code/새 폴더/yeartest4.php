


<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>google chart</title>

    <!-- 구글차트 스크립트 선언 -->
        <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>


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


            data.addRows([
              [new Date(2018, 4), 84],
              [new Date(2018, 5), 84],
              [new Date(2018, 6), 84],
              [new Date(2018, 7), 222],
              [new Date(2018, 8), 84],
              [new Date(2018, 9), 84],
              [new Date(2018, 10), 84],
              [new Date(2018, 11), 222]
            ]);

            var classicOptions = {
              title: 'Act data of this year',
              width: 900,
              height: 500,
              // Gives each series an axis that matches the vAxes number below.
              series: {
                0: {targetAxisIndex: 0},

              },
              vAxes: {
                // Adds titles to each axis.
                0: {title: 'Temps (Celsius)'},
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
              var classicChart = new google.visualization.LineChart(chartDiv);
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
