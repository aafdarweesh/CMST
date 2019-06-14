<!DOCTYPE html>
<html>
<head>
	<title>Findings Map</title>
	<link rel="stylesheet" href="css/newPath.css">
	<link rel="stylesheet" href="css/findingsMap.css">
	<?php 
		include_once 'resources/commonCSSImport.php';
	?>
	<?php 
		include_once 'resources/constants.php';
	?>
	<?php 
		include_once 'resources/db.php';
	?>
	<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
</head>
<body>
	
	<div id="page-container">
	<div id="content-wrap">

	<?php 
		include_once 'resources/wallpaper.php';
	?>

	<header class="centered">
	  <a href="./index.php"><img src="./resources/logo.jpg"/></a>
	  <div class="centered imageMenu">
		  <ul class="nav nav-tabs">
		  	  <li class="nav-item">
			    <a class="nav-link" href="./index.php">Home</a>
			  </li>
			  <li class="nav-item">
			    <a class="nav-link" href="./newMission.php">New Mission</a>
			  </li>
			  <li class="nav-item dropdown">
			    <a class="nav-link dropdown-toggle" data-toggle="dropdown" href="#" role="button" aria-haspopup="true" aria-expanded="false">Browse Results</a>
			    <div class="dropdown-menu">
			      <a class="dropdown-item" href="./browseResults.php">All Results</a>
			      <a class="dropdown-item" href="./resultsByMission.php">By Mission</a>
			    </div>
			  </li>
			  <li class="nav-item">
			    <a class="nav-link active" href="./findingsMap.php">Findings Map</a>
			  </li>
			</ul>
		</div>
	</header>

	<div class="centered"><div class="titler"><h1>Findings Map</h1></div></div>




	<?php

		function getStuff($url){

			include 'resources/db.php';

			$sql = "SELECT * FROM sighting WHERE sightingUrl=\"$url\" ;";
			$result = mysqli_query($conn, $sql);
			if(mysqli_num_rows($result) > 0) {
				while ($row = mysqli_fetch_assoc($result)) {
					$sighting = $row;
				}
			}

			$videoUrl = $sighting['videoUrl'];
			$sql = "SELECT * FROM video WHERE videoUrl=\"$videoUrl\" ;";
			$result = mysqli_query($conn, $sql);
			if(mysqli_num_rows($result) > 0) {
				while ($row = mysqli_fetch_assoc($result)) {
					$video = $row;
				}
			}

			$missionID = $video['missionID'];
			$sql = "SELECT * FROM mission WHERE missionID=\"$missionID\" ;";
			$result = mysqli_query($conn, $sql);
			if(mysqli_num_rows($result) > 0) {
				while ($row = mysqli_fetch_assoc($result)) {
					$mission = $row;
				}
			}


			$sql = "SELECT v2.latitude, v2.longitude FROM video as v1, video as v2 WHERE v1.missionID=v2.missionID AND v1.videoUrl=\"$videoUrl\" AND v2.startingTime > v1.startingTime ORDER BY v2.startingTime ASC;";
			$result = mysqli_query($conn, $sql);
			if(mysqli_num_rows($result) > 0) {
				$nextloc = mysqli_fetch_assoc($result);
			} else {
				$ya = "path";
				$sql = "SELECT p.latitude, p.longitude FROM mission as m, pathsteps as p, $ya as g WHERE m.pathID=p.pathID AND m.pathID=g.pathID AND m.missionID=\"$missionID\" AND p.stepNumber = g.numberOfSteps;";
				$result = mysqli_query($conn, $sql);
				if(mysqli_num_rows($result) > 0) {
					while ($row = mysqli_fetch_assoc($result)) {
						$nextloc = $row;
					}
					
				}
			}
			$result = array("sighting"=> $sighting, "video" => $video, "nextloc" => $nextloc);
			return $result;
		}

		function getAllStuff() {
			include 'resources/db.php';
			$sql = "SELECT * FROM sighting;";
			$result = mysqli_query($conn, $sql);
			$sightings = [];
			if(mysqli_num_rows($result) > 0) {
				while ($row = mysqli_fetch_assoc($result)) {
					array_push($sightings, $row);
				}
			}
			$result = [];
			for($i = 0; $i < sizeof($sightings); $i++) {
				array_push($result, getStuff($sightings[$i]['sightingUrl']));
			}
			return $result;
		}

	?>


	<div id="googleMap" style="margin: 10px auto;"></div>

	<div class="statsContainer">
		<p>Total number of Missions: <span id="totalMissions"></span></p>
		<p>Total number of detected Turtles: <span id="totalTurtles"></span></p>
		<p>Total number of detected Loggerhead Sea Turtles: <span id="totalLoggerhead"></span></p>
		<p>Total number of detected Green Sea Turtles: <span id="totalGreen"></span></p>
		<div id="PieDiv"></div>
	</div>

	<div class="statsContainer">
		<div class="histo" id="monthsGeneral"></div>
		<div class="histo" id="monthsLoggerhead"></div>
		<div class="histo" id="monthsGreen"></div>
	</div>

	<div class="statsContainer">
		<div class="histo" id="hoursGeneral"></div>
		<div class="histo" id="hoursLoggerhead"></div>
		<div class="histo" id="hoursGreen"></div>
	</div>
	
	<script defer src="https://maps.googleapis.com/maps/api/js?key=YOUR_KEY&callback=MyMap"></script>

	<script>

	
		function MyMap() {

			var map = new google.maps.Map(document.getElementById("googleMap"));

			var result = <?php echo json_encode(getAllStuff()); ?>;
			var length = <?php echo json_encode(LENGTH, JSON_HEX_TAG); ?>;
			latlngbounds = new google.maps.LatLngBounds();

			for (var i = 0; i < result.length; i++) {

				

				var locasion = {
					lat: parseFloat(result[i]['video']['latitude']) + (parseFloat(result[i]['nextloc']['latitude'])-parseFloat(result[i]['video']['latitude'])) * (parseFloat(result[i]['sighting']['timeOfAppearance']) / length),
					lng: parseFloat(result[i]['video']['longitude']) + (parseFloat(result[i]['nextloc']['longitude'])-parseFloat(result[i]['video']['longitude'])) * (parseFloat(result[i]['sighting']['timeOfAppearance']) / length)
				};

				
				var url = result[i]['sighting']['sightingUrl'];
							

				placeMarker(map, locasion, "", url);

				
				latlngbounds.extend(locasion);
				map.fitBounds(latlngbounds);
			}



		}	

		function placeMarker(map, location, order, sightingUrl) {

			var marker = new google.maps.Marker({
				position: location,
				map: map,
				icon: 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=' + order + '|FE6256|000000'
			});

			marker.addListener("click", function() {
		    	var url_to = './frame.php';
		        var form = $('<form action="' + url_to + '" method="post">' +
		          '<input type="text" name="frame" value=\"' + sightingUrl + '\" />' +
		          'type="hidden" </form>');
		        $('body').append(form);
		        form.submit();
		    });

		}


	</script>

	<script type="text/javascript">
		$.ajax({
			type: "POST",
			url: "./stats.php", 
			dataType: "json",
			error: function(){
				console.log("failure");
			},
			success: function(data) {

				var nMissions = data[1].length;
				var nTurtles = data[0].length;
				var Loggerheads = [];
				var Greens = [];
				for (var i = 0; i < data[0].length; i++) {
					if(data[0][i]['property1Value'].valueOf() === "Loggerhead")
						Loggerheads.push(data[0][i]);
					else
						Greens.push(data[0][i]);
				}
				document.getElementById("totalMissions").innerHTML = nMissions;
				document.getElementById("totalTurtles").innerHTML = nTurtles;
				document.getElementById("totalLoggerhead").innerHTML = Loggerheads.length;
				document.getElementById("totalGreen").innerHTML = Greens.length;

				var pie = [{
				  values: [Number((Loggerheads.length/nTurtles).toFixed(2)), Number((Greens.length/nTurtles).toFixed(2))],
				  labels: ['Loggerhead', 'Green'],
				  type: 'pie',
				  marker: {
				    colors: ['rgb(206, 57, 16)', 'rgb(12, 209, 12)']
				  }
				}];

				var layout = {
					title: "Loggerhead vs Green",
				  	font: {size: 11}
				};

				Plotly.newPlot('PieDiv', pie, layout, {responsive: true});

				//https://stackoverflow.com/questions/3075577/convert-mysql-datetime-stamp-into-javascripts-date-format
				Date.createFromMysql = function(mysql_string)
				{ 
				   var t, result = null;

				   if( typeof mysql_string === 'string' )
				   {
				      t = mysql_string.split(/[- :]/);

				      //when t[3], t[4] and t[5] are missing they defaults to zero
				      result = new Date(t[0], t[1] - 1, t[2], t[3] || 0, t[4] || 0, t[5] || 0);          
				   }

				   return result;   
				}

				var generalHours = new Array(24).fill(0);
				var loggerheadHours = new Array(24).fill(0);
				var greenHours = new Array(24).fill(0);

				var generalMonths = new Array(12).fill(0);
				var loggerheadMonths = new Array(12).fill(0);
				var greenMonths = new Array(12).fill(0);

				for (var i = 0; i < Loggerheads.length; i++) {
					var time = Date.createFromMysql(Loggerheads[i]['startingTimeStamp']);
					time.setSeconds(time.getSeconds() + parseInt(Loggerheads[i]['startingTime']) + parseInt(Loggerheads[i]['timeOfAppearance']));
					generalHours[time.getHours()]++;
					generalMonths[time.getMonth()]++;
					loggerheadHours[time.getHours()]++;
					loggerheadMonths[time.getMonth()]++;
				}

				for (var i = 0; i < Greens.length; i++) {
					var time = Date.createFromMysql(Greens[i]['startingTimeStamp']);
					time.setSeconds(time.getSeconds() + parseInt(Greens[i]['startingTime']) + parseInt(Greens[i]['timeOfAppearance']));
					generalHours[time.getHours()]++;
					generalMonths[time.getMonth()]++;
					greenHours[time.getHours()]++;
					greenMonths[time.getMonth()]++;
				}

				function plotMonths(monthsData, title, divID) {

					var data = {
						x: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
						y: monthsData,
						type: 'bar',
						marker: {
							color: 'rgb(49,130,189)',
							opacity: 0.7,
						}
					};

					var layout = {
						title: title,
						xaxis: {
							tickangle: -45,
							title: {
								text: 'Month'
							}
						},
						yaxis: {
							title: {
								text: 'Number of Detected Turtles'
							}
						}
					};

					Plotly.newPlot(divID, [data], layout, {responsive: true});
				}

				plotMonths(generalMonths, "Months Distribution for Detected Turtles", "monthsGeneral");
				plotMonths(loggerheadMonths, "Months Distribution for Detected Turtles (Loggerhead Only)", "monthsLoggerhead");
				plotMonths(greenMonths, "Months Distribution for Detected Turtles (Green Only)", "monthsGreen");


				function plotHours(hoursData, title, divID) {

					var data = {
						x: ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23'],
						y: hoursData,
						type: 'bar',
						marker: {
							color: 'rgb(49,130,189)',
							opacity: 0.7,
						}
					};

					var layout = {
						title: title,
						xaxis: {
							title: {
								text: 'Hour of Day'
							}
						},
						yaxis: {
							title: {
								text: 'Number of Detected Turtles'
							}
						}
					};

					Plotly.newPlot(divID, [data], layout, {responsive: true});
				}

				plotHours(generalHours, "Time of Day Distribution for Detected Turtles", "hoursGeneral");
				plotHours(loggerheadHours, "Time of Day Distribution for Detected Turtles (Loggerhead Only)", "hoursLoggerhead");
				plotHours(greenHours, "Time of Day Distribution for Detected Turtles (Green Only)", "hoursGreen");
				
			}

 		});
	</script>
	

	<?php 
		include_once 'resources/bottom.php';
	?>

</body>
</html>