<?php

	$response = Array();

	include 'resources/db.php';

	$sql = "SELECT * FROM mission ORDER BY missionID DESC;";
	$result = mysqli_query($conn, $sql);
	$missions = [];
	if(mysqli_num_rows($result) > 0) {
		while ($row = mysqli_fetch_assoc($result)) {
			array_push($missions, $row);
		}
	}
	array_push($response, $missions);

	$paths = array();
	for ($i=0; $i < sizeof($missions); $i++) {
		$id = $missions[$i]['pathID'];
		$sql = "SELECT * FROM pathsteps WHERE pathID=$id ORDER BY stepNumber ASC;";
		$result = mysqli_query($conn, $sql);
		$steps = array();
		if(mysqli_num_rows($result) > 0) {
			while ($row = mysqli_fetch_assoc($result)) {
				array_push($steps, array("lat"=>$row['latitude'], "lng"=>$row['longitude']));
			}
		}
		array_push($paths, $steps);
	}
	array_push($response, $paths);

	echo json_encode($response);
?>