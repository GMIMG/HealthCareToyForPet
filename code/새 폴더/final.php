<?php

$year=date("Y");
$mon=date("n");
$day=date("j");

$servername = "localhost";
$username = "pi";
$password = "1234";
$dbname = "pid";

$mysqli = new mysqli($servername, $username, $password, $dbname);
if ($mysqli->connect_errno) {
    printf("Connect failed: %s\n", $mysqli->connect_error);
    exit();
}
$query= "SELECT hour, MAX(act) AS act FROM sens WHERE year=".(int)$year. " AND mon=" .(int)$mon. " AND day=".(int)$day." AND hour>=7 AND hour<=21 GROUP BY hour";

?>
















<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>google chart</title>

        <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>

        <script type="text/javascript">
            google.charts.load('current', {packages: ['corechart', 'bar']});
            google.charts.setOnLoadCallback(drawBasic);

            function drawBasic() {
                var data = new google.visualization.DataTable();
                data.addColumn('timeofday', 'Time of Day');
                data.addColumn('number', 'Motivation Level');

                data.addRows([
                  <?php
                  /* fetch associative array */
                  while ($row = $result->fetch_assoc()) {
                    echo "[{v: [" .$row["hour"]. ", 0, 0], f: '" .$row["hour"]. " pm'}," .$row["act"]. "],";
                    }
                            /* free result set */
                            $result->free();
                            /* close connection */
                            $mysqli->close();
                  ?>
                ]);

                var options = {
                 title: 'Motivation Level Throughout the Day',
                 hAxis: {
                   title: 'Time of Day',
                   format: 'h:mm a',
                   viewWindow: {
                     min: [6, 30, 0],
                     max: [21, 30, 0]
                   }
                 },
                 vAxis: {
                   title: 'Rating (scale of 1-10)'
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
