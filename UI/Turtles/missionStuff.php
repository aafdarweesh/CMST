<?php

	include 'resources/db.php';

	$videos = [];
	$sightings = [];
	$response = [];

	$m = (int)$_POST["m"];
	$sql = "SELECT * FROM video WHERE missionID=$m ORDER BY startingTime ASC;";
	$result = mysqli_query($conn, $sql);
	if(mysqli_num_rows($result) > 0) {
		while ($row = mysqli_fetch_assoc($result)) {
			array_push($videos, $row['videoUrl']);

		}
	}
	array_push($response, $videos);

	$sql = "SELECT * FROM sighting as s, video as v WHERE s.videoUrl=v.videoUrl AND v.missionID=$m ORDER BY v.startingTime ASC, s.timeOfAppearance ASC;";
	$result = mysqli_query($conn, $sql);
	if(mysqli_num_rows($result) > 0) {
		while ($row = mysqli_fetch_assoc($result)) {
			array_push($sightings, $row['sightingUrl']);
		}
	}
	array_push($response, $sightings);

	echo json_encode($response);
?>