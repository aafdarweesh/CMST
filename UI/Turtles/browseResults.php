<?php 
	include_once 'resources/db.php';
?>
<!DOCTYPE html>
<html>
<head>
	<title>Browse Results</title>
	<link rel="stylesheet" href="css/browseResults.css">
	<?php 
		include_once 'resources/commonCSSImport.php';
	?>
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
			    <a class="nav-link active dropdown-toggle" data-toggle="dropdown" href="#" role="button" aria-haspopup="true" aria-expanded="false">Browse Results</a>
			    <div class="dropdown-menu">
			      <a class="dropdown-item active" href="./browseResults.php">All Results</a>
			      <a class="dropdown-item" href="./resultsByMission.php">By Mission</a>
			    </div>
			  </li>
			  <li class="nav-item">
			    <a class="nav-link" href="./findingsMap.php">Findings Map</a>
			  </li>
			</ul>
		</div>
	</header>

	<div class="centered"><div class="titler"><h1>All Results</h1></div></div>
	

	<div class="centered">
		<div class="btn-group" role="group" aria-label="Basic example">
		  <button type="button" onclick="openTab(event, 'videosTab')" class="btn btn-secondary">Videos</button>
		  <button type="button" onclick="openTab(event, 'imagesTab')" class="btn btn-secondary">Sightings</button>
		</div>
	</div>
	<div class="contentContainer" id="videosTab"></div>

	<?php
		$sql = "SELECT * FROM video;";
		$result = mysqli_query($conn, $sql);
		if(mysqli_num_rows($result) > 0) {
			$videos = [];
			while ($row = mysqli_fetch_assoc($result)) {
				array_push($videos, $row['videoUrl']);
			}
		}	
	?>
	
	<div class="contentContainer" id="imagesTab"></div>

	<?php
		$sql = "SELECT * FROM sighting;";
		$result = mysqli_query($conn, $sql);
		if(mysqli_num_rows($result) > 0) {
			$sightings = [];
			while ($row = mysqli_fetch_assoc($result)) {
				array_push($sightings, $row['sightingUrl']);
			}
		}	
	?>

	<script type="text/javascript" src="browseResults.js"></script>
	<script type="text/javascript">
    var jArray = <?php echo json_encode($sightings); ?>;
    loadStuff(jArray, "imagesTab"); 
    var jArray = <?php echo json_encode($videos); ?>;
    loadStuff(jArray, "videosTab"); 
 	</script>

 	 
	<?php 
		include_once 'resources/bottom.php';
	?>
	

</body>
</html>