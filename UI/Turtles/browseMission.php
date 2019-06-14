<?php 
	include_once 'resources/db.php';
?>
<!DOCTYPE html>
<html>
<head>
	<title>Results by Mission</title>
	<?php 
		include_once 'resources/commonCSSImport.php';
	?>
	<link rel="stylesheet" href="css/browseResults.css">
	<link rel="stylesheet" href="./notify/jquery.notify.css">
	<link rel="stylesheet" href="./notify/jquery.notify.fonts.css">
	<script src="./notify/jquery.notify.js"></script>
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
			      <a class="dropdown-item" href="./browseResults.php">All Results</a>
			      <a class="dropdown-item active" href="./resultsByMission.php">By Mission</a>
			    </div>
			  </li>
			  <li class="nav-item">
			    <a class="nav-link" href="./findingsMap.php">Findings Map</a>
			  </li>
			</ul>
		</div>
	</header>


	<?php

		$m = -1;

		if(isset($_GET["m"]) && ctype_digit($_GET['m'])) {
			$m = (int)$_GET["m"];
			echo "<div class=\"centered\"><div class=\"titler\"><h1>Mission $m Results</h1></div></div>";
		} else {
			echo "<div class=\"centered\"><div class=\"titler\"><h1>Mission ID not passed properly</h1></div></div>";	
		}

	?>



	

	<div class="centered">
		<div class="btn-group" role="group" aria-label="Basic example">
		  <button type="button" onclick="openTab(event, 'videosTab')" class="btn btn-secondary">Videos</button>
		  <button type="button" onclick="openTab(event, 'imagesTab')" class="btn btn-secondary">Sightings</button>
		</div>
	</div>
	<div class="contentContainer" id="videosTab"></div>
	
	<div class="contentContainer" id="imagesTab"></div>

	<script type="text/javascript" src="browseResults.js"></script>

	<script type="text/javascript">

		var currentCount = {
			videos: -1,
			sightings: -1
		};
		
		var finished = false;

		function get_Data_and_Populate() {
			$.ajax({
				type: "POST",
				url: "./missionStuff.php",
				data: {"m" : missionID}, 
				dataType: "json",
				error: function(){
					console.log("failure");
				},
				success: function(data) {

					newVideosCount = data[0].length;
					newSightingsCount = data[1].length;

					if(currentCount.videos == -1 || currentCount.sightings == -1) {

						loadStuff(data[0], "videosTab"); 
						loadStuff(data[1], "imagesTab");
						if(data[2].length != 0 && data[2][0]['state'].valueOf() === "2")
						{
							finished = true;
						}

					} else {

						videoDiff = newVideosCount - currentCount.videos;
						sightingDiff = newSightingsCount - currentCount.sightings;

						if(videoDiff > 0) {
							for (var i = 0; i < videoDiff; i++) {
								addElement("videosTab", (i+currentCount.videos)%3, data[0][data[0].length - 1 - i]);
								$.notify({
									title: "Mission " + missionID,
									body: "A new video has been received",
									timeout: 5000
								});
							}
						}

						if(sightingDiff > 0) {
							for (var i = 0; i < sightingDiff; i++) {
								addElement("imagesTab", (i+currentCount.sightings)%3, data[1][data[1].length - 1 - i]);
								$.notify({
									title: "Mission " + missionID,
									body: "A new sighting has been received",
									timeout: 5000
								});
							}
						}
						
						if(data[2].length != 0 && data[2][0]['state'].valueOf() === "2" && finished == false)
						{
							finished = true;
							$.notify({
								title: "Mission " + missionID,
								body: "The mission has finished",
								timeout: 5000
							});
						}
						

					}


					currentCount.videos = newVideosCount;
					currentCount.sightings = newSightingsCount;

					setTimeout(get_Data_and_Populate, 3000);
					 
				}

	 		});
		}

		var missionID = <?php echo json_encode($m, JSON_HEX_TAG); ?>;
		if(missionID != -1) {
		    get_Data_and_Populate();
		}
	    
 	</script>



	<?php 
		include_once 'resources/bottom.php';
	?>
</body>
</html>