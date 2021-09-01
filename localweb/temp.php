<html>

<head>
  <title>PiClima by DG</title>
  <meta http-equiv="refresh" content="120">
  <script type="text/javascript" src="script/fusioncharts.js"></script>
  <script type="text/javascript" src="script/fusioncharts.charts.js"></script>
  <script type="text/javascript" src="script/fusioncharts.theme.zune.js"></script>
  <link rel="stylesheet" type="text/css" href="css/style.css?v=<?php echo time(); ?>" rel="stylesheet" />
  <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.11.2/css/all.css">
</head>

<body>

  <?php
  include("gtemp.php");
  include("gpress.php");
  include("ghumidity.php");
  include("dados.php");

  // If the query returns a valid response, prepare the JSON string
  if ($lastDataResult)
    $row = mysqli_fetch_array($lastDataResult);
  ?>

  <section>
    <div class="wrapper">
      <h1 class="gamma lato thin ls-xlarge">home weather<br>
        <span class="merriweather tera ls-xlarge light">πClima</span><br>
        <span class="epsilon ls-small">
          <?php
          echo "Último Refresh: " . date("h:i:sa");
          ?></span>
      </h1>
    </div>
    <div class="main-container">
      <div class="card-container">
        <div class="card card-1">
          <div class="card__icon"><i class="fas fa-temperature-high"></i></div>
          <h2 class="card__title"><?= number_format($row['hum_temperature'], 0) ?>&#8451;</h2>
        </div>
        <div class="card card-2">
          <div class="card__icon"><i class="fas fa-tachometer-alt"></i></div>
          <h2 class="card__title"><?= number_format($row['pressure'], 0) ?> hPa</h2>
        </div>
        <div class="card card-3">
          <div class="card__icon"><i class="fas fa-tint"></i></div>
          <h2 class="card__title"><?= number_format($row['humidity'], 0) ?>&#37;</h2>
        </div>
  </section>


  </div>


  <div id="1" class="divTable" style="border: 5px;">
    <div id="2" class="divTableRow">
      <div id="chart-1" align=center class="divTableCell"></div>
    </div>
    <div id="3" class="divTableRow">
      <div id="chart-2" align=center class="divTableCell"></div>
    </div>
    <div id="4" class="divTableRow">
      <div id="chart-3" align=center class="divTableCell"></div>
    </div>
  </div>
  </div>
</body>

</html>