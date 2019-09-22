from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from login.models import *
from main.forms import *
from django.contrib.auth import get_user_model
from login.choices import *
from django.shortcuts import redirect
from django.db.models import Q
from datetime import datetime
from django.utils import timezone
from django.http import JsonResponse
from urllib.parse import parse_qs 
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import QueryDict

from django.core.files.storage import FileSystemStorage


User = get_user_model()

@login_required(login_url="/login/")
def home(request):
	currentUser = request.user

	userSports = UserSport.objects.filter(playerId = currentUser)
	sportsList = []
	for sport in userSports:
		try:
			sportsList.append((sport.sportName.sportName, sport.sportName.sportName))
		except sport.sportName.DoesNotExist:
			print(str(e))
	userChoices = set(list(SPORT_CHOICES)) - set(sportsList)
	sportForm = SportForm(tuple(userChoices))

	doublesReceivedFormationInvite = DoublesFormationRequest.objects.filter(receiverId= currentUser, status = 'Waiting');
	# doublesFormationInvite = DoublesFormationRequest.objects.filter(senderId= currentUser);
	teamJoiningRequestInvite = TeamJoiningRequest.objects.filter(playerId = currentUser, status='Waiting', requestType='Recruiting')
	
	teamJoiningRequestRequest = TeamJoiningRequest.objects.filter(teamId__captainId = currentUser, status='Waiting', requestType='Joining')
	

	# Setting Status as expired 
	userChallengesExpired = SinglesChallenge.objects.filter(Q(playerId1 = currentUser) | Q(playerId2 = currentUser), startDate__lt = datetime.now(), status = 'Waiting').update(status = 'Expired')
	# Setting completed matches in results table
	userChallengesCompleted = SinglesChallenge.objects.filter(Q(playerId1 = currentUser) | Q(playerId2 = currentUser), startDate__lt = datetime.now(), status = 'Accepted')
	for item in userChallengesCompleted:
		result = SinglesResult()
		result.playerId1 = item.playerId1
		result.playerId2 = item.playerId2
		result.sportName = item.sportName
		result.locationId = item.locationId
		result.startTime = item.startTime
		result.endTime = item.endTime
		result.startDate = item.startDate
		result.endDate = item.endDate
		result.status = 'NoneFilled'
		result.save() 
		item.status = 'ResultEntered'
		item.save()

	singlesResults = SinglesResult.objects.filter((Q(playerId1 = currentUser) & (Q(status = 'NoneFilled') | Q(status = 'Player2Filled'))) | (Q(playerId2 = currentUser) & (Q(status = 'NoneFilled') | Q(status = 'Player1Filled')))) 
	singlesResultFormList = []
	ids =0
	for item in singlesResults:
		if item.playerId1 == currentUser:
			username = item.playerId2.username
		else:
			username = item.playerId1.username

		default = '1'
		if item.victorId == currentUser:
			default = '1'
		else:
			default = '2'

		form = singlesResultForm(initial = {'resultId': item.singlesResultId, 'playerName': username, 'sportName': item.sportName.sportName, 'locationId' : item.locationId.locationName, 'startTime' : item.startTime, 'startDate': item.startDate, 'endTime': item.endTime,
			'endDate': item.endDate, 'username' : currentUser.username, 'matchScore': item.matchScore, 'winner': default})

		formDict = {'form': [form,ids]}
		singlesResultFormList.append(formDict)
		ids = ids+1

	doublesChallengesExpired = DoublesChallenge.objects.filter(Q(doublesId1__player1 = currentUser) | Q(doublesId1__player2 = currentUser) | Q(doublesId2__player1 = currentUser) | Q(doublesId2__player1 = currentUser), status = 'Waiting', startDate__lt = datetime.now()).update(status = 'Expired')
	doublesChallengesCompleted = DoublesChallenge.objects.filter(Q(doublesId1__player1 = currentUser) | Q(doublesId1__player2 = currentUser) | Q(doublesId2__player1 = currentUser) | Q(doublesId2__player1 = currentUser), status = 'Accepted', startDate__lt = datetime.now())
	for item in doublesChallengesCompleted:
		result = DoublesResult()
		result.doublesId1 = item.doublesId1
		result.doublesId2 = item.doublesId2
		result.sportName = item.sportName
		result.locationId = item.locationId
		result.startTime = item.startTime
		result.endTime = item.endTime
		result.startDate = item.startDate
		result.endDate = item.endDate
		result.status = 'NoneFilled'
		result.save() 
		item.status = 'ResultEntered'
		item.save()

	doublesResults = DoublesResult.objects.filter((Q(doublesId1__captainId = currentUser) & (Q(status = 'NoneFilled') | Q(status = 'Player2Filled'))) | (Q(doublesId2__captainId = currentUser) & (Q(status = 'NoneFilled') | Q(status = 'Player1Filled'))))
	doublesResultFormList = []
	for item in doublesResults:
		if item.doublesId1.captainId == currentUser:
			teamName = item.doublesId2.teamName
			userTeamName = item.doublesId1.teamName
		else:
			teamName = item.doublesId1.teamName
			userTeamName = item.doublesId2.teamName

		form = resultForm(initial = {'resultId': item.doublesMatchId, 'teamName': teamName, 'sportName': item.sportName.sportName, 'locationId' : item.locationId.locationName, 'startTime' : item.startTime, 'startDate': item.startDate, 'endTime': item.endTime,
			'endDate': item.endDate, 'userTeamName' : userTeamName, 'matchScore': item.matchScore})

		formDict = {'form': [form,ids]}
		doublesResultFormList.append(formDict)
		ids = ids +1

	teamChallengesExpired = TeamChallenge.objects.filter(Q(teamId1__captainId = currentUser) | Q(teamId2__captainId = currentUser), status = 'Waiting', startDate__lt = datetime.now()).update(status = 'Expired')
	userTeams = TeamPlayers.objects.filter(playerId = currentUser).values('teamId')
	teamChallengesCompleted = TeamChallenge.objects.filter(Q(teamId1__in = userTeams) | Q(teamId2__in = userTeams), status = 'Accepted', startDate__lt = datetime.now())
	for item in teamChallengesCompleted:
		result = TeamResult()
		result.teamId1 = item.teamId1
		result.teamId2 = item.teamId2
		result.sportName = item.teamId1.sportName
		result.locationId = item.locationId
		result.startTime = item.startTime
		result.endTime = item.endTime
		result.startDate = item.startDate
		result.endDate = item.endDate
		result.status = 'NoneFilled'
		result.save() 
		item.status = 'ResultEntered'
		item.save()

	teamResults = TeamResult.objects.filter((Q(teamId1__captainId = currentUser) & (Q(status = 'NoneFilled') | Q(status = 'Player2Filled'))) | (Q(teamId2__captainId = currentUser) & (Q(status = 'NoneFilled') | Q(status = 'Player1Filled'))))
	teamResultFormList = []
	for item in teamResults:
		if item.teamId1.captainId == currentUser:
			teamName = item.teamId2.teamName
			userTeamName = item.teamId1.teamName
		else:
			teamName = item.teamId1.teamName
			userTeamName = item.teamId2.teamName

		form = resultForm(initial = {'resultId': item.teamMatchId, 'teamName': teamName, 'sportName': item.teamId1.sportName.sportName, 'locationId' : item.locationId.locationName, 'startTime' : item.startTime, 'startDate': item.startDate, 'endTime': item.endTime,
			'endDate': item.endDate, 'userTeamName' : userTeamName, 'matchScore': item.matchScore})

		formDict = {'form': [form,ids]}
		teamResultFormList.append(formDict)
		ids = ids+1

	userChallenges = SinglesChallenge.objects.filter(Q(playerId1 = currentUser) | Q(playerId2 = currentUser), status = 'Accepted')
	SinglesMatching.objects.filter(Q(singlesRequestId1__playerId = currentUser) | Q(singlesRequestId2__playerId = currentUser), startDate__lt = datetime.now(), status='Accepted').update(status='Expired') 
	userMatching = SinglesMatching.objects.filter(Q(singlesRequestId1__playerId = currentUser) | Q(singlesRequestId2__playerId = currentUser), status = 'Accepted').select_related() 

	doublesChallenges = DoublesChallenge.objects.filter(Q(doublesId1__player1 = currentUser) | Q(doublesId1__player2 = currentUser) | Q(doublesId2__player1 = currentUser) | Q(doublesId2__player1 = currentUser), status = 'Accepted').select_related()
	doublesMatching =  DoublesMatching.objects.filter(Q(doublesRequestId1__doublesId__player1 = currentUser) | Q(doublesRequestId1__doublesId__player2 = currentUser) | Q(doublesRequestId2__doublesId__player1 = currentUser) | Q(doublesRequestId2__doublesId__player2 = currentUser)).select_related() 

	teamChallengesFirstTeam = TeamChallenge.objects.filter(teamId1__in = userTeams, status = 'Accepted')
	teamChallengesSecondTeam = TeamChallenge.objects.filter(teamId2__in = userTeams, status = 'Accepted')  
	teamMatchingFirstTeam = TeamMatching.objects.filter(teamRequestId1__teamId__in = userTeams, status = 'Accepted').select_related()
	teamMatchingSecondTeam = TeamMatching.objects.filter(teamRequestId2__teamId__in = userTeams, status = 'Accepted').select_related()  
	
	userReceivedChallenges = SinglesChallenge.objects.filter(playerId2 = currentUser, status = 'Waiting')

	doublesCaptain = Doubles.objects.filter(player1 = currentUser, captainId = currentUser).values('doublesId')
	doublesReceivedChallenges = DoublesChallenge.objects.filter(doublesId2__in = doublesCaptain, status = 'Waiting')
	teamReceivedChallenges = TeamChallenge.objects.filter(teamId2__captainId = currentUser, status = 'Waiting').select_related()

	return render(request, "main/home.html", {'sportForm' : sportForm, 'username': currentUser.username, 'userChallenges' : userChallenges, 'userMatching' : userMatching, 'doublesChallenges' : doublesChallenges, 'doublesMatching' : doublesMatching, 'teamChallengesFirstTeam' : teamChallengesFirstTeam, 
		'teamChallengesSecondTeam' : teamChallengesSecondTeam, 'teamMatchingFirstTeam' : teamMatchingFirstTeam, 'teamMatchingSecondTeam' : teamMatchingSecondTeam, 'userReceivedChallenges' : userReceivedChallenges, 'doublesReceivedChallenges' : doublesReceivedChallenges, 'teamReceivedChallenges' : teamReceivedChallenges, 'doublesReceivedFormationInvite' : doublesReceivedFormationInvite, 
		'teamJoiningRequestInvite' : teamJoiningRequestInvite, 'teamJoiningRequestRequest' : teamJoiningRequestRequest, 'singlesResultFormList': singlesResultFormList, 'doublesResultFormList': doublesResultFormList, 'teamResultFormList': teamResultFormList})


def profile(request):
	currentUser = request.user
	doubleTeams = Doubles.objects.filter(Q(player1 = currentUser) | Q(player2 = currentUser))
	teams = TeamPlayers.objects.filter(playerId = currentUser)
	sports = UserSport.objects.filter(playerId = currentUser)

	return render(request,"main/profile.html",{'currentUser':currentUser, 'user' : currentUser, 'doubleTeams' : doubleTeams, 'teams' : teams , 'sports' : sports, 'uploadButton' : "True"})

def uploadImage(request):
	currentUser = request.user
	doubleTeams = Doubles.objects.filter(Q(player1 = currentUser) | Q(player2 = currentUser))
	teams = TeamPlayers.objects.filter(playerId = currentUser)
	if request.method == 'POST':

		print(request.POST)
		print(request.FILES)
		print(request.FILES['myfile1'])

		form = UploadImageForm(request.POST, request.FILES)
		# if form.is_valid():
		# print("Got cpk",form.cleaned_data['title'])
		# print("Got file",request.FILES['file'].read())


		# print(form)

		# print(request)
		print("manas")
		# print(request.FILES['myfile'])
		myfile = request.FILES['myfile1']
		print(myfile)


		fs = FileSystemStorage()
		filename = fs.save(myfile.name, myfile)
		uploaded_file_url = fs.url(filename)

		print(uploaded_file_url)

		user = User.objects.get(username= currentUser)
		user.profilePicture = uploaded_file_url
		print(user)
		print(user.profilePicture)
		user.save()


	return redirect('/profile/') 	

def searchUserProfile(request,username):
	currentUser = request.user
	user=User.objects.get(username=username)
	doubleTeams = Doubles.objects.filter(Q(player1 = user) | Q(player2 = user))
	teams = TeamPlayers.objects.filter(playerId = user)
	blacklist = UserBlacklist.objects.filter(uid1= currentUser,uid2= user )
	isBlacklisted =0
	if blacklist.count() >0:
		isBlacklisted =1;

	friend = UserFriend.objects.filter(Q(uid1= currentUser,uid2= user)|Q(uid1= user,uid2= currentUser))
	isFriend =0
	if friend.count() ==1:
		isFriend =1;
	elif friend.count() >1:
		print("ERROR")

	isFriendRequestCancel =0
	isFriendRequestAccept =0

	friendRequestAccept = UserFriendRequest.objects.filter(uid1= user,uid2= currentUser, status='Waiting')
	if friendRequestAccept.count() ==1:
		isFriendRequestAccept =1;
	elif friendRequestAccept.count() >1:
		print("ERROR")

	friendRequestCancel = UserFriendRequest.objects.filter(uid1= currentUser, uid2= user, status='Waiting')
	if friendRequestCancel.count() ==1:
		isFriendRequestCancel =1;
	elif friendRequestCancel.count() >1:
		print("ERROR")

	sports = UserSport.objects.filter(playerId = user)
	return render(request,"main/profile.html",{'currentUser':currentUser, 'user' : user, 'doubleTeams' : doubleTeams, 'teams' : teams, 'blacklist':isBlacklisted, 'friend':isFriend, 'friendRequestCancel':isFriendRequestCancel, 'friendRequestAccept':isFriendRequestAccept, 'uploadButton' : "False",  'sports' : sports})

@login_required(login_url="/login/")
def blockList(request):
	
	userToBlock = request.user

	blockedUsers = UserBlacklist.objects.filter(uid1 = userToBlock)
	print(blockedUsers.count())
	return render(request,"main/blockList.html" , {'blockedUsers' : blockedUsers})
@login_required(login_url="/login/")
def friendList(request):
	
	currentUser = request.user

	friends = UserFriend.objects.filter(Q(uid1 = currentUser) | Q(uid2=currentUser))
	friendList=[]
	for friend in friends:
		if friend.uid1==currentUser:
			friendList.append(friend.uid2)
		else:
			friendList.append(friend.uid1)

	return render(request,"main/friendList.html" , {'friends' : friendList})

@login_required(login_url="/login/")
def unFriend(request):
	
	currentUser =request.user
	print(request.GET.get('username', None))
	user = User.objects.filter(username= request.GET.get('username', None))
	friends = UserFriend.objects.filter(Q(uid1=currentUser, uid2__username= request.GET.get('username', None))|Q(uid2=currentUser, uid1__username= request.GET.get('username', None)))
	data = {}
	if user.count() ==1 and friends.count()==1:

		friends = UserFriend.objects.filter(Q(uid1=currentUser, uid2__username= request.GET.get('username', None))|Q(uid2=currentUser, uid1__username= request.GET.get('username', None))).delete() 		
		data = {'status': "success"}
	else:
		print(user.count())
		print(friends.count())
		data = {'status': "failure"}

	print(data)
	return JsonResponse(data)

@login_required(login_url="/login/")
def sendFriendRequest(request):
	
	currentUser =request.user
	print(request.GET.get('username', None))
	user = User.objects.filter(username= request.GET.get('username', None))
	friendRequest = UserFriendRequest.objects.filter(Q(uid1= currentUser,uid2__username= request.GET.get('username', None),status='Waiting')|Q(uid1__username= request.GET.get('username', None),uid2= currentUser,status='Waiting'))
	data = {}
	if user.count() ==1 and friendRequest.count()==0:

		userFriendRequest = UserFriendRequest()
		userFriendRequest.uid1 = currentUser
		userFriendRequest.uid2 = user[0]
		userFriendRequest.status = 'Waiting'
		userFriendRequest.sentTime = datetime.now()
		userFriendRequest.save() 		
		data = {'status': "success"}
	else:
		print(user.count())
		print(friendRequest.count())
		data = {'status': "failure"}

	print(data)
	return JsonResponse(data)

@login_required(login_url="/login/")
def cancelFriendRequest(request):
	
	currentUser =request.user
	print(request.GET.get('username', None))
	user = User.objects.filter(username= request.GET.get('username', None))
	friendRequest = UserFriendRequest.objects.filter(uid1= currentUser, uid2__username= request.GET.get('username', None), status='Waiting')
	data = {}
	if user.count() ==1 and friendRequest.count()==1:
		friendReq = UserFriendRequest.objects.get(uid2__username= request.GET.get('username', None), uid1= currentUser, status='Waiting')
		friendReq.status = 'Cancelled'
		friendReq.save() 	

		data = {'status': "success"}
	else:
		print(user.count())
		print(friendRequest.count())
		data = {'status': "failure"}

	print(data)
	return JsonResponse(data)	

@login_required(login_url="/login/")
def acceptFriendRequest(request):
	
	currentUser =request.user
	print(request.GET.get('username', None))
	user = User.objects.filter(username= request.GET.get('username', None))
	friendRequest = UserFriendRequest.objects.filter(uid1__username= request.GET.get('username', None), uid2= currentUser, status='Waiting')
	data = {}
	if user.count() ==1 and friendRequest.count()==1:
		friendReq = UserFriendRequest.objects.get(uid1__username= request.GET.get('username', None), uid2= currentUser, status='Waiting')
		friendReq.status = 'Accepted'
		friendReq.save() 

		userFriend = UserFriend()
		userFriend.uid1 = currentUser
		userFriend.uid2 = user[0]
		userFriend.startTime = timezone.now()
		userFriend.save() 

		notificationHelper(user[0],currentUser.username+" has accepted your friend request.")


		data = {'status': "success"}
	else:
		print(user.count())
		print(friendRequest.count())
		data = {'status': "failure"}

	print(data)
	return JsonResponse(data)

@login_required(login_url="/login/")
def rejectFriendRequest(request):
	
	currentUser =request.user
	print(request.GET.get('username', None))
	user = User.objects.filter(username= request.GET.get('username', None))
	friendRequest = UserFriendRequest.objects.filter(uid1__username= request.GET.get('username', None), uid2= currentUser, status='Waiting')
	data = {}
	if user.count() ==1 and friendRequest.count()==1:
		friendReq = UserFriendRequest.objects.get(uid1__username= request.GET.get('username', None), uid2= currentUser, status='Waiting')
		friendReq.status = 'Rejected'
		friendReq.save() 

		data = {'status': "success"}
	else:
		print(user.count())
		print(friendRequest.count())
		data = {'status': "failure"}

	print(data)
	return JsonResponse(data)

@login_required(login_url="/login/")
def blockUser(request,username2):
	
	# print(username2)

	blockedUidObject = User.objects.filter(username= username2)

	for userId in blockedUidObject:
		blockedUserId = userId
	# print(blockedUidObject)

	blockedUid = User.objects.filter()

	blockedUsers = UserBlacklist()
	blockedUsers.uid1 = request.user
	blockedUsers.uid2 = blockedUserId
	blockedUsers.save() 		


	blockedUsers = UserBlacklist.objects.filter(uid1= request.user)
	print(blockedUsers.count())
	return render(request,"main/blockList.html" , {'blockedUsers' : blockedUsers})

def unblockUser(request,username2):
	
	unblockedUidObject = User.objects.filter(username= username2)
	for userId in unblockedUidObject:
		unblockedUserId = userId

	blockedUsers = UserBlacklist.objects.filter(uid1= request.user , uid2 = unblockedUserId).delete()

	blockedUsers = UserBlacklist.objects.filter(uid1= request.user)
	print(blockedUsers.count())
	return render(request,"main/blockList.html" , {'blockedUsers' : blockedUsers})

@login_required(login_url="/login/")
def ajaxblockUser(request):
	
	currentUser =request.user
	user = User.objects.filter(username= request.GET.get('username', None))
	blockedUser = UserBlacklist.objects.filter(uid1=currentUser, uid2__username= request.GET.get('username', None))
	data = {}
	if user.count() ==1 and blockedUser.count()==0:

		blockedUsers = UserBlacklist()
		blockedUsers.uid1 = currentUser
		blockedUsers.uid2 = user[0]
		blockedUsers.save() 		
		data = {'status': "success"}
	else:
		data = {'status': "failure"}

	return JsonResponse(data)

def ajaxunBlockUser(request):
	
	currentUser =request.user

	users = UserBlacklist.objects.filter(uid1=currentUser, uid2__username= request.GET.get('username', None))

	data = {}
	if users.count() ==1:
		blockedUsers = UserBlacklist.objects.filter(uid1=currentUser, uid2__username= request.GET.get('username', None)).delete()
		
		data = {'status': "success"}
	else:
		data = {'status': "failure"}

	return JsonResponse(data)
	return render(request,"main/blockList.html" , {'blockedUsers' : blockedUsers})

@login_required(login_url="/login/")
def notifications(request):
	currentUser = request.user

	userNotifications = Notification.objects.filter(userId = currentUser).order_by('-sentTime')
	friends = UserFriendRequest.objects.filter(uid2=currentUser,status='Waiting')

	return render(request,"main/notifications.html", {'userNotifications' : userNotifications,'friends': friends })

@login_required(login_url="/login/")
def singles(request):
	currentUser = request.user

	userSports = UserSport.objects.filter(playerId = currentUser)
	sportsList = []
	for sport in userSports:
		try:
			sportsList.append((sport.sportName.sportName, sport.sportName.sportName))
		except sport.sportName.DoesNotExist:
			print(str(e))
	
	locationList = []
	for sport in userSports:
		try:
			sportsLocation = LocationSport.objects.filter(sportName = sport.sportName.sportName)
			for location in sportsLocation:
				tupleAdded = ((location.locationId.locationName, location.locationId.locationName))
				if tupleAdded not in locationList:
					locationList.append(tupleAdded)
		except sport.sportName.DoesNotExist:
			print(str(e))

	form = SinglesChallengeForm(tuple(locationList), tuple(sportsList))

	formFillSlot = SinglesFillSlotForm(tuple(sportsList))

	singlesResults = SinglesResult.objects.filter(Q(playerId1 = currentUser)  | Q(playerId1 = currentUser))
	return render(request,"main/singles.html", {'form' : form, 'formFillSlot':formFillSlot, 'singlesResults':singlesResults, 'username': currentUser.username})

@login_required(login_url="/login/")
def doubles(request):
	currentUser = request.user

	userSports = UserSport.objects.filter(playerId = currentUser)
	sportsList = []
	for sport in userSports:
		try:
			sportsList.append((sport.sportName.sportName, sport.sportName.sportName))
		except sport.sportName.DoesNotExist:
			print(str(e))
	# print(tuple(sportsList))
	locationList = []
	for sport in userSports:
		try:
			sportsLocation = LocationSport.objects.filter(sportName = sport.sportName.sportName)
			for location in sportsLocation:
				tupleAdded = ((location.locationId.locationName, location.locationId.locationName))
				if tupleAdded not in locationList:
					locationList.append(tupleAdded)
		except sport.sportName.DoesNotExist:
			print(str(e))

	formChallenge = DoublesChallengeForm(tuple(locationList), tuple(sportsList))

	formFillSlot = DoublesFillSlotForm(tuple(sportsList))


	form = doublesTeamForm(tuple(sportsList))
	doublesResults = DoublesResult.objects.filter(Q(doublesId1__player1 = currentUser) | Q(doublesId1__player2 = currentUser) | Q(doublesId2__player1 = currentUser) | Q(doublesId2__player2 = currentUser))
	return render(request,"main/doubles.html", {'form' : form, 'formChallenge' : formChallenge, 'formFillSlot' : formFillSlot, 'doublesResults' : doublesResults, 'username' : currentUser.username})

@login_required(login_url="/login/")
def activities(request):
	return render(request,"main/activities.html")

@login_required(login_url="/login/")
def events(request):
	currentUser = request.user

	userSports = UserSport.objects.filter(playerId = currentUser)
	sportsList = []
	for sport in userSports:
		try:
			sportsList.append((sport.sportName.sportName, sport.sportName.sportName))
		except sport.sportName.DoesNotExist:
			print(str(e))
	
	locationList = []
	for sport in userSports:
		try:
			sportsLocation = LocationSport.objects.filter(sportName = sport.sportName.sportName)
			for location in sportsLocation:
				tupleAdded = ((location.locationId.locationName, location.locationId.locationName))
				if tupleAdded not in locationList:
					locationList.append(tupleAdded)
		except sport.sportName.DoesNotExist:
			print(str(e))

	form = EventForm(tuple(locationList), tuple(sportsList))

	expiredEventsList = Event.objects.filter(startDate__lt = datetime.now())
	expiredEvents = EventParticipant.objects.filter(userId = currentUser, eventId__in = expiredEventsList, status = 'Waiting').update(status = 'Expired') 
	expiredRequests = EventJoiningRequest.objects.filter(eventId__in = expiredEventsList, status = 'Waiting').update(status = 'Expired') 

	scheduledEvents = EventParticipant.objects.filter(userId=currentUser, status='Accepted')
	scheduledEventsList = []
	for item in scheduledEvents:
		scheduledEventsList.append(item.eventId.eventId)

	cancelledEvents = EventParticipant.objects.filter(userId=currentUser, status='Cancelled')
	for item in cancelledEvents:
		scheduledEventsList.append(item.eventId.eventId)

	eventsRequestSent = EventJoiningRequest.objects.filter(userId=currentUser, status__in=['Waiting','Cancelled','Rejected']).values('eventId')

	eventsList = Event.objects.exclude(Q(eventId__in=scheduledEventsList) | Q(eventId__in=eventsRequestSent))

	eventsRequestSent = EventJoiningRequest.objects.filter(userId=currentUser, status='Waiting')

	eventOrganiserList = Event.objects.filter(organiserId=currentUser)

	eventRequests = EventJoiningRequest.objects.filter(eventId__in=eventOrganiserList, status='Waiting')

	return render(request,"main/events.html", {'form' : form, 'scheduledEvents' : scheduledEvents, 'eventsList' : eventsList, 'eventRequests': eventRequests, 'eventsRequestSent': eventsRequestSent})

@login_required(login_url="/login/")
def registerUserSport(request):
	currentUser = request.user
	if request.method == 'POST':
		print(request.POST)
		form = SportForm(request.POST)
		if form.is_valid() or not form.errors:
			userSport = UserSport()
			userSport.playerId = currentUser
			userSport.sportName = Sport.objects.get(sportName = request.POST.get('sportName'))
			userSport.ladderScore = 1500
			userSport.startingDate = request.POST.get('experience')
			userSport.level = request.POST.get('level')
			userSport.save()
		else: 
			print(form.errors)
			print(form.non_field_errors)
	return redirect('/home/') 

@login_required(login_url="/login/")
def registerSinglesChallenge(request):
	currentUser = request.user
	if request.method == 'POST':
		form = SinglesChallengeForm(request.POST)
		print(form.is_valid())
		print(form.errors)
		print(form.non_field_errors)
		if form.is_valid() or not form.errors:
			print(form.errors)
			challenge = SinglesChallenge()
			challenge.playerId1 = currentUser
			challenge.playerId2 = User.objects.get(username = request.POST.get('playerName'))
			challenge.sportName = Sport.objects.get(sportName = request.POST.get('sportName'))
			challenge.startTime = request.POST.get('startTime')
			challenge.endTime = request.POST.get('endTime')
			date = request.POST.get('startDate')
			if date[2] == "/":
				month = date[0:2]
				day = date[3:5]
				year = date[6:]
				challenge.startDate = year + "-" + month + "-" + day
			else:
				challenge.startDate = date

			date = request.POST.get('endDate')
			if date[2] == "/":
				month = date[0:2]
				day = date[3:5]
				year = date[6:]
				challenge.endDate = year + "-" + month + "-" + day
			else:
				challenge.endDate = date

			challenge.locationId = Location.objects.get(locationName = request.POST.get('locationName'))
			challenge.status = 'Waiting'
			challenge.save()
		else: 
			print(form.errors)
			print(form.non_field_errors)
	return redirect('/singles/') 

def sanitiseTime(time):
	if time == "noon":
		time = datetime.strptime("12:00 pm", '%I:%M %p').time()
	elif ':' not in time:
		time = datetime.strptime(time.replace(".", ""), '%I %p').time()
	else:
		time = datetime.strptime(time.replace(".", ""), '%I:%M %p').time()
	return time
	
def notificationHelper(user, notification):
	userNotification = Notification()
	userNotification.userId = user
	userNotification.notification = notification
	userNotification.sentTime = timezone.now()
	userNotification.save()

def singlesChallengeHelper(currentUser, id1, sportName, startTime, endTime, locationName, status):
	endTime = sanitiseTime(endTime)
	startTime = sanitiseTime(startTime)
	singlesChallenge = SinglesChallenge.objects.get((Q(playerId1__username = id1) & Q(playerId2  = currentUser)) | (Q(playerId2__username = id1) & Q(playerId1  = currentUser)), sportName__sportName = sportName, 
		startTime = startTime, endTime = endTime, locationId__locationName = locationName)

	singlesChallenge.status = status
	singlesChallenge.save()

@login_required(login_url="/login/")
def rejectSinglesChallenge(request, id1, sportName, startTime, endTime, locationName):
	currentUser = request.user
	singlesChallengeHelper(currentUser, id1, sportName, startTime, endTime, locationName, 'Rejected')

	notificationText = currentUser.username + " has declined your challenge in " + sportName
	receiver = User.objects.get(username = id1)
	notificationHelper(receiver, notificationText)

	return redirect('/home/') 

@login_required(login_url="/login/")
def acceptSinglesChallenge(request, id1, sportName, startTime, endTime, locationName):
	currentUser = request.user
	singlesChallengeHelper(currentUser, id1, sportName, startTime, endTime, locationName, 'Accepted')
	
	notificationText = currentUser.username + " has accepted your challenge in " + sportName
	receiver = User.objects.get(username = id1)
	notificationHelper(receiver, notificationText)

	return redirect('/home/')

@login_required(login_url="/login/")
def clearNotification(request, notificationId):
	Notification.objects.get(pk=notificationId).delete()
	return redirect('/notifications/')

@login_required(login_url="/login/")
def clearAllNotifications(request):
	currentUser = request.user;
	item = Notification.objects.filter(userId=currentUser)
	item.delete() 
	return redirect('/notifications/')

@login_required(login_url="/login/")
def getLocations(request):
	currentUser = request.user
	# if request.method == 'POST':
	sport=request.GET.get('sportName', None)
	locationList=[]
	# try:
	sportsLocation = LocationSport.objects.filter(sportName = sport)
	for location in sportsLocation:
		tupleAdded = ((location.locationId.locationName, location.locationId.locationName))
		locationList.append(tupleAdded)
	data = {'locations': locationList}
	return JsonResponse(data)
	# except sport.sportName.DoesNotExist:

@login_required(login_url="/login/")
def getPlayerNames(request):
	currentUser = request.user
	# if request.method == 'POST':
	player=request.GET.get('playerName', None)
	sportName = request.GET.get('sportName', None)
	userList=[]
	# try:
	userObject=[]
	userObjectList = UserSport.objects.filter(playerId__username__icontains = player, sportName = sportName).exclude(playerId=currentUser);
	for u in userObjectList:
		isBlacklist1 = UserBlacklist.objects.filter(uid1=currentUser.id, uid2=u.playerId);
		isBlacklist2 = UserBlacklist.objects.filter(uid1=u.playerId, uid2=currentUser.id);
		if len(isBlacklist2)==0 and len(isBlacklist1)==0:
			userObject.append(u)
	userObject=userObject[:6]

	for user in userObject:
		userList.append(user.playerId.username)
	data = {'players': userList}
	return JsonResponse(data)

@login_required(login_url="/login/")
def getPlayerNamesDoubles(request):
	currentUser = request.user
	# if request.method == 'POST':
	player=request.GET.get('playerName', None)
	sportName = request.GET.get('sportName', None)
	userList=[]
	# try:
	userObject=[]
	userObjectList = UserSport.objects.filter(playerId__username__icontains = player, sportName = sportName).exclude(playerId=currentUser);
	print(userObjectList)
	for u in userObjectList:
		isBlacklist1 = UserBlacklist.objects.filter(uid1=currentUser.id, uid2=u.playerId);
		isBlacklist2 = UserBlacklist.objects.filter(uid1=u.playerId, uid2=currentUser.id);
		isTeam = Doubles.objects.filter(Q(Q(player1=u.playerId, player2=currentUser.id)|Q(player1=currentUser.id, player2=u.playerId)),sportName = sportName);
		isTeamRequest = DoublesFormationRequest.objects.filter(Q(Q(senderId=u.playerId, receiverId=currentUser.id)|Q(senderId=currentUser.id, receiverId=u.playerId)),sportName = sportName);
		print(isTeam)
		print(isTeamRequest)
		if len(isBlacklist2)==0 and len(isBlacklist1)==0 and len(isTeam)==0 and len(isTeamRequest)==0:
			userObject.append(u)
	userObject=userObject[:6]

	for user in userObject:
		userList.append(user.playerId.username)
	data = {'players': userList}
	print(data)
	print("SFDsdf")
	return JsonResponse(data)

@login_required(login_url="/login/")
def registerSinglesFillSlot(request):
	currentUser = request.user
	if request.method == 'POST':
		form = SinglesFillSlotForm(request.POST)
		if form.is_valid() or not form.errors:
			singlesRequest = SinglesRequest()
			singlesRequest.playerId = currentUser
			singlesRequest.sportName = Sport.objects.get(sportName = request.POST.get('sportName'))
			singlesRequest.startTime = request.POST.get('startTime')
			singlesRequest.endTime = request.POST.get('endTime')
			date = request.POST.get('startDate2')
			if date[2] == "/":
				month = date[0:2]
				day = date[3:5]
				year = date[6:]
				singlesRequest.startDate = year + "-" + month + "-" + day
			else:
				singlesRequest.startDate = date

			date = request.POST.get('endDate2')
			if date[2] == "/":
				month = date[0:2]
				day = date[3:5]
				year = date[6:]
				singlesRequest.endDate = year + "-" + month + "-" + day
			else:
				singlesRequest.endDate = date

			singlesRequest.locationId = Location.objects.get(locationName = request.POST.get('locationName'))
			singlesRequest.status = 'Waiting'
			singlesRequest.levelBase =  request.POST.get('levelBase')
			singlesRequest.levelTop = request.POST.get('levelTop')

			singlesRequest.save()

		# // matching code begins here
			import datetime

			# maxlevelMatch = 0
			requestMatched = 0
			allrequests = SinglesRequest.objects.filter(sportName = singlesRequest.sportName , locationId = singlesRequest.locationId , startDate = singlesRequest.startDate , endDate = singlesRequest.endDate);
			for requests in allrequests:
				print(requests.sportName.sportName)
				print(requests.startTime)
				print(requests.endTime)
				print(requests.status)
				print(requests.levelBase)
				print(requests.levelTop)

				print(singlesRequest.startTime)
				print(singlesRequest.levelTop)
				print(singlesRequest.levelBase)
				print(singlesRequest.endTime)

				ds1 = datetime.datetime.strptime(singlesRequest.endTime,'%H:%M').time()
				# ds2 = datetime.datetime.strptime(requests.startTime,'%H:%M')
				ds3 = datetime.datetime.strptime(singlesRequest.startTime,'%H:%M').time()
				# ds4 = datetime.datetime.strptime(requests.endTime,'%H:%M')

				if(ds1 < requests.startTime or ds3 > requests.endTime):
					continue

				if(int(singlesRequest.levelTop) < requests.levelBase or int(singlesRequest.levelBase) > requests.levelTop):
					continue

				if(singlesRequest.playerId == requests.playerId):
					continue
				if not requests.status == "Waiting":
					continue;	


				else:
					opponentId = requests.playerId
					levelOfOpp = (UserSport.objects.get(playerId = opponentId , sportName = requests.sportName)).level
					myLevel = (UserSport.objects.get(playerId = currentUser , sportName = requests.sportName)).level

					print("mylevel",myLevel)
					print(levelOfOpp)

					requestMatched = requests
					print(requestMatched)
					break
	
					# this is not exact matching please correct rating and uncomment below one to enable matchin

					# levelDif = int(myLevel)  - int(levelOfOpp)

					# if(levelDif > maxlevelMatch):
					# 	maxlevelMatch = levelDif

						# please account for friends as well

						
			if( (requestMatched) != 0):
			# this is the best user matched 


				singlesMatching = SinglesMatching()
				singlesMatching.singlesRequestId1 = singlesRequest
				singlesMatching.singlesRequestId2 = requestMatched

				if(ds3 > requestMatched.startTime ):
					singlesMatching.startTime = ds3
				else:
					singlesMatching.startTime = requestMatched.startTime					

				if(ds1 < requestMatched.endTime ):
					singlesMatching.endTime = ds1
				else:
					singlesMatching.endTime = requestMatched.endTime

				singlesMatching.startDate = singlesRequest.startDate						
				singlesMatching.endDate = singlesRequest.endDate						
				singlesMatching.location = singlesRequest.locationId	

				message = "you have been matched"

				print(message)
				notificationHelper(currentUser,message)				
				notificationHelper(requestMatched.playerId,message)			

				singlesRequest.status = "Accepted"
				singlesMatching.status = "Accepted"
				requestMatched.status = "Accepted"

				singlesMatching.save()	
				singlesRequest.save()
				requestMatched.save()	

			else:
			
				print("didn't get matched right away")		

		else: 
			print(form.errors)
			print(form.non_field_errors)

	return redirect('/singles/') 

@login_required(login_url="/login/")
def blackListUser(request, username, sportName, startTime, endTime, locationName):
	currentUser = request.user
	blacklist = UserBlacklist()
	blacklist.uid1 = currentUser
	blacklist.uid2 = User.objects.get(username = username)

	blacklist.save() 

	singlesChallengeHelper(currentUser, username, sportName, startTime, endTime, locationName, 'Rejected')

	notificationText = currentUser.username + " has declined your challenge in " + sportName
	receiver = User.objects.get(username = username)
	notificationHelper(receiver, notificationText)

	return redirect('/home/')

@login_required(login_url="/login/")
def formDoublesTeam(request):
	currentUser = request.user
	if request.method == 'POST':
		form = doublesTeamForm(request.POST)
		if form.is_valid() or not form.errors:

			doublesTeamInvite = DoublesFormationRequest()
			doublesTeamInvite.senderId = currentUser
			doublesTeamInvite.receiverId = User.objects.get(username = request.POST.get('playerName'))
			doublesTeamInvite.sportName = Sport.objects.get(sportName = request.POST.get('sportName'))
			doublesTeamInvite.teamName = request.POST.get('teamName')

			captain=request.POST.get('captain')
			if captain == YESNO_CHOICES[0][0]:
				doublesTeamInvite.captainId = User.objects.get(username = request.POST.get('playerName'))
			else:
				doublesTeamInvite.captainId = currentUser
			doublesTeamInvite.status = 'Waiting'
			doublesTeamInvite.sentTime = datetime.now()
			doublesTeamInvite.save()
		else: 
			print(form.errors)
			print(form.non_field_errors)
	return redirect('/doubles/') 

@login_required(login_url="/login/")
def rejectDoublesFormation(request, id1, sportName, captainId):
	currentUser = request.user

	print(DoublesFormationRequest.objects.filter(senderId__username = id1, receiverId  = currentUser, sportName__sportName = sportName
		, captainId__username=captainId).count())
	doublesFormationRequest = DoublesFormationRequest.objects.get(senderId__username = id1, receiverId  = currentUser, sportName__sportName = sportName
		, captainId__username=captainId)

	doublesFormationRequest.status = 'Rejected'
	doublesFormationRequest.save()

	receiverId = User.objects.get(username = id1)
	notification = currentUser.username + " has declined your request in " + sportName
	notificationHelper(receiverId,notification)

	return redirect('/home/') 

@login_required(login_url="/login/")
def acceptDoublesFormation(request, id1, sportName, captainId):
	currentUser = request.user
	print("Dvsd")
	doublesFormationRequest = DoublesFormationRequest.objects.get(senderId__username = id1, receiverId  = currentUser, sportName__sportName = sportName
		, captainId__username=captainId)

	doublesFormationRequest.status = 'Accepted'
	doublesFormationRequest.save()

	receiverId = User.objects.get(username = id1)
	notification = currentUser.username + " has accepted request in " + sportName
	notificationHelper(receiverId,notification)

	doublesTeam = Doubles();
	doublesTeam.player1 = currentUser
	doublesTeam.player2 = User.objects.get(username = id1)
	doublesTeam.captainId = User.objects.get(username = captainId)
	doublesTeam.sportName = Sport.objects.get(sportName = sportName)
	doublesTeam.teamName = doublesFormationRequest.teamName
	doublesTeam.ladderScore = 1500
	doublesTeam.formationDate=datetime.today().date()
	doublesTeam.save()

	return redirect('/home/')

@login_required(login_url="/login/")
def cancelChallenge(request, username, sportName, startTime, endTime, locationName):
	currentUser = request.user
	singlesChallengeHelper(currentUser, username, sportName, startTime, endTime, locationName, 'Cancelled')

	notificationText = currentUser.username + " has cancelled your match in " + sportName
	receiver = User.objects.get(username = username)
	notificationHelper(receiver, notificationText)

	return redirect('/home/')

def sanitiseMilitaryClock(time):
	return datetime.strptime(time, "%H:%M").time()

@login_required(login_url="/login/")
def submitSinglesResult(request):
	dict = parse_qs(request.POST.get('formData', None))
	print(dict);
	print(request.POST.get('formData', None))
	print(bool(dict))
	data = {}
	if (bool(dict)):
		username = dict['username'][0]
		location = Location.objects.get(locationName = dict['locationId'][0])
		item = SinglesResult.objects.get(pk=int(dict['resultId'][0]))
		item.locationId = location
		item.endTime = sanitiseMilitaryClock(dict['endTime'][0])
		item.startTime = sanitiseMilitaryClock(dict['startTime'][0]) 
		item.startDate = dict['startDate'][0]
		item.endDate = dict['endDate'][0]
		item.matchScore = dict['matchScore'][0]
		if item.playerId1.username == username:
			item.communityRatingTo2 = int(dict['communityRating'][0])
			item.levelTo2 = int(dict['level'][0])
			if item.status == "Player2Filled":
				item.status = "TwoFilled"
			else: 
				item.status = "Player1Filled"
		else:
			item.communityRatingTo1 = int(dict['communityRating'][0])
			item.levelTo1 = int(dict['level'][0])
			if item.status == "Player1Filled":
				item.status = "TwoFilled"
			else:
				item.status = "Player2Filled"

		if dict['winner'] == 'Yes':
			winnerObject = User.objects.get(username=username)
			loserObject = User.objects.get(username=dict['playerName'][0])
			item.victorId = winnerObject
		else:
			winnerObject = User.objects.get(username=dict['playerName'][0])
			loserObject = User.objects.get(username=username)
			item.victorId = winnerObject

		winnerUserSport = UserSport.objects.get(playerId=winnerObject, sportName=item.sportName)
		winnerUserSport.ladderScore += (3000-winnerUserSport.ladderScore)*0.05
		winnerUserSport.save()

		loserUserSport = UserSport.objects.get(playerId=loserObject, sportName=item.sportName)
		loserUserSport.ladderScore -= (loserUserSport.ladderScore)*0.05
		loserUserSport.save()

		item.save()
		data['success'] = 'success'
	else:
		data['success'] = 'failure'
	return JsonResponse(data)

@login_required(login_url="/login/")
def submitDoublesResult(request):
	dict = parse_qs(request.POST.get('formData', None))
	data = {}
	if (bool(dict)):
		userTeamName = dict['userTeamName'][0]
		location = Location.objects.get(locationName = dict['locationId'][0])
		item = DoublesResult.objects.get(pk=int(dict['resultId'][0]))
		item.locationId = location
		item.endTime = sanitiseMilitaryClock(dict['endTime'][0])
		item.startTime = sanitiseMilitaryClock(dict['startTime'][0]) 
		item.startDate = dict['startDate'][0]
		item.endDate = dict['endDate'][0]
		item.matchScore = dict['matchScore'][0]
		if item.doublesId1.teamName == userTeamName:
			userTeam = item.doublesId1
			opponentTeam = item.doublesId2
			item.communityRatingTo2 = int(dict['communityRating'][0])
			item.levelTo2 = int(dict['level'][0])
			if item.status == "Player2Filled":
				item.status = "TwoFilled"
			else: 
				item.status = "Player1Filled"
		else:
			userTeam = item.doublesId2
			opponentTeam = item.doublesId1
			item.communityRatingTo1 = int(dict['communityRating'][0])
			item.levelTo1 = int(dict['level'][0])
			if item.status == "Player1Filled":
				item.status = "TwoFilled"
			else:
				item.status = "Player2Filled"

		if dict['winner'] == 'Yes':
			winnerObject = userTeam
			loserObject = opponentTeam
			item.victorId = winnerObject
		else:
			winnerObject = opponentTeam
			loserObject = userTeam
			item.victorId = opponentTeam

		winnerObject.ladderScore += (3000-winnerObject.ladderScore)*0.05
		winnerObject.save()

		loserObject.ladderScore -= (loserObject.ladderScore)*0.05
		loserObject.save()

		item.save()
		data['success'] = 'success'
	else:
		data['success'] = 'failure'
	return JsonResponse(data)

@login_required(login_url="/login/")
def submitTeamResult(request):
	dict = parse_qs(request.POST.get('formData', None))
	data = {}
	if (bool(dict)):
		userTeamName = dict['userTeamName'][0]
		location = Location.objects.get(locationName = dict['locationId'][0])
		item = TeamResult.objects.get(pk=int(dict['resultId'][0]))
		item.locationId = location
		item.endTime = sanitiseMilitaryClock(dict['endTime'][0])
		item.startTime = sanitiseMilitaryClock(dict['startTime'][0]) 
		item.startDate = dict['startDate'][0]
		item.endDate = dict['endDate'][0]
		item.matchScore = dict['matchScore'][0]
		if item.teamId1.teamName == userTeamName:
			userTeam = item.teamId1
			opponentTeam = item.teamId2
			item.communityRatingTo2 = int(dict['communityRating'][0])
			item.levelTo2 = int(dict['level'][0])
			if item.status == "Player2Filled":
				item.status = "TwoFilled"
			else: 
				item.status = "Player1Filled"
		else:
			userTeam = item.teamId2
			opponentTeam = item.teamId1
			item.communityRatingTo1 = int(dict['communityRating'][0])
			item.levelTo1 = int(dict['level'][0])
			if item.status == "Player1Filled":
				item.status = "TwoFilled"
			else:
				item.status = "Player2Filled"

		if dict['winner'] == 'Yes':
			winnerObject = userTeam
			loserObject = opponentTeam
			item.victorId = winnerObject
		else:
			winnerObject = opponentTeam
			loserObject = userTeam
			item.victorId = opponentTeam

		winnerObject.ladderScore += (3000-winnerObject.ladderScore)*0.05
		winnerObject.save()

		loserObject.ladderScore -= (loserObject.ladderScore)*0.05
		loserObject.save()

		item.save()
		data['success'] = 'success'
	else:
		data['success'] = 'failure'
	return JsonResponse(data)

@login_required(login_url="/login/")
def team(request):
	currentUser = request.user

	userSports = UserSport.objects.filter(playerId = currentUser)
	sportsList = []
	for sport in userSports:
		try:
			sportsList.append((sport.sportName.sportName, sport.sportName.sportName))
		except sport.sportName.DoesNotExist:
			print(str(e))
	userTeams=Team.objects.filter(captainId = currentUser)
	teamList=[]
	for team in userTeams:
		try:
			teamList.append((team.teamName, team.teamName))
		except team.teamName.DoesNotExist:
			print(str(e))
	print(tuple(sportsList))
	addTeam = addTeamForm(tuple(sportsList))
	addPlayer = addPlayerForm(tuple(teamList))
	sendRequestTeam = sendRequestTeamForm(tuple(sportsList))
	# print(addTeam)

	locationList = []
	for sport in userSports:
		try:
			sportsLocation = LocationSport.objects.filter(sportName = sport.sportName.sportName)
			for location in sportsLocation:
				tupleAdded = ((location.locationId.locationName, location.locationId.locationName))
				if tupleAdded not in locationList:
					locationList.append(tupleAdded)
		except sport.sportName.DoesNotExist:
			print(str(e))

	formChallenge = TeamChallengeForm(tuple(locationList), tuple(sportsList))

	formFillSlot = TeamFillSlotForm(tuple(sportsList))


	# form = doublesTeamForm(tuple(sportsList))
	# return render(request,"main/doubles.html", {'form' : form, 'formChallenge' : formChallenge, 'formFillSlot' : formFillSlot})

	userTeamsPlayer = TeamPlayers.objects.filter(playerId = currentUser).values('teamId')
	teamResultsFirst =  TeamResult.objects.filter(teamId1__in = userTeamsPlayer)
	teamResultsSecond =  TeamResult.objects.filter(teamId2__in = userTeamsPlayer)
	return render(request,"main/team.html", {'addTeamForm' : addTeam, 'addPlayerForm' : addPlayer, 'sendRequestForm' : sendRequestTeam, 'formChallenge' : formChallenge, 'formFillSlot' : formFillSlot, 'teamResultsFirst' : teamResultsFirst, 'teamResultsSecond':teamResultsSecond})

@login_required(login_url="/login/")
def makeTeam(request):
	currentUser = request.user
	if request.method == 'POST':
		form = addTeamForm(request.POST)
		if form.is_valid() or not form.errors:

			team = Team()
			team.teamName = request.POST.get('teamName')
			team.maximumplayers = request.POST.get('maxPlayers')
			team.sportName = Sport.objects.get(sportName = request.POST.get('sportName'))

			team.captainId = currentUser
			team.ladderScore = 1500
			team.communityRating = 1500
			team.formationDate=datetime.today().date()
			team.city = request.POST.get('city')
			team.state = request.POST.get('state')
			team.country = request.POST.get('country')
			team.save()

			teamPlayer = TeamPlayers()
			teamPlayer.teamId = team
			teamPlayer.playerId = currentUser
			teamPlayer.startDate = datetime.today().date()

			teamPlayer.save()

		else: 
			print(form.errors)
			print(form.non_field_errors)
	return redirect('/team/') 

@login_required(login_url="/login/")
def getPlayerNamesTeam(request):
	currentUser = request.user
	# if request.method == 'POST':
	player=request.GET.get('playerName', None)
	teamName = request.GET.get('teamName', None)
	userList=[]
	# try:
	userObject=[]
	team = Team.objects.get(teamName = teamName, captainId = currentUser)
	userObjectList = UserSport.objects.filter(playerId__username__icontains = player, sportName = team.sportName).exclude(playerId=currentUser);
	print(userObjectList)
	print(player)
	for u in userObjectList:
		isBlacklist1 = UserBlacklist.objects.filter(uid1=currentUser.id, uid2=u.playerId);
		isBlacklist2 = UserBlacklist.objects.filter(uid1=u.playerId, uid2=currentUser.id);
		isTeam = TeamPlayers.objects.filter(playerId = u.playerId, teamId = team);
		isTeamRequest = TeamJoiningRequest.objects.filter(playerId = u.playerId, teamId = team, status= 'Waiting');

		if len(isBlacklist2)==0 and len(isBlacklist1)==0 and len(isTeam)==0 and len(isTeamRequest)==0:
			userObject.append(u)
	userObject=userObject[:6]

	for user in userObject:
		userList.append(user.playerId.username)
	data = {'players': userList}
	print(data)
	print("SFDsdf")
	return JsonResponse(data)

@login_required(login_url="/login/")
def sendRequestTeamJoin(request):
	currentUser = request.user
	teamName=request.GET.get('teamName', None)
	sportName = request.GET.get('sportName', None)
	teamList=[]
	# try:
	print(teamName)
	print(sportName)
	teamObject=set()
	team = Team.objects.filter(teamName__icontains = teamName, sportName__sportName = sportName)

	print(team)
	for t in team:
		isTeam = TeamPlayers.objects.filter(playerId = currentUser, teamId = team);
		isTeamRequest = TeamJoiningRequest.objects.filter(playerId = currentUser, teamId = team, status= 'Waiting');

		if len(isTeam)==0 and len(isTeamRequest)==0:
			teamObject.add(t)
	newTeamObject=list(teamObject)[:6]

	for t in newTeamObject:
		teamList.append(t.teamName)
	data = {'teams': teamList}
	print(data)
	print("SFDsdf")
	return JsonResponse(data)

@login_required(login_url="/login/")
def findCaptainTeam(request):
	currentUser = request.user
	teamName=request.GET.get('teamName', None)
	sportName = request.GET.get('sportName', None)
	captainList=[]
	print(teamName)
	print(sportName)
	teamObject=set()
	team = Team.objects.filter(teamName = teamName, sportName__sportName = sportName)

	print(team)
	# for t in team:
	# 	# isBlacklist1 = UserBlacklist.objects.filter(uid1=currentUser.id, uid2=u.playerId);
	# 	# isBlacklist2 = UserBlacklist.objects.filter(uid1=u.playerId, uid2=currentUser.id);
	# 	isTeam = TeamPlayers.objects.filter(playerId = currentUser, teamId = team);
	# 	isTeamRequest = TeamJoiningRequest.objects.filter(playerId = currentUser, teamId = team, status= 'Waiting');

	# 	if len(isTeam)==0 and len(isTeamRequest)==0:
	# 		teamObject.add(t)

	# newTeamObject=list(teamObject)

	for t in team:
		captainList.append(t.captainId.username)
	data = {'captains': captainList, 'number' :len(captainList)}
	print(data)
	print("SFDsdf")
	return JsonResponse(data)

@login_required(login_url="/login/")
def getUsernames(request):
	currentUser = request.user
	username=request.GET.get('username', None)
	users = User.objects.filter(username__icontains=username)
	userList=[]
	for u in users:
		if u != currentUser:
			userList.append(u.username)
	data = {'userList': userList, 'number' :len(userList)}
	return JsonResponse(data)


@login_required(login_url="/login/")
def addPlayerTeam(request):
	currentUser = request.user
	if request.method == 'POST':
		form = addPlayerForm(request.POST)
		if form.is_valid() or not form.errors:

			teamRequest = TeamJoiningRequest()
			teamRequest.teamId = Team.objects.get(teamName = request.POST.get('teamName'), captainId = currentUser)
			teamRequest.playerId = User.objects.get(username = request.POST.get('playerName'))

			teamRequest.status = 'Waiting'
			teamRequest.requestType = 'Recruiting'
			teamRequest.sentDate=datetime.today().date()
			teamRequest.position = request.POST.get('position')
			teamRequest.save()

		else: 
			print(form.errors)
			print(form.non_field_errors)
	return redirect('/team/')

@login_required(login_url="/login/")
def rejectTeamInvite(request, teamName, sportName, captainId):
	currentUser = request.user

	# print(DoublesFormationRequest.objects.filter(senderId__username = id1, receiverId  = currentUser, sportName__sportName = sportName
	# 	, captainId__username=captainId).count())
	teamRequest = TeamJoiningRequest.objects.get(teamId__teamName = id1, playerId  = currentUser, teamId__sportName__sportName = sportName
		, teamId__captainId__username=captainId)

	teamRequest.status = 'Rejected'
	teamRequest.save()

	receiverId = User.objects.get(username = captainId)
	notification = currentUser.username + " has declined your request to join team " + teamRequest.teamId.teamName
	notificationHelper(receiverId,notification)

	return redirect('/home/') 

@login_required(login_url="/login/")
def acceptTeamInvite(request, teamName, sportName, captainId):
	currentUser = request.user
	teamRequest = TeamJoiningRequest.objects.get(teamId__teamName = teamName, playerId  = currentUser, teamId__sportName__sportName = sportName
		, teamId__captainId__username=captainId)

	teamRequest.status = 'Accepted'
	teamRequest.save()

	receiverId = User.objects.get(username = captainId)
	notification = currentUser.username + " has accepted your request to join team " + teamRequest.teamId.teamName
	notificationHelper(receiverId,notification)

	teamPlayer = TeamPlayers()
	teamPlayer.teamId = teamRequest.teamId
	teamPlayer.playerId = currentUser
	teamPlayer.startDate = datetime.today().date()
	teamPlayer.position = teamRequest.position

	teamPlayer.save()
	return redirect('/home/')


@login_required(login_url="/login/")
def sendJoinRequestTeam(request):
	currentUser = request.user
	if request.method == 'POST':
		form = sendRequestTeamForm(request.POST)
		if form.is_valid() or not form.errors:

			teamRequest = TeamJoiningRequest()
			teamRequest.teamId = Team.objects.get(teamName = request.POST.get('teamName'), captainId__username = request.POST.get('captainName'))
			teamRequest.playerId = User.objects.get(username = currentUser)

			teamRequest.status = 'Waiting'
			teamRequest.requestType = 'Joining'
			teamRequest.sentDate=datetime.today().date()
			teamRequest.position = request.POST.get('position')
			teamRequest.save()

		else: 
			print(form.errors)
			print(form.non_field_errors)
	return redirect('/team/')

@login_required(login_url="/login/")
def rejectJoinTeamRequest(request, teamName, sportName, playerName):
	currentUser = request.user

	# print(DoublesFormationRequest.objects.filter(senderId__username = id1, receiverId  = currentUser, sportName__sportName = sportName
	# 	, captainId__username=captainId).count())
	teamRequest = TeamJoiningRequest.objects.get(teamId__teamName = teamName, playerId  = User.objects.get(username=playerName), teamId__sportName__sportName = sportName
		, teamId__captainId=currentUser)

	teamRequest.status = 'Rejected'
	teamRequest.save()

	receiverId = User.objects.get(username = playerName)
	notification = currentUser.username + " has declined your request to join team " + teamRequest.teamId.teamName
	notificationHelper(receiverId,notification)
	return redirect('/home/') 

@login_required(login_url="/login/")
def acceptJoinTeamRequest(request, teamName, sportName, playerName):
	currentUser = request.user
	print("Dvsd")
	teamRequest = TeamJoiningRequest.objects.get(status='Waiting', teamId__teamName = teamName, playerId__username  = playerName, teamId__sportName__sportName = sportName, teamId__captainId=currentUser)

	teamRequest.status = 'Accepted'
	teamRequest.save()

	receiverId = User.objects.get(username = playerName)
	notification = currentUser.username + " has accepted your request to join team " + teamRequest.teamId.teamName
	notificationHelper(receiverId,notification)

	teamPlayer = TeamPlayers()
	teamPlayer.teamId = teamRequest.teamId
	teamPlayer.playerId = User.objects.get(username = playerName)
	teamPlayer.startDate = datetime.today().date()
	teamPlayer.position = teamRequest.position

	teamPlayer.save()
	return redirect('/home/')

@login_required(login_url="/login/")
def getUserTeamSport(request):
	currentUser = request.user
	sport=request.GET.get('sportName', None)
	teamList=[]
	# try:
	teams = Doubles.objects.filter(sportName__sportName = sport, captainId =currentUser)
	for team in teams:
		# tupleAdded = ((location.locationId.locationName, location.locationId.locationName))
		teamList.append(team.teamName)
	data = {'teams': teamList, 'number' : len(teamList)}
	print(data)
	return JsonResponse(data)

@login_required(login_url="/login/")
def getDoubleSportTeam(request):
	currentUser = request.user
	teamName=request.GET.get('teamName', None)
	sportName = request.GET.get('sportName', None)
	teamNameUser=request.GET.get('teamNameUser', None)
	teamList=[]
	print(teamName)
	print(sportName)
	teamObject=set()
	team = Doubles.objects.filter(teamName__icontains = teamName, sportName__sportName = sportName)
	teamUser = Doubles.objects.get(teamName=teamNameUser, sportName__sportName=sportName, captainId=currentUser)
	print(team)
	for t in team:
		if t.player1!=teamUser.player1 and t.player1!=teamUser.player2 and t.player2!=teamUser.player1 and t.player2!=teamUser.player2:
			teamObject.add(t)
	newTeamObject=list(teamObject)[:6]

	for t in newTeamObject:
		teamList.append(t.teamName)
	data = {'teams': teamList}
	print(data)
	print("SFDsdf")
	return JsonResponse(data)

@login_required(login_url="/login/")
def findCaptainDoubles(request):
	currentUser = request.user
	teamName=request.GET.get('teamName', None)
	sportName = request.GET.get('sportName', None)
	captainList=[]
	print(teamName)
	print(sportName)
	team = Doubles.objects.filter(teamName = teamName, sportName__sportName = sportName)

	print(team)
	for t in team:
		captainList.append(t.captainId.username)
	data = {'captains': captainList, 'number' :len(captainList)}
	print(data)
	print("SFDsdf")
	return JsonResponse(data)

@login_required(login_url="/login/")
def registerDoublesChallenge(request):
	currentUser = request.user
	if request.method == 'POST':
		form = DoublesChallengeForm(request.POST)
		if form.is_valid() or not form.errors:
			challenge = DoublesChallenge()
			doubles1=Doubles.objects.get(captainId=currentUser, teamName=request.POST.get('teamNameUser'), sportName = request.POST.get('sportName'))
			doubles2=Doubles.objects.get(captainId__username=request.POST.get('captainName'), teamName=request.POST.get('teamNameOpponent'), sportName = request.POST.get('sportName'))
			challenge.doublesId1 = doubles1
			challenge.doublesId2 = doubles2
			challenge.sportName = Sport.objects.get(sportName = request.POST.get('sportName'))
			challenge.startTime = request.POST.get('startTime')
			challenge.endTime = request.POST.get('endTime')
			date = request.POST.get('startDate')
			if date[2] == "/":
				month = date[0:2]
				day = date[3:5]
				year = date[6:]
				challenge.startDate = year + "-" + month + "-" + day
			else:
				challenge.startDate = date

			date = request.POST.get('endDate')
			if date[2] == "/":
				month = date[0:2]
				day = date[3:5]
				year = date[6:]
				challenge.endDate = year + "-" + month + "-" + day
			else:
				challenge.endDate = date

			challenge.locationId = Location.objects.get(locationName = request.POST.get('locationName'))
			challenge.status = 'Waiting'
			challenge.save()
		else: 
			print(form.errors)
			print(form.non_field_errors)
	return redirect('/doubles/') 

@login_required(login_url="/login/")
def rejectDoublesChallenge(request, id1, id2, sportName, startTime, endTime, locationName):
	currentUser = request.user
	endTime = datetime.strptime(endTime.replace(".", ""), '%I:%M %p').time()
	startTime = datetime.strptime(startTime.replace(".", ""), '%I:%M %p').time()
	print(DoublesChallenge.objects.filter(doublesId1__teamName = id1, doublesId2__teamName = id2, doublesId2__captainId=currentUser, sportName__sportName = sportName
		, locationId__locationName = locationName, startTime = startTime, endTime = endTime).count())
	doublesChallenge = DoublesChallenge.objects.get(doublesId1__teamName = id1, doublesId2__teamName = id2, doublesId2__captainId=currentUser, sportName__sportName = sportName
		, locationId__locationName = locationName, startTime = startTime, endTime = endTime)

	doublesChallenge.status = 'Rejected'
	doublesChallenge.save()

	receiverId=User.objects.get(username=doublesChallenge.doublesId1.captainId.username)
	notification = doublesChallenge.doublesId2.teamName + " has declined your doubles team challenge in " + sportName
	notificationHelper(receiverId,notification)
	return redirect('/home/') 

@login_required(login_url="/login/")
def acceptDoublesChallenge(request, id1, id2, sportName, startTime, endTime, locationName):
	currentUser = request.user
	endTime = datetime.strptime(endTime.replace(".", ""), '%I:%M %p').time()
	startTime = datetime.strptime(startTime.replace(".", ""), '%I:%M %p').time()
	print(DoublesChallenge.objects.filter(doublesId1__teamName = id1, doublesId2__teamName = id2, doublesId2__captainId=currentUser, sportName__sportName = sportName
		, locationId__locationName = locationName, startTime = startTime, endTime = endTime).count())
	doublesChallenge = DoublesChallenge.objects.get(doublesId1__teamName = id1, doublesId2__teamName = id2, doublesId2__captainId=currentUser, sportName__sportName = sportName
		, locationId__locationName = locationName, startTime = startTime, endTime = endTime)

	doublesChallenge.status = 'Accepted'
	doublesChallenge.save()

	receiverId=User.objects.get(username=doublesChallenge.doublesId1.captainId.username)
	notification = doublesChallenge.doublesId2.teamName + " has accepted your doubles team challenge in " + sportName
	notificationHelper(receiverId,notification)
	return redirect('/home/') 

@login_required(login_url="/login/")
def registerTeamChallenge(request):
	currentUser = request.user
	if request.method == 'POST':
		form = TeamChallengeForm(request.POST)
		if form.is_valid() or not form.errors:
			challenge = TeamChallenge()
			team1=Team.objects.get(captainId=currentUser, teamName=request.POST.get('teamNameUser'), sportName = request.POST.get('sportName'))
			team2=Team.objects.get(captainId__username=request.POST.get('captainName'), teamName=request.POST.get('teamNameOpponent'), sportName = request.POST.get('sportName'))
			challenge.teamId1 = team1
			challenge.teamId2 = team2
			challenge.sportName = Sport.objects.get(sportName = request.POST.get('sportName'))
			challenge.startTime = request.POST.get('startTime')
			challenge.endTime = request.POST.get('endTime')
			date = request.POST.get('startDate')
			if date[2] == "/":
				month = date[0:2]
				day = date[3:5]
				year = date[6:]
				challenge.startDate = year + "-" + month + "-" + day
			else:
				challenge.startDate = date

			date = request.POST.get('endDate')
			if date[2] == "/":
				month = date[0:2]
				day = date[3:5]
				year = date[6:]
				challenge.endDate = year + "-" + month + "-" + day
			else:
				challenge.endDate = date

			challenge.locationId = Location.objects.get(locationName = request.POST.get('locationName'))
			challenge.status = 'Waiting'
			challenge.save()
		else: 
			print(form.errors)
			print(form.non_field_errors)
	return redirect('/team/') 

@login_required(login_url="/login/")
def rejectTeamChallenge(request, id1, id2, sportName, startTime, endTime, locationName):
	currentUser = request.user
	endTime = datetime.strptime(endTime.replace(".", ""), '%I:%M %p').time()
	startTime = datetime.strptime(startTime.replace(".", ""), '%I:%M %p').time()
	# print(TeamChallenge.objects.filter(teamId1__teamName = id1, teamId2__teamName = id2, teamId2__captainId=currentUser.username, sportName__sportName = sportName
	# 	, locationId__locationName = locationName, startTime = startTime, endTime = endTime).count())
	teamChallenge = TeamChallenge.objects.get(teamId1__teamName = id1, teamId2__teamName = id2, teamId2__captainId=currentUser, teamId1__sportName__sportName = sportName
		, locationId__locationName = locationName, startTime = startTime, endTime = endTime)

	teamChallenge.status = 'Rejected'
	teamChallenge.save()

	receiverId=User.objects.get(username=teamChallenge.teamId1.captainId.username)
	notification = teamChallenge.teamId2.teamName + " has declined your team challenge in " + teamChallenge.teamId1.sportName.sportName
	notificationHelper(receiverId,notification)
	return redirect('/home/') 

@login_required(login_url="/login/")
def acceptTeamChallenge(request, id1, id2, sportName, startTime, endTime, locationName):
	currentUser = request.user
	endTime = datetime.strptime(endTime.replace(".", ""), '%I:%M %p').time()
	startTime = datetime.strptime(startTime.replace(".", ""), '%I:%M %p').time()
	# print(TeamChallenge.objects.filter(teamId1__teamName = id1, teamId2__teamName = id2, teamId2__captainId=currentUser.username, sportName__sportName = sportName
	# 	, locationId__locationName = locationName, startTime = startTime, endTime = endTime).count())
	teamChallenge = TeamChallenge.objects.get(teamId1__teamName = id1, teamId2__teamName = id2, teamId2__captainId=currentUser, teamId1__sportName__sportName = sportName
		, locationId__locationName = locationName, startTime = startTime, endTime = endTime)

	teamChallenge.status = 'Accepted'
	teamChallenge.save()

	receiverId=User.objects.get(username=teamChallenge.teamId1.captainId.username)
	notification = teamChallenge.teamId2.teamName + " has accepted your team challenge in " + teamChallenge.teamId1.sportName.sportName
	notificationHelper(receiverId,notification)
	return redirect('/home/') 

@login_required(login_url="/login/")
def getUserSportTeamsList(request):
	currentUser = request.user
	sport=request.GET.get('sportName', None)
	teamList=[]
	# try:
	teams = Team.objects.filter(sportName__sportName = sport, captainId =currentUser)
	for team in teams:
		teamList.append(team.teamName)
	data = {'teams': teamList, 'number' : len(teamList)}
	print(data)
	return JsonResponse(data)

	

@login_required(login_url="/login/")
def getOpponentTeamsListChallenge(request):
	currentUser = request.user
	teamName=request.GET.get('teamName', None)
	sportName = request.GET.get('sportName', None)
	teamNameUser=request.GET.get('teamNameUser', None)
	teamList=[]
	print(teamName)
	print(sportName)
	teamObject=set()
	team = Team.objects.filter(teamName__icontains = teamName, sportName__sportName = sportName)
	teamUser = Team.objects.get(teamName=teamNameUser, sportName__sportName=sportName, captainId=currentUser)
	print(team)
	for t in team:
		# if t.player1!=teamUser.player1 and t.player1!=teamUser.player2 and t.player2!=teamUser.player1 and t.player2!=teamUser.player2:
		teamBlacklist=TeamBlacklist.objects.filter(Q(teamId1=t,teamId2=teamUser)|Q(teamId1=teamUser,teamId2=t))
		if len(teamBlacklist)==0:
			teamUserPlayers=TeamPlayers.objects.filter(teamId=teamUser)
			isPlayerInBothTeams=0

			for u in teamUserPlayers:
				teamPlayer=TeamPlayers.objects.filter(teamId=team,playerId=u.playerId)
				if len(teamPlayer) !=0:
					isPlayerInBothTeams=1
					break
			if isPlayerInBothTeams==0:
				teamObject.add(t)

	newTeamObject=list(teamObject)[:6]

	for t in newTeamObject:
		teamList.append(t.teamName)
	data = {'teams': teamList}
	print(data)
	print("SFDsdf")
	return JsonResponse(data)

def getMonth(month):
	if month == "Jan":
		return "January"
	elif month == "Feb":
		return "February"
	elif month == "Mar":
		return "March"
	elif month == "Apr":
		return "April"
	elif month == "May":
		return "May"
	elif month == "June":
		return "June"
	elif month == "July":
		return "July"
	elif month == "Aug":
		return "August"
	elif month == "Sept":
		return "September"
	elif month == "Oct":
		return "October"
	elif month == "Nov":
		return "November"
	elif month == "Dec":
		return "December"
	else:
		return "Error" 

def sanitiseDate(startDate):
	part = startDate.split()
	return datetime.strptime('%s %s %s' % (getMonth(part[0][:-1]), part[1], part[2]), '%B %d, %Y').date()

def doublesChallengeHelper(id1, id2, sportName, startTime, startDate, locationName, status):
	startTime = sanitiseTime(startTime) 
	startDate = sanitiseDate(startDate)
	doublesChallenge = DoublesChallenge.objects.get((Q(doublesId1__doublesId = id1) & Q(doublesId2__doublesId = id2)) | (Q(doublesId2__doublesId = id1) & Q(doublesId1__doublesId = id2)), sportName__sportName = sportName
		, locationId__locationName = locationName, startTime = startTime, startDate = startDate)

	doublesChallenge.status = status
	doublesChallenge.save()

def teamChallengeHelper(id1, id2, startTime, startDate, locationName, status):
	startTime = sanitiseTime(startTime) 
	startDate = sanitiseDate(startDate)
	teamChallenge = TeamChallenge.objects.get((Q(teamId1__teamId = id1) & Q(teamId2__teamId = id2)) | (Q(teamId2__teamId = id1) & Q(teamId1__teamId = id2)), 
		locationId__locationName = locationName, startTime = startTime, startDate = startDate)

	teamChallenge.status = status
	teamChallenge.save()

@login_required(login_url="/login/")
def cancelChallengeDoubles(request, id1, id2, sportName, startTime, startDate, locationName):
	doublesChallengeHelper(id1, id2, sportName, startTime, startDate, locationName, 'Cancelled')

	doublesTeam = Doubles.objects.get(doublesId = id2)
	notificationText = doublesTeam.teamName + " has cancelled your match in " + sportName
	doublesReceiver = Doubles.objects.get(doublesId = id1)
	notificationHelper(doublesReceiver.player1, notificationText)
	notificationHelper(doublesReceiver.player2, notificationText)

	return redirect('/home/') 

@login_required(login_url="/login/")
def cancelChallengeTeam(request, id1, id2, startTime, startDate, locationName):
	teamChallengeHelper(id1, id2, startTime, startDate, locationName, 'Cancelled')

	team = Team.objects.get(teamId = id2)
	notificationText = team.teamName + " has cancelled your match in " + team.sportName.sportName
	receiverTeam = Team.objects.get(teamId = id1)
	receivers = TeamPlayers.objects.filter(teamId = receiverTeam)
	for item in receivers:
		notificationHelper(item.playerId, notificationText)
	
	return redirect('/home/')

@login_required(login_url="/login/")
def registerDoublesFillSlot(request):
	currentUser = request.user
	if request.method == 'POST':
		form = DoublesFillSlotForm(request.POST)
		if form.is_valid() or not form.errors:
			doublesRequest = DoublesRequest()
			print(request.POST.get('sportName') +" "+request.POST.get('teamNameUser')+" "+currentUser.username)
			doublesRequest.doublesId = Doubles.objects.get(sportName=request.POST.get('sportName'), teamName=request.POST.get('teamNameUser'), captainId=currentUser)
			doublesRequest.sportName = Sport.objects.get(sportName = request.POST.get('sportName'))
			doublesRequest.startTime = request.POST.get('startTime')
			doublesRequest.endTime = request.POST.get('endTime')
			date = request.POST.get('startDate2')
			if date[2] == "/":
				month = date[0:2]
				day = date[3:5]
				year = date[6:]
				doublesRequest.startDate = year + "-" + month + "-" + day
			else:
				doublesRequest.startDate = date

			date = request.POST.get('endDate2')
			if date[2] == "/":
				month = date[0:2]
				day = date[3:5]
				year = date[6:]
				doublesRequest.endDate = year + "-" + month + "-" + day
			else:
				doublesRequest.endDate = date

			doublesRequest.locationId = Location.objects.get(locationName = request.POST.get('locationName'))
			doublesRequest.status = 'Waiting'
			doublesRequest.levelBase = request.POST.get('levelBase')
			doublesRequest.levelTop = request.POST.get('levelTop')
			print(request.POST.get('levelBase')+" "+request.POST.get('levelTop'))
			doublesRequest.save()

					# // matching code begins here
			# import datetime

			# # maxlevelMatch = 0
			# requestMatched = 0
			# allrequests = DoublesRequest.objects.filter(sportName = doublesRequest.sportName , locationId = doublesRequest.locationId , startDate = doublesRequest.startDate , endDate = doublesRequest.endDate);
			# for requests in allrequests:
			# 	print(requests.sportName.sportName)
			# 	print(requests.startTime)
			# 	print(requests.endTime)
			# 	print(requests.status)
			# 	print(requests.levelBase)
			# 	print(requests.levelTop)

			# 	print(doublesRequest.startTime)
			# 	print(doublesRequest.levelTop)
			# 	print(doublesRequest.levelBase)
			# 	print(doublesRequest.endTime)

			# 	ds1 = datetime.datetime.strptime(doublesRequest.endTime,'%H:%M').time()
			# 	# ds2 = datetime.datetime.strptime(requests.startTime,'%H:%M')
			# 	ds3 = datetime.datetime.strptime(doublesRequest.startTime,'%H:%M').time()
			# 	# ds4 = datetime.datetime.strptime(requests.endTime,'%H:%M')

			# 	if(ds1 < requests.startTime or ds3 > requests.endTime):
			# 		continue

			# 	if(int(doublesRequest.levelTop) < requests.levelBase or int(doublesRequest.levelBase) > requests.levelTop):
			# 		continue

			# 	if(doublesRequest.doublesId == requests.doublesId):
			# 		continue
			# 	if not requests.status == "Waiting":
			# 		continue;	


			# 	else:
			# 		# opponentId = requests.doublesId
			# 		# levelOfOpp = (UserSport.objects.get(playerId = opponentId , sportName = requests.sportName)).level
			# 		# myLevel = (UserSport.objects.get(playerId = currentUser , sportName = requests.sportName)).level

			# 		# print("mylevel",myLevel)
			# 		# print(levelOfOpp)

			# 		requestMatched = requests
			# 		# print(requestMatched)
			# 		break
	
			# 		# this is not exact matching please correct rating and uncomment below one to enable matching

			# 		# levelDif = int(myLevel)  - int(levelOfOpp)

			# 		# if(levelDif > maxlevelMatch):
			# 		# 	maxlevelMatch = levelDif

			# 			# please account for friends as well

						
			# if( (requestMatched) != 0):
			# # this is the best user matched 


			# 	doublesMatching = DoublesMatching()
			# 	doublesMatching.doublesRequestId1 = doublesRequest
			# 	doublesMatching.doublesRequestId2 = requestMatched

			# 	if(ds3 > requestMatched.startTime ):
			# 		doublesMatching.startTime = ds3
			# 	else:
			# 		doublesMatching.startTime = requestMatched.startTime					

			# 	if(ds1 < requestMatched.endTime ):
			# 		doublesMatching.endTime = ds1
			# 	else:
			# 		doublesMatching.endTime = requestMatched.endTime

			# 	doublesMatching.startDate = doublesRequest.startDate						
			# 	doublesMatching.endDate = doublesRequest.endDate						
			# 	doublesMatching.location = doublesRequest.locationId	

			# 	message = "your double team has been matched"

			# 	DoubleMatched = Doubles.objects.get(doublesId = requestMatched.doublesId.doublesId)

			# 	print(message)
			# 	notificationHelper(currentUser,message)				
			# 	notificationHelper(DoubleMatched.captainId,message)			# send the captain a notification

			# 	doublesRequest.status = "Accepted"
			# 	requestMatched.status = "Accepted"

			# 	doublesMatching.status = "Accepted"
			# 	doublesMatching.save()	
			# 	doublesRequest.save()
			# 	requestMatched.save()	

			# else:
			
			# 	print("didn't get matched right away")		


		else: 
			print(form.errors)
			print(form.non_field_errors)
	return redirect('/doubles/') 


@login_required(login_url="/login/")
def registerTeamFillSlot(request):
	currentUser = request.user
	if request.method == 'POST':
		form = SinglesFillSlotForm(request.POST)
		if form.is_valid() or not form.errors:
			teamRequest = TeamRequest()
			teamRequest.teamId = Team.objects.get(sportName=request.POST.get('sportName'), teamName=request.POST.get('teamNameUser'), captainId=currentUser)
			teamRequest.sportName = Sport.objects.get(sportName = request.POST.get('sportName'))
			teamRequest.startTime = request.POST.get('startTime')
			teamRequest.endTime = request.POST.get('endTime')
			date = request.POST.get('startDate2')
			if date[2] == "/":
				month = date[0:2]
				day = date[3:5]
				year = date[6:]
				teamRequest.startDate = year + "-" + month + "-" + day
			else:
				teamRequest.startDate = date

			date = request.POST.get('endDate2')
			if date[2] == "/":
				month = date[0:2]
				day = date[3:5]
				year = date[6:]
				teamRequest.endDate = year + "-" + month + "-" + day
			else:
				teamRequest.endDate = date

			teamRequest.locationId = Location.objects.get(locationName = request.POST.get('locationName'))
			teamRequest.status = 'Waiting'
			teamRequest.levelBase = request.POST.get('levelBase')
			teamRequest.levelTop = request.POST.get('levelTop')
			print(request.POST.get('levelBase')+" "+request.POST.get('levelTop'))
			teamRequest.save()

		# // matching code begins here
			import datetime

			# maxlevelMatch = 0
			requestMatched = 0

			teamSport = Team.objects.get(teamId = teamRequest.teamId.teamId)

			allrequests = TeamRequest.objects.filter(locationId = teamRequest.locationId , startDate = teamRequest.startDate , endDate = teamRequest.endDate);
			for requests in allrequests:

				ds1 = datetime.datetime.strptime(teamRequest.endTime,'%H:%M').time()
				# ds2 = datetime.datetime.strptime(requests.startTime,'%H:%M')
				ds3 = datetime.datetime.strptime(teamRequest.startTime,'%H:%M').time()
				# ds4 = datetime.datetime.strptime(requests.endTime,'%H:%M')

				if(ds1 < requests.startTime or ds3 > requests.endTime):
					continue

				if(int(teamRequest.levelTop) < requests.levelBase or int(teamRequest.levelBase) > requests.levelTop):
					continue

				if(teamRequest.teamId == requests.teamId):
					continue
				if not requests.status == "Waiting":
					continue;	


				else:
					# opponentId = requests.playerId
					# levelOfOpp = (UserSport.objects.get(playerId = opponentId , sportName = requests.sportName)).level
					# myLevel = (UserSport.objects.get(playerId = currentUser , sportName = requests.sportName)).level

					# print("mylevel",myLevel)
					# print(levelOfOpp)

					requestMatched = requests
					# print(requestMatched)
					break
	
					# this is not exact matching please correct rating and uncomment below one to enable matchin

					# levelDif = int(myLevel)  - int(levelOfOpp)

					# if(levelDif > maxlevelMatch):
					# 	maxlevelMatch = levelDif

						# please account for friends as well

						
			if( (requestMatched) != 0):
			# this is the best user matched 


				teamsMatching = TeamMatching()
				teamsMatching.teamRequestId1 = teamRequest
				teamsMatching.teamRequestId2 = requestMatched

				if(ds3 > requestMatched.startTime ):
					teamsMatching.startTime = ds3
				else:
					teamsMatching.startTime = requestMatched.startTime					

				if(ds1 < requestMatched.endTime ):
					teamsMatching.endTime = ds1
				else:
					teamsMatching.endTime = requestMatched.endTime

				teamsMatching.startDate = teamRequest.startDate						
				teamsMatching.endDate = teamRequest.endDate						
				teamsMatching.location = teamRequest.locationId	

				message = "your team has been matched"

				teamCaptain = Team.objects.get(teamId = requestMatched.teamId.teamId)

				print(message)
				notificationHelper(currentUser,message)				
				notificationHelper(teamCaptain.captainId,message)			

				teamRequest.status = "Accepted"
				requestMatched.status = "Accepted"

				teamsMatching.status = 'Accepted'
				teamsMatching.save()	
				teamRequest.save()
				requestMatched.save()	

			else:
			
				print("didn't get matched right away")		



		else: 
			print(form.errors)
			print(form.non_field_errors)
	return redirect('/team/') 

@login_required(login_url="/login/")
def addEvent(request):
	currentUser = request.user
	if request.method == 'POST':
		form = EventForm(request.POST)
		if form.is_valid() or not form.errors:
			event = Event()
			event.organiserId = currentUser
			event.sportName = Sport.objects.get(sportName = request.POST.get('sportName'))
			event.startTime = request.POST.get('startTime')
			event.endTime = request.POST.get('endTime')
			date = request.POST.get('startDate')
			if date[2] == "/":
				month = date[0:2]
				day = date[3:5]
				year = date[6:]
				event.startDate = year + "-" + month + "-" + day
			else:
				event.startDate = date

			date = request.POST.get('endDate')
			if date[2] == "/":
				month = date[0:2]
				day = date[3:5]
				year = date[6:]
				event.endDate = year + "-" + month + "-" + day
			else:
				event.endDate = date


			event.locationId = Location.objects.get(locationName = request.POST.get('locationName'))
			event.maxParticipants = request.POST.get('maxParticipants')
			event.description = request.POST.get('description')
			event.save()
		else: 
			print(form.errors)
			print(form.non_field_errors)
	return redirect('/events/') 

@login_required(login_url="/login/")
def joinEvent(request, eventId):
	currentUser = request.user
	joiningRequest = EventJoiningRequest()
	joiningRequest.eventId = Event.objects.get(eventId=eventId)
	joiningRequest.userId = currentUser
	joiningRequest.requestType = 'Joining'
	joiningRequest.status = 'Waiting'

	joiningRequest.save()

	return redirect('/events/') 

@login_required(login_url="/login/")
def CancelEvent(request, eventId):
	currentUser = request.user
	event = Event.objects.get(eventId=eventId)
	joiningRequest = EventJoiningRequest.objects.get(eventId=event, userId=currentUser)
	joiningRequest.status = 'Cancelled'

	joiningRequest.save()

	notificationText = currentUser.username + " has cancelled the request to your event in " + event.sportName.sportName
	receiver = event.organiserId
	notificationHelper(receiver, notificationText)

	return redirect('/events/') 

@login_required(login_url="/login/")
def acceptEventRequest(request, eventId, username):
	user = User.objects.get(username = username)
	currentUser = request.user
	joiningRequest = EventJoiningRequest.objects.get(eventId=eventId, userId=user)
	joiningRequest.status = 'Accepted'

	joiningRequest.save()

	eventParticipant = EventParticipant()
	eventParticipant.eventId = Event.objects.get(eventId=eventId)
	eventParticipant.userId = user
	eventParticipant.status = 'Accepted'

	eventParticipant.save()

	notificationText = currentUser.username + " has accepted your request to the event in " + Event.objects.get(eventId=eventId).sportName.sportName
	receiver = user
	notificationHelper(receiver, notificationText)

	return redirect('/events/')

@login_required(login_url="/login/")
def rejectEventRequest(request, eventId, username):
	user = User.objects.get(username = username)
	currentUser = request.user
	joiningRequest = EventJoiningRequest.objects.get(eventId=eventId, userId=user)
	joiningRequest.status = 'Rejected'

	joiningRequest.save()

	notificationText = currentUser.username + " has declined your request to the event in " + Event.objects.get(eventId=eventId).sportName.sportName
	receiver = user
	notificationHelper(receiver, notificationText)

	return redirect('/events/')

@login_required(login_url="/login/")
def cancelScheduledEvent(request, eventId):
	currentUser = request.user
	event = Event.objects.get(eventId=eventId)
	eventParticipant = EventParticipant.objects.get(eventId=event, userId=currentUser)
	eventParticipant.status = 'Cancelled'

	eventParticipant.save()

	notificationText = currentUser.username + " has cancelled his attendance at your event in " + event.sportName.sportName
	receiver = event.organiserId
	notificationHelper(receiver, notificationText)
	return redirect('/events/')

@login_required(login_url="/login/")
def cancelSinglesMatching(request, requestId1, requestId2):
	userMatching = SinglesMatching.objects.filter(singlesRequestId1 = SinglesRequest.objects.get(singlesRequestId=requestId1), singlesRequestId2 = SinglesRequest.objects.get(singlesRequestId=requestId2)).update(status='Cancelled')
	return redirect('/home/')

@login_required(login_url="/login/")
def cancelDoublesMatching(request, requestId1, requestId2):
	doublesMatching = DoublesMatching.objects.filter(doublesRequestId1 = DoublesRequest.objects.get(doublesRequestId=requestId1), doublesRequestId = DoublesRequest.objects.get(DoublesRequestId=requestId2)).update(status='Cancelled')
	return redirect('/home/')

@login_required(login_url="/login/")
def cancelTeamMatching(request, requestId1, requestId2):
	teamMatching = TeamMatching.objects.filter(teamRequestId1 = TeamRequest.objects.get(teamRequestId=requestId1), teamRequestId2 = TeamRequest.objects.get(teamRequestId=requestId2)).update(status='Cancelled')
	return redirect('/home/')