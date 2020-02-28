<?php
$year=date("Y")
$year=(int)$year
$mon=date("n")
$mon=(int)$mon
$day=date("j")
$day=(int)$day

$servername = "localhost";
$username = "pi";
$password = "1234";
$dbname = "pid";

$conn = mysqli_connect($servername, $username, $password, $dbname);
if (!$conn) {
    die("Connection failed: " . mysqli_connect_error());
}

$sql = "SELECT hour, MAX(act) as act FROM sens WHERE year=&year AND mon=&mon AND day=&day AND hour>=7 AND hour<=21" GROUP BY hour;
$result = mysqli_query($conn,$sql);
?>
