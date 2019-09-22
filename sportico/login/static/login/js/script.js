function rejectSinglesChallenge(id1, sportName, startTime, endTime, locationName) {
	window.location.href = '/rejectSinglesChallenge/' + id1 + '/' + sportName + '/'+ startTime + '/'+ endTime + '/'+ locationName + '/';
}

function acceptSinglesChallenge(id1, sportName, startTime, endTime, locationName) {
	window.location.href = '/acceptSinglesChallenge/' + id1 + '/' + sportName + '/'+ startTime + '/'+ endTime + '/'+ locationName + '/';
}

function rejectDoublesChallenge(sportName, startTime, endTime, locationName, id1, id2) {
	window.location.href = '/rejectDoublesChallenge/' + id1 + '/' + id2 + '/' + sportName + '/'+ startTime + '/'+ endTime + '/'+ locationName + '/';
}

function acceptDoublesChallenge(sportName, startTime, endTime, locationName, id1, id2) {
	window.location.href = '/acceptDoublesChallenge/' + id1 + '/' + id2 + '/' + sportName + '/'+ startTime + '/'+ endTime + '/'+ locationName + '/';
}

function rejectTeamChallenge(sportName, startTime, endTime, locationName, id1, id2) {
	window.location.href = '/rejectTeamChallenge/' + id1 + '/' + id2 + '/' + sportName + '/'+ startTime + '/'+ endTime + '/'+ locationName + '/';
}

function acceptTeamChallenge(sportName, startTime, endTime, locationName, id1, id2) {
	window.location.href = '/acceptTeamChallenge/' + id1 + '/' + id2 + '/' + sportName + '/'+ startTime + '/'+ endTime + '/'+ locationName + '/';
}


function acceptDoublesFormation(id1, sportName, captainId) {
	window.location.href = '/acceptDoublesFormation/' + id1 + '/' + sportName +'/' + captainId + '/';
}

function rejectDoublesFormation(id1, sportName, captainId) {
	window.location.href = '/rejectDoublesFormation/' + id1 + '/' + sportName +'/' + captainId + '/';
}

function acceptTeamInvite(teamName, sportName, captainId) {
	window.location.href = '/acceptTeamInvite/' + teamName + '/' + sportName +'/' + captainId + '/';
}

function rejectTeamInvite(teamName, sportName, captainId) {
	window.location.href = '/rejectTeamInvite/' + teamName + '/' + sportName +'/' + captainId + '/';
}

function acceptJoinTeamRequest(teamName, sportName, playerName) {
	window.location.href = '/acceptJoinTeamRequest/' + teamName + '/' + sportName +'/' + playerName + '/';
}

function rejectJoinTeamRequest(teamName, sportName, playerName) {
	window.location.href = '/rejectJoinTeamRequest/' + teamName + '/' + sportName +'/' + playerName + '/';
}

function blacklistUser() {
	var username = document.getElementById('hiddenIdParameter').value;
	var sportName = document.getElementById('hiddenSportNameParameter').value;
	var startTime = document.getElementById('hiddenStartTimeParameter').value;
	var endTime = document.getElementById('hiddenEndTimeParameter').value;
	var locationName = document.getElementById('hiddenLocationNameParameter').value;
	window.location.href = '/blackListUser/' + username + '/'+ sportName + '/'+ startTime + '/'+ endTime + '/'+ locationName + '/';
}

function fillHiddenField(username, sportName, startTime, endTime, locationName) {
	document.getElementById('hiddenIdParameter').value = username;
	document.getElementById('hiddenSportNameParameter').value = sportName;
	document.getElementById('hiddenStartTimeParameter').value = startTime;
	document.getElementById('hiddenEndTimeParameter').value = endTime;
	document.getElementById('hiddenLocationNameParameter').value = locationName;
}

function cancelChallenge() {
	var username = document.getElementById('hiddenIdParameter').value;
	var sportName = document.getElementById('hiddenSportNameParameter').value;
	var startTime = document.getElementById('hiddenStartTimeParameter').value;
	var endTime = document.getElementById('hiddenEndTimeParameter').value;
	var locationName = document.getElementById('hiddenLocationNameParameter').value;
	window.location.href = '/cancelChallenge/' + username + '/'+ sportName + '/'+ startTime + '/'+ endTime + '/'+ locationName + '/';
}

function fillHiddenFieldTeam(id1, id2, sportName, startTime, startDate, locationName) {
	document.getElementById('hiddenTeamId1Parameter').value = id1;
	document.getElementById('hiddenTeamId2Parameter').value = id2;
	document.getElementById('hiddenSportNameParameter').value = sportName;
	document.getElementById('hiddenStartTimeParameter').value = startTime;
	document.getElementById('hiddenStartDateParameter').value = startDate;
	document.getElementById('hiddenLocationNameParameter').value = locationName;
}

function cancelChallengeDoubles() {
	var id1 = document.getElementById('hiddenTeamId1Parameter').value;
	var id2 = document.getElementById('hiddenTeamId2Parameter').value;
	var sportName = document.getElementById('hiddenSportNameParameter').value;
	var startTime = document.getElementById('hiddenStartTimeParameter').value;
	var startDate = document.getElementById('hiddenStartDateParameter').value;
	var locationName = document.getElementById('hiddenLocationNameParameter').value;
	window.location.href = '/cancelChallengeDoubles/' + id1 + '/'+ id2 + '/' + sportName + '/'+ startTime + '/'+ startDate + '/'+ locationName + '/';
}

function cancelChallengeTeam() {
	var id1 = document.getElementById('hiddenTeamId1Parameter').value;
	var id2 = document.getElementById('hiddenTeamId2Parameter').value;
	var startTime = document.getElementById('hiddenStartTimeParameter').value;
	var startDate = document.getElementById('hiddenStartDateParameter').value;
	var locationName = document.getElementById('hiddenLocationNameParameter').value;
	window.location.href = '/cancelChallengeTeam/' + id1 + '/'+ id2 + '/'+ startTime + '/'+ startDate + '/'+ locationName + '/';
}

function clearNotification(notificationId) {
	window.location.href = '/clearNotification/' + notificationId + '/';
}

function clearAllNotifications() {
	window.location.href = '/clearAllNotifications/';
}

function blockList() {
	window.location.href = '/blockList/';
}	

function friendList() {
	window.location.href = '/friendList/';
}	

function toggleBlock(username2) {
    var x = document.getElementById("toggleBlock");
    if (x.innerText == "UnBlock") {
		window.location.href = '/unblockUser/' + username2 + '/';
    } 
}

function joinEvent(eventId) {
	window.location.href = '/joinEvent/' + eventId + '/';
}

function CancelEvent(eventId) {
	window.location.href = '/CancelEvent/' + eventId + '/';
}

function acceptEventRequest(eventId, userId) {
	window.location.href = '/acceptEventRequest/' + eventId + '/' + userId + '/';
}

function rejectEventRequest(eventId, userId) {
	window.location.href = '/rejectEventRequest/' + eventId + '/' + userId + '/';
}

function fillHiddenFieldEvent(eventId) {
	document.getElementById('hiddenEventId1Parameter').value = eventId;
}

function cancelScheduledEvent() {
	var eventId = document.getElementById('hiddenEventId1Parameter').value;
	window.location.href = '/cancelScheduledEvent/' + eventId + '/';
}

function fillHiddenFieldMatching(requestId1, requestId2) {
	document.getElementById('hiddenMatchingParameter1').value = requestId1;
	document.getElementById('hiddenMatchingParameter2').value = requestId2;
}

function cancelSinglesMatching() {
	var requestId1 = document.getElementById('hiddenMatchingParameter1').value;
	var requestId2 = document.getElementById('hiddenMatchingParameter2').value;

	window.location.href = '/cancelSinglesMatching/' + requestId1 + '/' + requestId2 + '/';
}

function cancelDoublesMatching() {
	var requestId1 = document.getElementById('hiddenMatchingParameter1').value;
	var requestId2 = document.getElementById('hiddenMatchingParameter2').value;

	window.location.href = '/cancelDoublesMatching/' + requestId1 + '/' + requestId2 + '/';
}

function cancelTeamMatching() {
	var requestId1 = document.getElementById('hiddenMatchingParameter1').value;
	var requestId2 = document.getElementById('hiddenMatchingParameter2').value;

	window.location.href = '/cancelTeamMatching/' + requestId1 + '/' + requestId2 + '/';
}