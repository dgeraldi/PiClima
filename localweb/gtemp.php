<?php
include("fusioncharts.php");
include("dados.php");


//For 2D Column WITH Heat Index Line
if ($result) {
	// The `$arrData` array holds the chart attributes and data
	$arrData = array(
	"chart" => array(
	"caption"=> "Temperatura & Heat Index",
	"xAxisname"=> "Dias/Horas",
	"yAxisName"=> "Celsius",
	"paletteColors" => "#0075c2,#cc0000",
	"baseFont" => "Helvetica Neue,Arial",
	"captionFontSize" => "14",
	"subcaptionFontSize" => "14",
	"subcaptionFontBold" => "0",
	"placeValuesInside" => "1",
	"showShadow" => "0",
	"usePlotGradientColor" => "0",
	"bgAlpha" => "0",
	"canvasBgAlpha" => "0",
	"divlineColor"=> "#999999",
	"divLineIsDashed"=> "1",
	"divLineDashLen"=> "1",
	"divLineGapLen"=> "1",
	"showHoverEffect"=> "1",
	"showborder" => "0",
	"showplotborder" => "0",
	"showcanvasborder" => "0",
	//Values
	"numVisiblePlot"=> "27",
	"yAxisMaxValue"=>"50",
	"showLineValues"=> "1",
	"valuePosition"=> "ABOVE",
	"valueFontColor" => "#000000",
	"valuePadding"=>"5",
	//"numberSuffix"=> "°C",
	//Tooltip
	"toolTipColor"=> "#ffffff",
	"toolTipBorderThickness"=> "0",
	"toolTipBgColor"=> "#000000",
	"toolTipBgAlpha"=> "80",
	"toolTipBorderRadius"=> "2",
	"toolTipPadding"=> "5",
	//Scroll
	"scrollheight"=> "10",
	"flatScrollBars"=> "1",
	"scrollShowButtons"=> "0",
	"scrollColor"=> "#cccccc",
	"scrollPadding" => "5",

		)
	);

$categoryArray = array();
$tempDataArray = array();
$heatIndexDataArray = array();

// Fetch data from the result and populate arrays
while ($row = mysqli_fetch_array($result)) {
	// Populate category array
	array_push(
		$categoryArray,
		array(
			"label" => date("d/m H:i", strtotime($row['created']))
		)
	);

	// Populate Temperature data array
	array_push(
		$tempDataArray,
		array(
			"value" => number_format($row["hum_temperature"], 0)
		)
		);
	// Assuming $row["heat_index"] contains Heat Index data in the same loop
	array_push(
		$heatIndexDataArray,
		array(
			"value" => number_format($row["heat_index"], 0)
		)
		);
}

// Form the dataset structure for Temperature and Heat Index
$arrData["dataset"] = array(
	array(
		"seriesName" => "Temperatura",
		"data" => $tempDataArray
	),
	array(
		"seriesName" => "Heat Index",
		"renderAs" => "line",
		"data" => $heatIndexDataArray
	)
);

// Set the categories
$arrData["categories"] = array(
	array(
		"category" => $categoryArray
	)
);
$jsonEncodedData = json_encode($arrData);

$columnChart = new FusionCharts("scrollcombi2d", "chartTemp", 800, 300, "chart-1", "json", $jsonEncodedData);
// Render the chart
$columnChart->render();
}

//********************************************/
//For 2D Column only with no Heat Index line
/*
if ($result) {
	// The `$arrData` array holds the chart attributes and data
	$arrData = array(
		"chart" => array(
			"caption" => "Temperatura",
			"xAxisName" => "Dias/Horas",
			"yAxisName" => "Celsius",
			"yAxisMaxValue" => "45",
			"paletteColors" => "#0075c2",
			"valueFontColor" => "#ffffff",
			"baseFont" => "Helvetica Neue,Arial",
			"captionFontSize" => "14",
			"subcaptionFontSize" => "14",
			"subcaptionFontBold" => "0",
			"placeValuesInside" => "1",
			"rotateValues" => "1",
			"showShadow" => "0",
			"divlineColor" => "#999999",
			"divLineDashed" => "1",
			"divlineThickness" => "1",
			"divLineDashLen" => "1",
			"bgAlpha" => "0",
			"canvasBgAlpha" => "0",

			//ScrollColumn2D
			"numVisiblePlot" => "30",
			"scrollheight" => "7",
			"flatScrollBars" => "1",
			"scrollShowButtons" => "0",
			"scrollColor" => "#cccccc",
			"showHoverEffect" => "1",
			"showborder" => "0",
			"showplotborder" => "0",
			"showcanvasborder" => "0",
			"scrollPadding" => "5",
			"usePlotGradientColor" => "0",

		)
	);

	//scrollColumn2d arrays
	$categoryArray = array();
	$dataArray = array();

	// Push the data into the array
	while ($row = mysqli_fetch_array($result)) {

		array_push(
			$categoryArray,
			array(
				"label" => date("d/m H:i", strtotime($row['created']))
			)
		);

		array_push(
			$dataArray,
			array(
				"value" => number_format($row["hum_temperature"],0)
			)

		);
	}
	//Only for scrollColumn2d
	$arrData["dataset"] = array(array("data" => $dataArray));
	$arrData["categories"] = array(array("category" => $categoryArray));

	$jsonEncodedData = json_encode($arrData);

	$columnChart = new FusionCharts("scrollColumn2d", "chartTemp", 800, 300, "chart-1", "json", $jsonEncodedData);
	// Render the chart
	$columnChart->render();
}
*/
/*****************************************************/
?>