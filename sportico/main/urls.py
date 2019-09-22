from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
	url(r'^home/$', views.home, name='home'),
	url(r'^events/$', views.events, name='events'),
	url(r'^profile/$', views.profile, name='profile'),
	url(r'^uploadImage/$', views.uploadImage, name='uploadImage'),
	url(r'^notifications/$', views.notifications, name='notifications'),
	url(r'^singles/$', views.singles, name='singles'),
	url(r'^doubles/$', views.doubles, name='doubles'),
	url(r'^activities/$', views.activities, name='activities'),
	url(r'^registerUserSport/$', views.registerUserSport, name='registerUserSport'),
	url(r'^registerSinglesChallenge/$', views.registerSinglesChallenge, name='registerSinglesChallenge'),
	url(r'^rejectSinglesChallenge/(?P<id1>[\w .]+)/(?P<sportName>[\w .]+)/(?P<startTime>[\w .:]+)/(?P<endTime>[\w .:]+)/(?P<locationName>[\w .]+)/$', views.rejectSinglesChallenge, name='rejectSinglesChallenge'),
	url(r'^acceptSinglesChallenge/(?P<id1>[\w .]+)/(?P<sportName>[\w .]+)/(?P<startTime>[\w .:]+)/(?P<endTime>[\w .:]+)/(?P<locationName>[\w .]+)/$', views.acceptSinglesChallenge, name='acceptSinglesChallenge'),
	url(r'^registerSinglesFillSlot/$', views.registerSinglesFillSlot, name='registerSinglesFillSlot'),
	url(r'^clearNotification/(?P<notificationId>[0-9+]+)/$', views.clearNotification, name='clearNotification'),
	url(r'^clearAllNotifications/$', views.clearAllNotifications, name='clearAllNotifications'),
	url(r'^blackListUser/(?P<username>[\w .]+)/(?P<sportName>[\w .]+)/(?P<startTime>[\w .:]+)/(?P<endTime>[\w .:]+)/(?P<locationName>[\w .]+)/$', views.blackListUser, name='blackListUser'),
	url(r'^cancelChallenge/(?P<username>[\w .]+)/(?P<sportName>[\w .]+)/(?P<startTime>[\w .:]+)/(?P<endTime>[\w .:]+)/(?P<locationName>[\w .]+)/$', views.cancelChallenge, name='cancelChallenge'),
	url(r'^ajax/getLocations/$', views.getLocations, name='getLocations'),
	url(r'^ajax/getPlayerNames/$', views.getPlayerNames, name='getPlayerNames'),
	url(r'^ajax/getPlayerNamesDoubles/$', views.getPlayerNamesDoubles, name='getPlayerNamesDoubles'),
	url(r'^formDoublesTeam/$', views.formDoublesTeam, name='formDoublesTeam'),
	url(r'^rejectDoublesFormation/(?P<id1>[\w .]+)/(?P<sportName>[\w .]+)/(?P<captainId>[\w .]+)/$', views.rejectDoublesFormation, name='rejectDoublesFormation'),
	url(r'^acceptDoublesFormation/(?P<id1>[\w .]+)/(?P<sportName>[\w .]+)/(?P<captainId>[\w .]+)/$', views.acceptDoublesFormation, name='acceptDoublesFormation'),
	url(r'^submitSinglesResult/$', views.submitSinglesResult, name='submitSinglesResult'),
	url(r'^submitTeamResult/$', views.submitTeamResult, name='submitTeamResult'),
	url(r'^submitDoublesResult/$', views.submitDoublesResult, name='submitDoublesResult'),
	url(r'^team/$', views.team, name='team'),
	url(r'^makeTeam/$', views.makeTeam, name='makeTeam'),
	url(r'^addPlayerTeam/$', views.addPlayerTeam, name='addPlayerTeam'),
	url(r'^ajax/getPlayerNamesTeam/$', views.getPlayerNamesTeam, name='getPlayerNamesTeam'),
	url(r'^ajax/sendRequestTeamJoin/$', views.sendRequestTeamJoin, name='sendRequestTeamJoin'),
	url(r'^ajax/findCaptainTeam/$', views.findCaptainTeam, name='findCaptainTeam'),
	url(r'^sendJoinRequestTeam/$', views.sendJoinRequestTeam, name='sendJoinRequestTeam'),
	url(r'^acceptTeamInvite/(?P<teamName>[\w .]+)/(?P<sportName>[\w .]+)/(?P<captainId>[\w .]+)/$', views.acceptTeamInvite, name='acceptTeamInvite'),
	url(r'^rejectTeamInvite/(?P<teamName>[\w .]+)/(?P<sportName>[\w .]+)/(?P<captainId>[\w .]+)/$', views.rejectTeamInvite, name='rejectTeamInvite'),
	url(r'^acceptJoinTeamRequest/(?P<teamName>[\w .]+)/(?P<sportName>[\w .]+)/(?P<playerName>[\w .]+)/$', views.acceptJoinTeamRequest, name='acceptJoinTeamRequest'),
	url(r'^rejectJoinTeamRequest/(?P<teamName>[\w .]+)/(?P<sportName>[\w .]+)/(?P<playerName>[\w .]+)/$', views.rejectJoinTeamRequest, name='rejectJoinTeamRequest'),
	url(r'^ajax/getUserTeamSport/$', views.getUserTeamSport, name='getUserTeamSport'),
	url(r'^ajax/getDoubleSportTeam/$', views.getDoubleSportTeam, name='getDoubleSportTeam'),
	url(r'^ajax/findCaptainDoubles/$', views.findCaptainDoubles, name='findCaptainDoubles'),

	url(r'^registerDoublesChallenge/$', views.registerDoublesChallenge, name='registerDoublesChallenge'),
	url(r'^rejectDoublesChallenge/(?P<id1>[\w .]+)/(?P<id2>[\w .]+)/(?P<sportName>[\w .]+)/(?P<startTime>[\w .:]+)/(?P<endTime>[\w .:]+)/(?P<locationName>[\w .]+)/$', views.rejectDoublesChallenge, name='rejectDoublesChallenge'),
	url(r'^acceptDoublesChallenge/(?P<id1>[\w .]+)/(?P<id2>[\w .]+)/(?P<sportName>[\w .]+)/(?P<startTime>[\w .:]+)/(?P<endTime>[\w .:]+)/(?P<locationName>[\w .]+)/$', views.acceptDoublesChallenge, name='acceptDoublesChallenge'),
	
	url(r'^ajax/getUserSportTeamsList/$', views.getUserSportTeamsList, name='getUserSportTeamsList'),
	url(r'^ajax/getOpponentTeamsListChallenge/$', views.getOpponentTeamsListChallenge, name='getOpponentTeamsListChallenge'),
	url(r'^registerTeamChallenge/$', views.registerTeamChallenge, name='registerTeamChallenge'),
	url(r'^rejectTeamChallenge/(?P<id1>[\w .]+)/(?P<id2>[\w .]+)/(?P<sportName>[\w .]+)/(?P<startTime>[\w .:]+)/(?P<endTime>[\w .:]+)/(?P<locationName>[\w .]+)/$', views.rejectTeamChallenge, name='rejectTeamChallenge'),
	url(r'^acceptTeamChallenge/(?P<id1>[\w .]+)/(?P<id2>[\w .]+)/(?P<sportName>[\w .]+)/(?P<startTime>[\w .:]+)/(?P<endTime>[\w .:]+)/(?P<locationName>[\w .]+)/$', views.acceptTeamChallenge, name='acceptTeamChallenge'),
	url(r'^cancelChallengeDoubles/(?P<id1>[0-9+]+)/(?P<id2>[0-9+]+)/(?P<sportName>[\w .]+)/(?P<startTime>[\w .:]+)/(?P<startDate>[\w .:,]+)/(?P<locationName>[\w .]+)/$', views.cancelChallengeDoubles, name='cancelChallengeDoubles'),
	url(r'^cancelChallengeTeam/(?P<id1>[0-9+]+)/(?P<id2>[0-9+]+)/(?P<startTime>[\w .:]+)/(?P<startDate>[\w .:,]+)/(?P<locationName>[\w .]+)/$', views.cancelChallengeTeam, name='cancelChallengeTeam'),

	url(r'^blockList/$', views.blockList, name='blockList'),
	url(r'^friendList/$', views.friendList, name='friendList'),

	url(r'^blockUser/(?P<username2>[\w .]+)/$', views.blockUser, name='blockUser'),
	url(r'^unblockUser/(?P<username2>[\w .]+)/$', views.unblockUser, name='unblockUser'),

	url(r'^registerDoublesFillSlot/$', views.registerDoublesFillSlot, name='registerDoublesFillSlot'),
	url(r'^registerTeamFillSlot/$', views.registerTeamFillSlot, name='registerTeamFillSlot'),

	url(r'^ajax/getUsernames/$', views.getUsernames, name='getUsernames'),
	url(r'^profile/user/(?P<username>[\w .]+)/$', views.searchUserProfile, name='searchUserProfile'),
	url(r'^ajax/blockUser/$', views.ajaxblockUser, name='ajaxblockUser'),
	url(r'^ajax/unBlockUser/$', views.ajaxunBlockUser, name='ajaxunBlockUser'),

	url(r'^addEvent/$', views.addEvent, name='addEvent'),
	url(r'^joinEvent/(?P<eventId>[0-9+]+)/$', views.joinEvent, name='joinEvent'),
	url(r'^CancelEvent/(?P<eventId>[0-9+]+)/$', views.CancelEvent, name='CancelEvent'),

	url(r'^acceptEventRequest/(?P<eventId>[0-9+]+)/(?P<username>[\w .]+)/$', views.acceptEventRequest, name='acceptEventRequest'),
	url(r'^rejectEventRequest/(?P<eventId>[0-9+]+)/(?P<username>[\w .]+)/$', views.rejectEventRequest, name='rejectEventRequest'),

	url(r'^cancelScheduledEvent/(?P<eventId>[0-9+]+)/$', views.cancelScheduledEvent, name='cancelScheduledEvent'),

	url(r'^ajax/sendFriendRequest/$', views.sendFriendRequest, name='sendFriendRequest'),
	url(r'^ajax/cancelFriendRequest/$', views.cancelFriendRequest, name='cancelFriendRequest'),
	url(r'^ajax/acceptFriendRequest/$', views.acceptFriendRequest, name='acceptFriendRequest'),
	url(r'^ajax/rejectFriendRequest/$', views.rejectFriendRequest, name='rejectFriendRequest'),
	url(r'^ajax/unFriend/$', views.unFriend, name='unFriend'),

	url(r'^cancelSinglesMatching/(?P<requestId1>[0-9+]+)/(?P<requestId2>[0-9+]+)/$', views.cancelSinglesMatching, name='cancelSinglesMatching'),
	url(r'^cancelDoublesMatching/(?P<requestId1>[0-9+]+)/(?P<requestId2>[0-9+]+)/$', views.cancelDoublesMatching, name='cancelDoublesMatching'),
	url(r'^cancelTeamMatching/(?P<requestId1>[0-9+]+)/(?P<requestId2>[0-9+]+)/$', views.cancelTeamMatching, name='cancelTeamMatching'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)