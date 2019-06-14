<!DOCTYPE html>
<html>
<head>
	<title>Select New Path</title>
	<link rel="stylesheet" href="css/newPath.css">
	<?php 
		include_once 'resources/commonCSSImport.php';
	?>
	<?php 
		include_once 'resources/constants.php';
	?>
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
			    <a class="nav-link active" href="./newMission.php">New Mission</a>
			  </li>
			  <li class="nav-item dropdown">
			    <a class="nav-link dropdown-toggle" data-toggle="dropdown" href="#" role="button" aria-haspopup="true" aria-expanded="false">Browse Results</a>
			    <div class="dropdown-menu">
			      <a class="dropdown-item" href="./browseResults.php">All Results</a>
			      <a class="dropdown-item" href="./resultsByMission.php">By Mission</a>
			    </div>
			  </li>
			  <li class="nav-item">
			    <a class="nav-link" href="./findingsMap.php">Findings Map</a>
			  </li>
			</ul>
		</div>
	</header>	


	<div id="googleMap" ></div>	
	<div id="GrandParentContainer">
		<table>
			<tr>
				<td><button class="btn btn-dark" id="submitter">Submit</button></td>
				<td><button class="btn btn-dark" id="clearer">Clear</button></td>
			</tr>
		</table>
		<p class="centered">Current distance so far is <span id="distance">0</span> meters</p>
		<p class="centered red" id="error"></p>	
	</div>

	


	
	
	
	<script defer src="https://maps.googleapis.com/maps/api/js?key=YOUR_KEY&callback=myMap"></script>
	
	<script>

		var myTrip = [];
		var markers = [];
		var polylines = [];
		var distance = 0;

		function myMap() {
			var mapProp= {
			  center:new google.maps.LatLng(35.24778877594932, 33.023398253874916),
			  zoom:12
			};

			var map = new google.maps.Map(document.getElementById("googleMap"),mapProp);

			google.maps.event.addListener(map, 'click', function(event) {
			  placeMarker(map, event.latLng);
			  document.getElementById("error").innerHTML = "";
			});

			document.getElementById("clearer").addEventListener("click", function(){
				for (var i = 0; i < markers.length; i++ ) {
					markers[i].setMap(null);
				}
				markers.length = 0;
				myTrip.length = 0;
				for (var i = 0; i < polylines.length; i++ ) {
					polylines[i].setMap(null);
				}
				polylines.length = 0;
				distance = 0;
				document.getElementById("distance").innerHTML = distance;
				document.getElementById("error").innerHTML = "";
			});

			document.getElementById("submitter").addEventListener("click", function(){
				var height = <?php echo json_encode($_POST["h"], JSON_HEX_TAG); ?>;
				var speed = <?php echo json_encode($_POST["s"], JSON_HEX_TAG); ?>;
				var id = <?php echo json_encode($_POST["droneID"], JSON_HEX_TAG); ?>;
				var length = <?php echo json_encode(LENGTH, JSON_HEX_TAG); ?>;
				var max_time = <?php echo json_encode(MAXTIME, JSON_HEX_TAG); ?>;
				var locations = new Array();
				for (var i = 0; i < myTrip.length; i++) {
					locations.push(
						{
							lat: myTrip[i].lat(),
							lng: myTrip[i].lng()
						}
					);
				}
				if (!(distance > 0)) {
					document.getElementById("error").innerHTML = "Error: path not specified";
				} else if(distance/speed > max_time) {
					document.getElementById("error").innerHTML = "Error: path requirements are impossible to satisfy!";	
				} else {

					var times = new Array();
					for (var i = 0; i < locations.length-1; i++) {
						if(i==0)
							times.push(getDistanceFromLatLonInKm(locations[i]['lat'], locations[i]['lng'], locations[i+1]['lat'], locations[i+1]['lng'])*1000/speed);
						else 
							times.push(times[i-1] + getDistanceFromLatLonInKm(locations[i]['lat'], locations[i]['lng'], locations[i+1]['lat'], locations[i+1]['lng'])*1000/speed);
					}

					
					var numVids = Math.ceil((distance/speed)/length);

					var videoLocations = new Array();

					console.log(times);

					for (var i = 0, j = 0, timer = 0; i < numVids; i++) {
						if(timer>times[j])
							j++;

						var segmentStart = j==0? 0:times[j-1];
						var segmentEnd = times[j];
						var ratio = (segmentEnd - timer) / (segmentEnd - segmentStart);

						videoLocations.push(
							{
								lat: locations[j].lat + (1-ratio) * (locations[j+1].lat - locations[j].lat),
								lng: locations[j].lng + (1-ratio) * (locations[j+1].lng - locations[j].lng)
							}
						);

						timer += length;
					}

					/*for (var i = 0; i < videoLocations.length; i++) {
						placeMarker_test(map, videoLocations[i], i);
					}*/


					


					let request = {
						"newMissionFlag" : true,
						"serialNumber" : id,
						"NumberOfVideos" : numVids,
						"flightConfigurations": {"height": height, "speed": speed, "locations": locations, "videoLocations": videoLocations}
					};
					var xmlhttp = new XMLHttpRequest();   // new HttpRequest instance
					xmlhttp.onreadystatechange = function() {
					    if (xmlhttp.readyState == XMLHttpRequest.DONE) {
					        console.log(xmlhttp.responseText);
					    }
					}
					xmlhttp.open("POST", "SERVER_ADRRESS:PORT/assignNewMission");
					xmlhttp.setRequestHeader("Content-Type", "application/json");
					xmlhttp.send(JSON.stringify(request));

					$(location).attr('href', './resultsByMission.php');

				}
			});




		}	

		function placeMarker_test(map, location, order) {
		  var marker = new google.maps.Marker({
		    position: location,
		    map: map,
		    icon: 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=' + order + '|FE6256|000000'
		  });
		  
		}	

		function placeMarker(map, location) {
		  var marker = new google.maps.Marker({
		    position: location,
		    map: map
		  });
		  //map.panTo(location);
		  markers.push(marker);
		  myTrip.push(location);
		  var flightPath = new google.maps.Polyline({
		  	path:myTrip,
		  	strokeColor:"#0000FF",
		  	strokeOpacity:0.8,
		  	strokeWeight:2
		  });
		  flightPath.setMap(map);
		  polylines.push(flightPath);

		  if(myTrip.length > 1) {
		  	distance += Math.round(getDistanceFromLatLonInKm(myTrip[myTrip.length - 2].lat(), myTrip[myTrip.length - 2].lng(), myTrip[myTrip.length - 1].lat(), myTrip[myTrip.length - 1].lng()) * 1000);
		  	document.getElementById("distance").innerHTML = distance;
		  }
		}

		//https://stackoverflow.com/questions/18883601/function-to-calculate-distance-between-two-coordinates
		function getDistanceFromLatLonInKm(lat1, lon1, lat2, lon2) {
		  var R = 6371; // Radius of the earth in km
		  var dLat = deg2rad(lat2-lat1);  // deg2rad below
		  var dLon = deg2rad(lon2-lon1); 
		  var a = 
		    Math.sin(dLat/2) * Math.sin(dLat/2) +
		    Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) * 
		    Math.sin(dLon/2) * Math.sin(dLon/2)
		    ; 
		  var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a)); 
		  var d = R * c; // Distance in km
		  return d;
		}

		function deg2rad(deg) {
		  return deg * (Math.PI/180)
		}



		
	</script>
	

	<?php 
		include_once 'resources/bottom.php';
	?>

</body>
</html>