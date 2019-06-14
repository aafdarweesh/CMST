<!DOCTYPE html>
<html>
<head>
	<title>Home</title>
	<?php 
		include_once 'resources/commonCSSImport.php';
	?>
	<link rel="stylesheet" href="css/index_s.css">
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
			    <a class="nav-link active" href="./index.php">Home</a>
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

	
	<div class="imagesMenuContainer">
		<div class="row"> 
		  <div class="column">
		    <a href="./newMission.php"><img src="./resources/drone_new.png"></a>
		  </div>
		  <div class="column">
		    <a href="./browseResults.php"><img src="./resources/all_new.png"></a>
		  </div>
		  <div class="column">
		    <a href="./resultsByMission.php"><img src="./resources/missionic_new.png"></a>
		  </div>
		  <div class="column">
		    <a href="./findingsMap.php"><img src="./resources/map_new.png"></a>
		  </div> 
		</div>
	</div>
	


	<?php 
		include_once 'resources/bottom.php';
	?>
</body>
</html>