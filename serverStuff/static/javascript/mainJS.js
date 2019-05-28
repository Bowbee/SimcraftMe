function submitButton(){ // submit button for Simple Sim
	var x = document.getElementById("loadScreen");
    if (x.style.display === "") {
        x.style.display = "block";   
    }
	var xhr = new XMLHttpRequest();
	var url = "api/1/sim";
	xhr.open("POST", url, true);
	xhr.setRequestHeader("Content-Type", "application/json");
	xhr.onreadystatechange = function () { // callback function, what to do when we get a reply
	    if (xhr.readyState === 4 && xhr.status === 200) {
	        var reportID = JSON.parse(xhr.responseText);
	        var rID = reportID['ReportID'];
	        statusCheck(rID);
	    }
	};
	var region = document.getElementById("realmSelect").value;
	var realm = document.getElementById("serverInput").value;
	var character = document.getElementById("characterInput").value;
	var data = JSON.stringify({
		"region":region,
		"realm": realm,
		"character":character
	});
	console.log(data)
	xhr.send(data);
}

function advSubmitButton(){ // submit button for Advanced Sim
	var x = document.getElementById("loadScreen");
    if (x.style.display === "") {
        x.style.display = "block";   
    }
	var xhr = new XMLHttpRequest();
	var url = "api/1/sim";
	xhr.open("POST", url, true);
	xhr.setRequestHeader("Content-Type", "application/json");
	xhr.onreadystatechange = function () { // callback function, what to do when we get a reply
	    if (xhr.readyState === 4 && xhr.status === 200) {
	        var reportID = JSON.parse(xhr.responseText);
	        var rID = reportID['ReportID'];
	        statusCheck(rID);
	    }
	};
	var simString = document.getElementById("simEntry").value;
	var data = JSON.stringify({
		"simString":simString
	});
	console.log(data)
	xhr.send(data);
}

function statusCheck(rID){ // make and wait for reply for status, if complete, redirect to report.html, if failed, redirect to failed, else wait for complete or failed
	var xhr = new XMLHttpRequest();
	var url = "api/1/status";
	xhr.open("POST", url, true);
	xhr.setRequestHeader("Content-Type", "application/json");
	xhr.onreadystatechange = function () {
	    if (xhr.readyState === 4 && xhr.status === 200) {
	        var reply = JSON.parse(xhr.responseText);
	        console.log(reply);
	        if(reply['Status'] == 0 || reply['Status'] == 1){
	        	if(reply['Status' == 0]){
	        		document.getElementById("loadText").innerHTML = "You are in Queue...";
	        	}
	        	if(reply['Status'] == 1){
					document.getElementById("loadText").innerHTML = "Processing Sim...";
	        	}
	        	setTimeout(function() {
				    statusCheck(rID);
				}, 500);

	        }
	        if(reply['Status'] == 2){
	        	document.getElementById("loadText").innerHTML = "Completed!";
	        	document.getElementById("loadGif").src = "/static/loaderComplete.png";
	        	location.replace("/report/"+rID);
	        }
	        if(reply['Status'] == 3){
	        	document.getElementById("loadText").innerHTML = "Sim Failed!";
	        	document.getElementById("loadGif").src = "/static/loaderFailed.png";
	        	location.replace("/failed");
	        }
	    }
	};
	console.log(rID);
	var data = JSON.stringify({
		'reportID':rID
	});
	xhr.send(data);
}



function exampleButton(){ // example button data for advanced sim
	console.log(document.getElementById("simEntry").value);
	document.getElementById('simEntry').value = `# SimC Addon 1.9.1

monk="Bowbi"
level=110
race=human
region=us
server=frostmourne
role=attack
professions=alchemy=800/engineering=800
talents=3213132
spec=windwalker
artifact=50:0:0:0:0:1094:4:800:4:801:4:1341:1:820:4:821:4:822:4:824:4:825:4:826:1:827:1:828:1:829:4:830:1:1549:4:1550:1:831:1:1551:1:832:1:833:1:1644:1:1376:1:1552:29
crucible=0/0/0

head=,id=151811,bonus_id=1811/3630
neck=,id=151965,enchant_id=5890,bonus_id=3612/42/1512/3336
shoulder=,id=152147,bonus_id=3612/1808/1502/3528
back=,id=152143,enchant_id=5435,bonus_id=3612/1522/3337
chest=,id=144239,bonus_id=1811/3630
shirt=,id=89195
tabard=,id=23705
wrist=,id=151992,bonus_id=3612/1808/1517/3337
hands=,id=152144,bonus_id=3612/1507/3336
waist=,id=134199,bonus_id=3536/1627/3337
legs=,id=152146,bonus_id=3612/1507/3336
feet=,id=137448,bonus_id=3536/1808/1612/3337
finger1=,id=151972,enchant_id=5429,bonus_id=3612/40/1502/3528
finger2=,id=152064,enchant_id=5429,bonus_id=3610/1808/1522/3337
trinket1=,id=154174,bonus_id=3984/3997
trinket2=,id=151968,bonus_id=3612/1502/3528
main_hand=,id=128940,bonus_id=734,relic_id=3612:1517:3337/3536:1617:3337/3612:1512:3528
off_hand=,id=133948
`;
}
