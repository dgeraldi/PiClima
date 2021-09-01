<?php
require 'vendor/autoload.php';
//Set the correct directory to your .env file
$dotenv = Dotenv\Dotenv::createImmutable('/home/pi');
$dotenv->load();

//Get .env variables
$servername = getenv('SQLSERVER');
$username = getenv('USER_SQL');
$password = getenv('SECRET_SQL');
$dbname = getenv('SQLDBNAME');

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
} 

$sql = "SELECT hum_temperature, pressure, created, humidity from log_temperatura ORDER BY created DESC LIMIT 120";
$result = $conn->query($sql) or exit("Error code ({$conn->errno}): {$conn->error}");

//Get only the first row
$lastData = "SELECT hum_temperature,pressure, humidity FROM log_temperatura ORDER BY id DESC LIMIT 1";
$lastDataResult = $conn->query($lastData) or exit("Error code ({$conn->errno}): {$conn->error}");

$conn->close();

?>
