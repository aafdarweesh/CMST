<?php 
	include_once 'resources/db.php';
?>
<!DOCTYPE html>
<html>
<head>
	<title>Sighting Details</title>
	<?php 
		include_once 'resources/commonCSSImport.php';
	?>
	<?php 
		include_once 'resources/constants.php';
	?>
	<link rel="stylesheet" href="css/frame.css">
</head>
<body>
	<?php 
		include_once 'resources/top.php';
	?>

	<?php 
		include_once 'resources/wallpaper.php';
	?>

	<header class="centered">
	  <a href="./index.php"><img src="./resources/logo.jpg"/></a>
	  <div class="centered">
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
			    <a class="nav-link" href="./findingsMap.php">Findings Map</a>
			  </li>
			</ul>
		</div>
	</header>

	<div class="centered"><div class="titler"><h1>Sighting Details</h1></div></div>
	<div id="daddy">
		
	</div>

	<?php
		$url = $_POST['frame'];
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

		$sql = "SELECT * FROM detectedobject WHERE sightingUrl=\"$url\" ;";
		$result = mysqli_query($conn, $sql);
		if(mysqli_num_rows($result) > 0) {
			$objects = [];
			while ($row = mysqli_fetch_assoc($result)) {
				array_push($objects, $row);
			}
		}
	?>

	<script type="text/javascript">
		var sighting = <?php echo json_encode($sighting); ?>;
		var video = <?php echo json_encode($video); ?>;
		var mission = <?php echo json_encode($mission); ?>;
		var objects = <?php echo json_encode($objects); ?>;
		var nextloc = <?php echo json_encode($nextloc); ?>;
		var length = <?php echo json_encode(LENGTH, JSON_HEX_TAG); ?>;

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

		var time = Date.createFromMysql(mission['startingTimeStamp']);
		time.setSeconds(time.getSeconds() + parseInt(video['startingTime']) + parseInt(sighting['timeOfAppearance']));

		var locasion = {
			lat: parseFloat(video['latitude']) + (parseFloat(nextloc['latitude'])-parseFloat(video['latitude'])) * (parseFloat(sighting['timeOfAppearance']) / length),
			lng: parseFloat(video['longitude']) + (parseFloat(nextloc['longitude'])-parseFloat(video['longitude'])) * (parseFloat(sighting['timeOfAppearance']) / length)
		};

		var daddy = document.getElementById('daddy');

		var cell = document.createElement('p');
		cell.innerHTML = "Mission ID: " + mission['missionID'];
		daddy.appendChild(cell);

		cell = document.createElement('p');
		cell.innerHTML = "Estimated Capturing Timestamp: " + time;
		daddy.appendChild(cell);

		for (var i = 0; i < objects.length; i++) {
			cell = document.createElement('img');
			cell.src = "./" + objects[i]["url"];
			cell.setAttribute("style", "width: 30%; height: 30%;")
			daddy.appendChild(cell);
			cell = document.createElement('p');
			cell.innerHTML = objects[i]['property1Value'] + " " + objects[i]['objectName'] + " (" + objects[i]['accuracy'] + ")";
			daddy.appendChild(cell);
		}
		

		var cell = document.createElement('p');
		cell.innerHTML = "Estimated Location: ";
		daddy.appendChild(cell);

		var cell = document.createElement('div');
		cell.setAttribute("id", "googleMap");
		daddy.appendChild(cell);

		cell = document.createElement('p');
		cell.innerHTML = "Original Video: ";
		daddy.appendChild(cell);

		media = document.createElement('video');
	    media.controls = true;
	    src = document.createElement('source');
	    src.src = "./" + video['videoUrl'];
	    src.type = "video/mp4";
	    media.appendChild(src);
	    media.setAttribute("style", "width: 50%; height: 50%;")
	    daddy.appendChild(media);

	</script>

	<script defer src="https://maps.googleapis.com/maps/api/js?key=YOUR_KEY&callback=MyMap"></script>

	<script>

	
		function MyMap() {

			var mapProp= {
			  center:new google.maps.LatLng(35.24778877594932, 33.023398253874916),
			  zoom:12
			};

			var map = new google.maps.Map(document.getElementById("googleMap"),mapProp);

			placeMarker(map, locasion, ""/*"picture (seconds elapsed: " + sighting['timeOfAppearance'] + " out of 10)"*/);
			/*let first = {
				lat: parseFloat(video['latitude']),
				lng: parseFloat(video['longitude'])
			};
			let second = {
				lat: parseFloat(nextloc['latitude']),
				lng: parseFloat(nextloc['longitude'])
			};
			placeMarker(map, first, "its video starting location");
			placeMarker(map, second, "next video (or last path point)");
			var flightPath = new google.maps.Polyline({
				path:[first, second],
				strokeColor:"#0000FF",
				strokeOpacity:0.8,
				strokeWeight:2
			});
			flightPath.setMap(map);*/


			var latlngbounds = new google.maps.LatLngBounds();
			latlngbounds.extend(locasion);
			map.fitBounds(latlngbounds);

		}	

		function placeMarker(map, location, order) {
		  var marker = new google.maps.Marker({
		    position: location,
		    map: map,
		    icon: 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=' + order + '|FE6256|000000'
		  });
		  
		}


		
	</script>

	<?php 
		include_once 'resources/bottom.php';
	?>

</body>
</html>