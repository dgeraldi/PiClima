<?php
include("dados.php");
     	// If the query returns a valid response, prepare the JSON string
     	if ($result) {
        	// The `$arrData` array holds the chart attributes and data
        	$arrData2 = array(
        	    "chart" => array(
       			"caption" => "Pressao Relativa",
    			"xAxisName" => "Dias/Horas",
        		"yAxisName" => "Pressao hPa",
        		"paletteColors" => "#0075c2",
        		"valueFontColor" => "#000033",
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
				"yAxisMaxValue" => "1030",
				"yAxisMinValue" => "1005",
				"decimals" => "0",
		        "thousandSeparator" => ".",
				"formatNumberScale" => "0",
				"showvalues" => "1",
				"showborder" => "0",
				"showcanvasborder" =>"0",
				"showAlternateHGridColor" => "1",
				"bgAlpha" => "0",
				"canvasBgAlpha"=> "0",

				//scrollArea2D
				"numVisiblePlot"=> "30",
				"scrollheight"=> "7",
          		"flatScrollBars"=> "1",
           		"scrollShowButtons"=> "0",
            	"scrollColor"=> "#cccccc",
            	"showHoverEffect"=> "1",
				"showborder" => "0",
				"showplotborder" => "0",
				"showcanvasborder" => "0",
				"scrollPadding" => "5",
				"usePlotGradientColor" => "0",
             	)
           	);

        	//Area2d array
        	//$arrData["data"] = array();

			//scrollarea2d arrays
			$categoryArray2 = array();
			$dataArray2 = array();

	// Push the data into the array
        while($row2 = mysqli_fetch_array($result)) 
		{
				//Only for Area2d
          	 	/*array_push($arrData2["data"], array(
             		 	"label" => date("d/m H:i", strtotime($row2['created'])),
              			"value" => $row2["pressure"]
              			)
           		);*/

        	//Only scrollarea2d
			array_push($categoryArray2, array(
					"label" => date("d/m H:i", strtotime($row2['created']))
					)
				 );

				array_push($dataArray2, array(
					"value" => $row2["pressure"]
					)

				);
        }
		    //Only for scrollArea2d
		    $arrData2["dataset"] = array(array("data"=>$dataArray2));
			$arrData2["categories"] = array(array("category"=>$categoryArray2));

        	/*JSON Encode the data to retrieve the string containing the JSON representation of the data in the array. */

        	$jsonEncodedData2 = json_encode($arrData2);

	/*Create an object for the column chart using the FusionCharts PHP class constructor. Syntax for the constructor is ` FusionCharts("type of chart", "unique chart id", width of the chart, height of the chart, "div id to render the chart", "data format", "data source")`. Because we are using JSON data to render the chart, the data format will be `json`. The variable `$jsonEncodeData` holds all the JSON data for the chart, and will be passed as the value for the data source parameter of the constructor.*/

        	$columnChart2 = new FusionCharts("scrollarea2d", "chartPress" , 800, 300, "chart-2", "json", $jsonEncodedData2);

        	// Render the chart
        	$columnChart2->render();

     	}
?>