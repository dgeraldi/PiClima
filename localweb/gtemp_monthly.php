<?php
include("fusioncharts.php");
include("dados.php");

// If the query returns a valid response, prepare the JSON string
if ($result) {
	// The `$arrData` array holds the chart attributes and data
	$arrDataMonthly = array(
		"chart" => array(
			"caption" => "Temperatura",
			"xAxisName" => "Mês",
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

	$categoryArrayMontly = array();
	$dataArrayMonthly = array();

	// Push the data into the array
	while ($rowMontly = mysqli_fetch_array($result)) {
		
		//Only scrollColumn2d
		array_push(
			$categoryArrayMonthly,
			array(
				"label" => date("m", strtotime($rowMontly['created']))
			)
		);

		array_push(
			$dataArrayMonthly,
			array(
				"seriesname"=> date("y", strtotime($rowMontly['created'])),
				"value" => $rowMontly["hum_temperature"]
			)

		);
	}
	//Only for scrollColumn2d
	$arrDataMonthly["dataset"] = array(array("data" => $dataArrayMonthly));
	$arrDataMonthly["categories"] = array(array("category" => $categoryArrayMonthly));

	/*JSON Encode the data to retrieve the string containing the JSON representation of the data in the array. */
	$jsonEncodedDataMonthly = json_encode($arrDataMonthly);

	/*Create an object for the column chart using the FusionCharts PHP class constructor. Syntax for the constructor is ` FusionCharts("type of chart", "unique chart id", width of the chart, height of the chart, "div id to render the chart", "data format", "data source")`. Because we are using JSON data to render the chart, the data format will be `json`. The variable `$jsonEncodeData` holds all the JSON data for the chart, and will be passed as the value for the data source parameter of the constructor.*/

	$columnChartMonthly = new FusionCharts("scrollColumn2d", "chartTemp", 800, 300, "chart-1", "json", $jsonEncodedDataMonthly);
	// Render the chart
	$columnChartMonthly->render();
}
?>