<?php 
	include_once 'resources/db.php';
?>
<!DOCTYPE html>
<html>
<head>
	<title>All Missions</title>
	<script  src="https://maps.googleapis.com/maps/api/js?key=YOUR_KEY"></script>
	<?php 
		include_once 'resources/commonCSSImport.php';
	?>
	<link rel="stylesheet" href="css/resultsByMission.css">
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
	

	<div class="centered"><div class="titler"><h1>All Missions</h1></div></div>

	<div id="daddy"></div>

	

	<script type="text/javascript">


		function placeMarker(map, location, order) {
		  var marker = new google.maps.Marker({
		    position: location,
		    map: map,
		    icon: 'http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=' + order + '|FE6256|000000'
		  });
		}

		function renderOneMap(path, mission) {

			var map = new google.maps.Map(document.getElementById("googleMap" + mission['missionID']));

			for (var j = 0; j < path.length; j++) {
				placeMarker(map, path[j], j+1);
			}

			var polyline = new google.maps.Polyline({
				path:path,
				strokeColor:"#0000FF",
				strokeOpacity:0.8,
				strokeWeight:2
			});
			polyline.setMap(map);

			var latlngbounds = new google.maps.LatLngBounds();
			for (var k = 0; k < path.length; k++) {
			    latlngbounds.extend(path[k]);
			}
			map.fitBounds(latlngbounds);

		}

		function floatifyPath(path_old) {
			path = new Array(path_old.length);
			for (var j = 0; j < path_old.length; j++) {
				path[j] = {lat: parseFloat(path_old[j]['lat']), lng: parseFloat(path_old[j]['lng'])};
			}
			return path;
		}

		function RenderMaps(paths_old, missions) {

			paths = new Array(paths_old.length);

			for (var i = 0; i < paths_old.length; i++) {
				paths[i] = floatifyPath(paths_old[i]);
			}

			for (var i = 0; i < missions.length; i++) {
				renderOneMap(paths[i], missions[i])
			}

		}

		function populateMission(mission, prepend=false) {

			var daddy = document.getElementById("daddy");
			var missionDIV = document.createElement('div');
			missionDIV.className = "missionContainer";
			missionDIV.setAttribute("id", mission['missionID']);

			if(prepend)
				daddy.insertBefore(missionDIV, daddy.firstChild);
			else
				daddy.appendChild(missionDIV);
			
			var subMissionDIV = document.createElement('div');
			subMissionDIV.className = "subMissionContainer";
			missionDIV.appendChild(subMissionDIV);

			var subSubMissionDIV = document.createElement('div');
			subSubMissionDIV.className = "subSubMissionContainer";
			subMissionDIV.appendChild(subSubMissionDIV);

			

			var cell;
			cell = document.createElement('p');
			cell.innerHTML = "Mission ID: " + mission['missionID'];
			subSubMissionDIV.appendChild(cell);

			cell = document.createElement('p');
			cell.innerHTML = "Drone ID: " + mission['droneID'];
			subSubMissionDIV.appendChild(cell);

			var status = mission['state'];
			cell = document.createElement('p');
			cell.innerHTML = "State: ";
			var span = document.createElement('span');
			if(status == 0) {
				span.innerHTML = "Waiting";
				span.setAttribute("style", "background-color: orange; padding: 6px; border-radius:50%;");
			} else if(status == 1) {
				span.innerHTML = "Running";
				span.setAttribute("style", "background-color: red; padding: 6px; border-radius:50%;");
			} else {
				span.innerHTML = "Finished";
				span.setAttribute("style", "background-color: green; padding: 6px; border-radius:50%;");
			}
			cell.appendChild(span);
			subSubMissionDIV.appendChild(cell);

			if(status > 0) {
				cell = document.createElement('p');
				cell.innerHTML = "Starting Timestamp: " + mission['startingTimeStamp'];
				subSubMissionDIV.appendChild(cell);
			}

			if(status > 1) {
				cell = document.createElement('p');
				cell.innerHTML = "Ending Timestamp: " + mission['endingTimeStamp'];
				subSubMissionDIV.appendChild(cell);
			}


			var mapdiv = document.createElement('div');
			mapdiv.className = "pathMap";
			mapdiv.setAttribute("id", "googleMap" + mission['missionID']);
			subMissionDIV.appendChild(mapdiv);

			var btndiv = document.createElement('div');
			btndiv.className = "centered";
			button = document.createElement('button');
			button.className = "btn btn-dark";
			button.innerHTML = "Results";
			var link = document.createElement('a');
			link.href = "./browseMission.php?m=" + mission['missionID'];
			link.appendChild(button);
			if(status == 0) {
				button.className += " disabled";
				link.className = "disabledAnchor";
			}
			btndiv.appendChild(link);
			missionDIV.appendChild(btndiv);

		}

		function populate(response) {
			
			
	 		var missions = response[0];
	 		var paths_old = response[1];
			
			for (var i = 0; i < missions.length; i++) {
				populateMission(missions[i]);
			}

			RenderMaps(paths_old, missions);
		}	

		var states = {
			waiting: -1,
			running: -1,
			finished: -1,
			lastMissionId: -1,
			getSum: function() {
				return this.waiting + this.running + this.finished;
			},
			getStates: function() {
				return [this.waiting , this.running , this.finished];
			},
			setStates: function(newStates) {
				this.waiting = newStates[0];
				this.running = newStates[1];
				this.finished = newStates[2];
			}
		}

		function classifyMissions(missions) {
			var waiting = [];
			var running = [];
			var finished = [];
			for (var i = 0; i < missions.length; i++) {
				if(missions[i]['state'] == '0')
					waiting.push(missions[i]);
				else if(missions[i]['state'] == '1')
					running.push(missions[i]);
				else
					finished.push(missions[i]);
			}
			return [waiting, running, finished];
		}

		function getData_and_populate(renderedMissions) {
			$.ajax({
				type: "POST",
				url: "./byMission.php",
				dataType: "json",
				error: function(){
					console.log("failure");
				},
				success: function(data) {

					var waiting = [];
					var running = [];
					var finished = [];

					var lastMissionId = -1;

					for (var i = 0; i < data[0].length; i++) {

						if(data[0][i]['state'] == '0') {
							waiting.push({
								m: data[0][i],
								p: data[1][i]
							});
						}
						else if(data[0][i]['state'] == '1') {
							running.push({
								m: data[0][i],
								p: data[1][i]
							});
						}
						else {
							finished.push({
								m: data[0][i],
								p: data[1][i]
							});
						}

						if(parseInt(data[0][i]['missionID']) > lastMissionId)
							lastMissionId = parseInt(data[0][i]['missionID']);

					}

					classifiedMissions = [waiting, running, finished];
					classifiedMissions_reserved = [waiting.slice(), running.slice(), finished.slice()];

					if(states.getSum() >= 0) {

						var newMissionsCount = (classifiedMissions[0].length + classifiedMissions[1].length + classifiedMissions[2].length) - states.getSum();
						if(newMissionsCount > 0) {
							newMissions = [];
							for (var i = 0; i < classifiedMissions.length; i++) {
								for (var j = 0; j < classifiedMissions[i].length; j++) {
									if(parseInt(classifiedMissions[i][j]['m']['missionID']) > states.lastMissionId) {
										newMissions.push(classifiedMissions[i][j]);
										classifiedMissions[i].splice(j, 1);
									}
								}
							}
							for (var i = 0; i < newMissions.length; i++) {
								populateMission(newMissions[i]['m'], true);
								renderOneMap(floatifyPath(newMissions[i]['p']), newMissions[i]['m']);
								$.notify({
									body: "Mission " + newMissions[i]['m']['missionID'] + " has been added",
									timeout: 5000
								});
							}
						} 

						var started = states.waiting - classifiedMissions[0].length;
						if(started > 0) {
							var startedMissions = [];
							var justFinishedMissions = [];
							for (var i = 0; i < renderedMissions[0].length; i++) {
								var matched = false;
								for (var j = 0; j < classifiedMissions[0].length; j++) {
									if(classifiedMissions[0][j]['m']['missionID'].valueOf() == renderedMissions[0][i]['m']['missionID'].valueOf()) {
										matched = true;
										break;
									}
								}
								if(matched == false) {
									
									var found = false;
									for (var j = 0; j < classifiedMissions[1].length; j++) {
										if(classifiedMissions[1][j]['m']['missionID'].valueOf() == renderedMissions[0][i]['m']['missionID'].valueOf()) {
											startedMissions.push(classifiedMissions[1][j]);
											classifiedMissions[1].splice(j, 1);
											found = true;
											break;
										}
									}

									if(found == false) {
										for (var j = 0; j < classifiedMissions[2].length; j++) {
											if(classifiedMissions[2][j]['m']['missionID'].valueOf() == renderedMissions[0][i]['m']['missionID'].valueOf()) {
												justFinishedMissions.push(classifiedMissions[2][j]);
												break;
											}
										}
									}

								}
							}
							for (var i = 0; i < startedMissions.length; i++) {
								document.getElementById(startedMissions[i]['m']['missionID']).querySelector("span").innerHTML = "Running";
								document.getElementById(startedMissions[i]['m']['missionID']).querySelector("span").style = "background-color: red; padding: 6px; border-radius:50%;";
								cell = document.createElement('p');
								cell.innerHTML = "Starting Timestamp: " + startedMissions[i]['m']['startingTimeStamp'];
								document.getElementById(startedMissions[i]['m']['missionID']).querySelector(".subSubMissionContainer").appendChild(cell);
								document.getElementById(startedMissions[i]['m']['missionID']).querySelector(".btn").classList.remove("disabled");
								document.getElementById(startedMissions[i]['m']['missionID']).querySelector(".disabledAnchor").className = "";
								$.notify({
									body: "Mission " + startedMissions[i]['m']['missionID'] + " has started",
									timeout: 5000
								});
							}
							for (var i = 0; i < justFinishedMissions.length; i++) {
								document.getElementById(justFinishedMissions[i]['m']['missionID']).querySelector("span").innerHTML = "Finished";
								document.getElementById(justFinishedMissions[i]['m']['missionID']).querySelector("span").style = "background-color: green; padding: 6px; border-radius:50%;";
								cell = document.createElement('p');
								cell.innerHTML = "Starting Timestamp: " + justFinishedMissions[i]['m']['startingTimeStamp'];
								document.getElementById(justFinishedMissions[i]['m']['missionID']).querySelector(".subSubMissionContainer").appendChild(cell);
								cell = document.createElement('p');
								cell.innerHTML = "Ending Timestamp: " + justFinishedMissions[i]['m']['endingTimeStamp'];
								document.getElementById(justFinishedMissions[i]['m']['missionID']).querySelector(".subSubMissionContainer").appendChild(cell);
								document.getElementById(justFinishedMissions[i]['m']['missionID']).querySelector(".btn").classList.remove("disabled");
								document.getElementById(justFinishedMissions[i]['m']['missionID']).querySelector(".disabledAnchor").className = "";
								$.notify({
									body: "Mission " + justFinishedMissions[i]['m']['missionID'] + " has finished",
									timeout: 5000
								});
							} 

						}
						
						var justFinished = states.running - classifiedMissions[1].length;
						if(justFinished > 0) {
							var justFinishedMissions = [];
							for (var i = 0; i < renderedMissions[1].length; i++) {
								var matched = false;
								for (var j = 0; j < classifiedMissions[1].length; j++) {
									if(classifiedMissions[1][j]['m']['missionID'].valueOf() == renderedMissions[1][i]['m']['missionID'].valueOf()) {
										matched = true;
										break;
									}
								}
								if(matched == false) {
									for (var j = 0; j < classifiedMissions[2].length; j++) {
										if(classifiedMissions[2][j]['m']['missionID'].valueOf() == renderedMissions[1][i]['m']['missionID'].valueOf()) {
											justFinishedMissions.push(classifiedMissions[2][j]);
											break;
										}
									}
								}
							}
							for (var i = 0; i < justFinishedMissions.length; i++) {
								document.getElementById(justFinishedMissions[i]['m']['missionID']).querySelector("span").innerHTML = "Finished";
								document.getElementById(justFinishedMissions[i]['m']['missionID']).querySelector("span").style = "background-color: green; padding: 6px; border-radius:50%;";
								cell = document.createElement('p');
								cell.innerHTML = "Ending Timestamp: " + justFinishedMissions[i]['m']['endingTimeStamp'];
								document.getElementById(justFinishedMissions[i]['m']['missionID']).querySelector(".subSubMissionContainer").appendChild(cell);
								$.notify({
									body: "Mission " + justFinishedMissions[i]['m']['missionID'] + " has finished",
									timeout: 5000
								});
							} 
						}

					} else {
						populate(data);
					}

					states.setStates([classifiedMissions_reserved[0].length, classifiedMissions_reserved[1].length, classifiedMissions_reserved[2].length]); 
					states.lastMissionId = lastMissionId;
					setTimeout(function(){
						getData_and_populate(classifiedMissions_reserved);
					}, 3000);
				}

	 		});
		}

		getData_and_populate([]);
		
	</script>


	<?php 
		include_once 'resources/bottom.php';
	?>


</body>
</html>