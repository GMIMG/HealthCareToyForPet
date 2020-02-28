


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
google.charts.setOnLoadCallback(drawChart);

function drawChart() {

var data = new google.visualization.DataTable();
data.addColumn('date', 'Time of Day');
data.addColumn('number', 'Rating');

data.addRows([
  [new Date(2015, 0, 1), 5],  [new Date(2015, 0, 2), 7],  [new Date(2015, 0, 3), 3],
  [new Date(2015, 0, 4), 1],  [new Date(2015, 0, 5), 3],  [new Date(2015, 0, 6), 4],
  [new Date(2015, 0, 7), 3],  [new Date(2015, 0, 8), 4],  [new Date(2015, 0, 9), 2],
  [new Date(2015, 0, 10), 5], [new Date(2015, 0, 11), 8], [new Date(2015, 0, 12), 6],
  [new Date(2015, 0, 13), 3], [new Date(2015, 0, 14), 3], [new Date(2015, 0, 15), 5],
  [new Date(2015, 0, 16), 7], [new Date(2015, 0, 17), 6], [new Date(2015, 0, 18), 6],
  [new Date(2015, 0, 19), 3], [new Date(2015, 0, 20), 1], [new Date(2015, 0, 21), 2],
  [new Date(2015, 0, 22), 4], [new Date(2015, 0, 23), 6], [new Date(2015, 0, 24), 5],
  [new Date(2015, 0, 25), 9], [new Date(2015, 0, 26), 4], [new Date(2015, 0, 27), 9],
  [new Date(2015, 0, 28), 8], [new Date(2015, 0, 29), 6], [new Date(2015, 0, 30), 4],
  [new Date(2015, 0, 31), 6], [new Date(2015, 1, 1), 7],  [new Date(2015, 1, 2), 9]
]);


var options = {
  title: 'Rate the Day on a Scale of 1 to 10',
  width: 900,
  height: 500,
  hAxis: {
    format: 'M/d/yy',
    gridlines: {count: 15}
  },
  vAxis: {
    gridlines: {color: 'none'},
    minValue: 0
  }
};

        var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
chart.draw(data, options);

var button = document.getElementById('change');

button.onclick = function () {

  // If the format option matches, change it to the new option,
  // if not, reset it to the original format.
  options.hAxis.format === 'M/d/yy' ?
  options.hAxis.format = 'MMM dd, yyyy' :
  options.hAxis.format = 'M/d/yy';

  chart.draw(data, options);
};
}

        </script>

  </head>
  <body>
    <div id="chart_div"></div>
  </body>
</html>
