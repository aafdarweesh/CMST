<?php 
	include_once 'resources/db.php';
?>
<!DOCTYPE html>
<html>
<head>
	<title>New Mission</title>
	<?php 
		include_once 'resources/commonCSSImport.php';
	?>
	<link rel="stylesheet" href="css/newMission.css">
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

	<?php
		$sql = "SELECT * FROM drone;";
		$result = mysqli_query($conn, $sql);
		if(mysqli_num_rows($result) > 0) {
			$drones = [];
			while ($row = mysqli_fetch_assoc($result)) {
				array_push($drones, $row['droneID']);
			}
		}	
	?>

	<div class="centered">
		<div class="myFormContainer">
			<h3>Enter Trip Parameters:</h3>
			<form action="./newPath.php" method="post">
			  <div class="form-group">
			    <label for="h_id">Height (m):</label>
			    <input name="h" type="number" class="form-control" id="h_id" tabIndex="1" placeholder="Enter the height of the drone" step="any" min="1" max="30" required autoFocus>
			  </div>
			  <div class="form-group">
			    <label for="s_id">Speed (m/s):</label>
			    <input name="s" type="number" class="form-control" id="s_id" tabIndex="1" placeholder="Enter the speed of the drone" step="any" min="0.1" max="10" required>
			  </div>
			  <div class="form-group">
			    <label for="FormControlSelect1">Select Drone/Raspberry Pi</label>
			    <select name="droneID" class="form-control" id="FormControlSelect1" required>
			    	<?php
			    		foreach($drones as $droneID) {
			    			echo("<option>$droneID</option>");
			    		}
			    	?>
			    </select>
			  </div>
			  <button type="submit" name="submit" class="btn btn-dark">Next</button>
			</form>
		<div>
	</div>
	

	<?php 
		include_once 'resources/bottom.php';
	?>
</body>
</html>