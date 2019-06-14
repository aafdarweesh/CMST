<?php

	include 'resources/db.php';
	$response = [];

	$sql = "SELECT d.property1Value, d.objectName, d.accuracy, s.timeOfAppearance, v.startingTime, m.startingTimeStamp FROM detectedobject as d, sighting as s, video as v, mission as m WHERE d.sightingUrl = s.sightingUrl AND s.videoUrl = v.videoUrl AND v.missionID = m.missionID AND m.startingTimeStamp IS NOT NULL;";
	$result = mysqli_query($conn, $sql);
	$objects = [];
	if(mysqli_num_rows($result) > 0) {
		while ($row = mysqli_fetch_assoc($result)) {
			array_push($objects, $row);
		}
	}
	array_push($response, $objects);

	$sql = "SELECT * FROM mission;";
	$result = mysqli_query($conn, $sql);
	$missions = [];
	if(mysqli_num_rows($result) > 0) {
		while ($row = mysqli_fetch_assoc($result)) {
			array_push($missions, $row);
		}
	}
	array_push($response, $missions);
	
	echo json_encode($response);
?>