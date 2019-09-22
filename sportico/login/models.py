from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser

from django.db import models
from login.choices import *
from django.conf import settings
from django.core.validators import RegexValidator
from datetime import datetime

class User(AbstractUser):
	nickName = models.CharField(max_length=30, blank=True, null=True)
	birthDate = models.DateField(blank=True, null=True)
	profilePicture = models.CharField(max_length=100,blank=True, null=True)
	gender = models.CharField(max_length=30, choices = GENDER_CHOICES, blank=True, null=True)
	street = models.CharField(max_length=30, blank=True, null=True)
	city = models.CharField(max_length=30, blank=True, null=True)
	state = models.CharField(max_length=30, blank=True, null=True)
	country = models.CharField(max_length=30, blank=True, null=True)
	communityRating = models.IntegerField(blank=True, null=True)
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
	phoneNumber = models.CharField(validators=[phone_regex], max_length=15, blank=True, null=True)
	appJoinDate = models.DateField(blank=True, null=True)

	class Meta:
		managed = True
		db_table = 'appUser'

class Doubles(models.Model):
	doublesId = models.AutoField(primary_key=True)
	player1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_player1', blank=True, null=True)
	player2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_player2', blank=True, null=True)
	sportName = models.ForeignKey('Sport', on_delete=models.CASCADE, related_name='%(class)s_sportName')
	teamName = models.CharField(max_length=50, blank=True, null=True)
	captainId = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_captainId', blank=True, null=True)
	ladderScore = models.IntegerField(blank=True, null=True)
	formationDate = models.DateField(blank=True, null=True)
	disbandDate = models.DateField(blank=True, null=True)
	level = models.CharField(max_length=30, choices = LEVEL_CHOICES, blank=True, null=True)

	class Meta:
		managed = True
		db_table = 'doubles'

class DoublesBlacklist(models.Model):
	doublesId1 = models.ForeignKey('Doubles', on_delete=models.CASCADE, related_name='%(class)s_doublesId1')
	doublesId2 = models.ForeignKey('Doubles', on_delete=models.CASCADE, related_name='%(class)s_doublesId2')

	class Meta:
		managed = True
		db_table = 'doublesBlacklist'
		unique_together = (('doublesId1', 'doublesId2'),)


class DoublesChallenge(models.Model):
	doublesId1 = models.ForeignKey('Doubles', on_delete=models.CASCADE, related_name='%(class)s_doublesId1')
	doublesId2 = models.ForeignKey('Doubles', on_delete=models.CASCADE, related_name='%(class)s_doublesId2')
	sportName = models.ForeignKey('Sport', on_delete=models.CASCADE, related_name='%(class)s_sportName')
	startTime =models.TimeField()
	endTime =models.TimeField(blank=True, null=True)
	startDate = models.DateField()
	endDate = models.DateField(blank=True, null=True)
	locationId = models.ForeignKey('Location', on_delete=models.CASCADE, related_name='%(class)s_locationId')
	status = models.CharField(max_length=30, choices = STATUS_CHOICES, blank=True, null=True)

	class Meta:
		managed = True
		db_table = 'doublesChallenge'
		unique_together = (('doublesId1', 'doublesId2', 'sportName', 'startTime', 'startDate', 'locationId'),)


class DoublesFeedback(models.Model):
	doublesMatchId = models.ForeignKey('DoublesResult', on_delete=models.CASCADE, related_name='%(class)s_doublesMatchId')
	playerId1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_playerId1')
	playerId2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_playerId2')
	communityRatingTo2 = models.IntegerField(blank=True, null=True)

	class Meta:
		managed = True
		db_table = 'doublesFeedback'
		unique_together = (('doublesMatchId', 'playerId1', 'playerId2'),)


class DoublesFormationRequest(models.Model):
	senderId = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_senderId', blank=True, null=True)
	receiverId = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_receiverId', blank=True, null=True)
	captainId = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_captainId', blank=True, null=True)
	sportName = models.ForeignKey('Sport', on_delete=models.CASCADE, related_name='%(class)s_sportName', blank=True, null=True)
	teamName = models.CharField(max_length=50, null=True)
	sentTime =models.DateTimeField(blank=True, null=True)
	status = models.CharField(max_length=30, choices = STATUS_CHOICES, blank=True, null=True)

	class Meta:
		managed = True
		db_table = 'doublesFormationRequest'

class DoublesInvite(models.Model):
	doublesRequestId1 = models.ForeignKey('DoublesRequest', on_delete=models.CASCADE, related_name='%(class)s_doublesRequestId1')
	doublesRequestId2 = models.ForeignKey('DoublesRequest', on_delete=models.CASCADE, related_name='%(class)s_doublesRequestId2')
	status = models.CharField(max_length=30, choices = STATUS_CHOICES, blank=True, null=True)

	class Meta:
		managed = True
		db_table = 'doublesInvite'
		unique_together = (('doublesRequestId1', 'doublesRequestId2'),)


class DoublesMatching(models.Model):
	doublesRequestId1 = models.ForeignKey('DoublesRequest', on_delete=models.CASCADE, related_name='%(class)s_doublesRequestId1')
	doublesRequestId2 = models.ForeignKey('DoublesRequest', on_delete=models.CASCADE, related_name='%(class)s_doublesRequestId2')
	startTime = models.TimeField(blank=True, null=True)
	endTime = models.TimeField(blank=True, null=True)
	startDate = models.DateField(blank=True, null=True)
	endDate = models.DateField(blank=True, null=True)
	locationId = models.ForeignKey('Location', on_delete=models.CASCADE, related_name='%(class)s_locationId', blank=True, null=True)

	class Meta:
		managed = True
		db_table = 'doublesMatching'
		unique_together = (('doublesRequestId1', 'doublesRequestId2'),)


class DoublesRequest(models.Model):
	doublesRequestId = models.AutoField(primary_key=True)
	doublesId = models.ForeignKey('Doubles', on_delete=models.CASCADE, related_name='%(class)s_doublesId', blank=True, null=True)
	sportName = models.ForeignKey('Sport', on_delete=models.CASCADE, related_name='%(class)s_sportName', blank=True, null=True)
	startTime =models.TimeField(blank=True, null=True)
	endTime =models.TimeField(blank=True, null=True)
	startDate = models.DateField(blank=True, null=True)
	endDate = models.DateField(blank=True, null=True)
	locationId = models.ForeignKey('Location', on_delete=models.CASCADE, related_name='%(class)s_locationId', blank=True, null=True)
	status = models.CharField(max_length=30, choices = STATUS_CHOICES, blank=True, null=True)
	levelBase = models.IntegerField(choices=FILL_SLOT_LEVEL_CHOICES,blank=True, null=True)
	levelTop = models.IntegerField(choices=FILL_SLOT_LEVEL_CHOICES,blank=True, null=True)
	
	class Meta:
		managed = True
		db_table = 'doublesRequest'

class DoublesResult(models.Model):
	doublesMatchId = models.AutoField(primary_key=True)
	doublesId1 = models.ForeignKey('Doubles', on_delete=models.CASCADE, related_name='%(class)s_doublesId1', blank=True, null=True)
	doublesId2 = models.ForeignKey('Doubles', on_delete=models.CASCADE, related_name='%(class)s_doublesId2', blank=True, null=True)
	sportName = models.ForeignKey('Sport', on_delete=models.CASCADE, related_name='%(class)s_sportName', blank=True, null=True)
	locationId = models.ForeignKey('Location', on_delete=models.CASCADE, related_name='%(class)s_locationId', blank=True, null=True)
	startTime =models.TimeField(blank=True, null=True)
	endTime =models.TimeField(blank=True, null=True)
	startDate = models.DateField(blank=True, null=True)
	endDate = models.DateField(blank=True, null=True)
	communityRatingTo1 = models.IntegerField(blank=True, null=True)
	communityRatingTo2 = models.IntegerField(blank=True, null=True)
	levelTo1 = models.CharField(max_length=30, choices = LEVEL_CHOICES, blank=True, null=True)
	levelTo2 = models.CharField(max_length=30, choices = LEVEL_CHOICES, blank=True, null=True)
	matchScore = models.CharField(max_length=50, blank=True, null=True)
	victorId = models.ForeignKey('Doubles', on_delete=models.CASCADE, related_name='%(class)s_victorId', blank=True, null=True)
	status = models.CharField(max_length=30, choices = SCORESTATUS_CHOICES, blank=True, null=True)
	
	class Meta:
		managed = True
		db_table = 'doublesResult'

class Event(models.Model):
	eventId = models.AutoField(primary_key=True)
	sportName = models.ForeignKey('Sport', on_delete=models.CASCADE, related_name='%(class)s_sportName', blank=True, null=True)
	organiserId = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_organiserId')
	locationId = models.ForeignKey('Location', on_delete=models.CASCADE, related_name='%(class)s_locationId')
	startTime =models.TimeField(blank=True, null=True)
	endTime =models.TimeField(blank=True, null=True)
	startDate = models.DateField(blank=True, null=True)
	endDate = models.DateField(blank=True, null=True)
	maxParticipants = models.IntegerField(blank=True, null=True)
	description = models.CharField(max_length=1024, blank=True, null=True)

	class Meta:
		managed = True
		db_table = 'event'

class EventJoiningRequest(models.Model):
	eventId = models.ForeignKey('Event', on_delete=models.CASCADE, related_name='%(class)s_eventId')
	userId = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_userId')
	requestType = models.CharField(choices = REQUESTTYPE_CHOICES, blank=True, null=True, max_length=30)
	status = models.CharField(max_length=30, choices = STATUS_CHOICES, blank=True, null=True)

	class Meta:
		managed = True
		db_table = 'eventJoiningRequest'
		unique_together = (('eventId', 'userId'),)


class EventOrganiserFeedback(models.Model):
	eventId = models.ForeignKey('Event', on_delete=models.CASCADE, related_name='%(class)s_eventId')
	attendance = models.IntegerField(blank=True, null=True)
	comments = models.CharField(max_length=255, blank=True, null=True)

	class Meta:
		managed = True
		db_table = 'eventOrganiserFeedback'

class EventParticipant(models.Model):
	eventId = models.ForeignKey('Event', on_delete=models.CASCADE, related_name='%(class)s_eventId')
	userId = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_userId')
	status = models.CharField(max_length=30, choices = STATUS_CHOICES, blank=True, null=True)

	class Meta:
		managed = True
		db_table = 'eventParticipant'
		unique_together = (('eventId', 'userId'),)


class Location(models.Model):
	locationId = models.AutoField(primary_key=True)
	locationName = models.CharField(max_length=30)
	street = models.CharField(max_length=30, blank=True, null=True)
	city = models.CharField(max_length=30)
	state = models.CharField(max_length=30)
	country = models.CharField(max_length=30)
	description = models.CharField(max_length=30, blank=True, null=True)

	class Meta:
		managed = True
		db_table = 'location'

class LocationSport(models.Model):
	locationId = models.ForeignKey('Location', on_delete=models.CASCADE, related_name='%(class)s_locationId')
	sportName = models.CharField(max_length=50)
	description = models.CharField(max_length=255, blank=True, null=True)

	class Meta:
		managed = True
		db_table = 'locationSport'
		unique_together = (('locationId', 'sportName'),)

class NonCompetitiveMatching(models.Model):
	nonCompetitiveId = models.AutoField(primary_key=True)
	startTime =models.TimeField(blank=True, null=True)
	endTime =models.TimeField(blank=True, null=True)
	startDate = models.DateField(blank=True, null=True)
	endDate = models.DateField(blank=True, null=True)
	locationId = models.ForeignKey('Location', on_delete=models.CASCADE, related_name='%(class)s_locationId', blank=True, null=True)
	sportName = models.ForeignKey('Sport', on_delete=models.CASCADE, related_name='%(class)s_sportName', blank=True, null=True)

	class Meta:
		managed = True
		db_table = 'nonCompetitiveMatching'

class NonCompetitiveMatchingFeedback(models.Model):
	nonCompetitiveId = models.ForeignKey('NonCompetitiveMatching', on_delete=models.CASCADE, related_name='%(class)s_nonCompetitiveId')
	playerId1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_playerId1')
	playerId2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_playerId2')
	communityRating = models.IntegerField(blank=True, null=True)
	level = models.CharField(max_length=30, choices = LEVEL_CHOICES, blank=True, null=True)

	class Meta:
		managed = True
		db_table = 'nonCompetitiveMatchingFeedback'
		unique_together = (('nonCompetitiveId', 'playerId1', 'playerId2'),)


class NonCompetitiveMatchingparticipant(models.Model):
	nonCompetitiveId = models.ForeignKey('NonCompetitiveMatching', on_delete=models.CASCADE, related_name='%(class)s_nonCompetitiveId')
	singlesRequestId = models.ForeignKey('SinglesRequest', on_delete=models.CASCADE, related_name='%(class)s_singlesRequestId')
	status = models.CharField(max_length=30, choices = STATUS_CHOICES, blank=True, null=True)

	class Meta:
		managed = True
		db_table = 'nonCompetitiveMatchingparticipant'
		unique_together = (('nonCompetitiveId', 'singlesRequestId'),)

class Notification(models.Model):
	notificationId = models.AutoField(primary_key=True)
	userId = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_playerId1')
	notification = models.CharField(max_length=400, blank=True, null=True)
	sentTime = models.DateTimeField()

	class Meta:
		managed = True

class SinglesChallenge(models.Model):
	playerId1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_playerId1')
	playerId2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_playerId2')
	sportName = models.ForeignKey('Sport', on_delete=models.CASCADE, related_name='%(class)s_sportName')
	startTime = models.TimeField()
	endTime = models.TimeField(blank=True, null=True)
	startDate = models.DateField()
	endDate = models.DateField(blank=True, null=True)
	locationId = models.ForeignKey('Location', on_delete=models.CASCADE, related_name='%(class)s_locationId')
	status = models.CharField(max_length=30, choices = STATUS_CHOICES, blank=True, null=True)

	class Meta:
		managed = True
		db_table = 'singlesChallenge'
		unique_together = (('playerId1', 'playerId2', 'sportName', 'startTime', 'startDate', 'locationId'),)


class Singlesinvite(models.Model):
	singlesRequestId1 = models.ForeignKey('SinglesRequest', on_delete=models.CASCADE, related_name='%(class)s_singlesRequestId1')
	singlesRequestId2 = models.ForeignKey('SinglesRequest', on_delete=models.CASCADE, related_name='%(class)s_singlesRequestId2')
	status = models.CharField(max_length=30, choices = STATUS_CHOICES, blank=True, null=True)

	class Meta:
		managed = True
		db_table = 'singlesinvite'
		unique_together = (('singlesRequestId1', 'singlesRequestId2'),)


class SinglesMatching(models.Model):
	singlesRequestId1 = models.ForeignKey('SinglesRequest', on_delete=models.CASCADE, related_name='%(class)s_singlesRequestId1')
	singlesRequestId2 = models.ForeignKey('SinglesRequest', on_delete=models.CASCADE, related_name='%(class)s_singlesRequestId2')
	startTime =models.TimeField(blank=True, null=True)
	endTime =models.TimeField(blank=True, null=True)
	startDate = models.DateField(blank=True, null=True)
	endDate = models.DateField(blank=True, null=True)
	locationId = models.ForeignKey('Location', on_delete=models.CASCADE, related_name='%(class)s_locationId', blank=True, null=True)
	status = models.CharField(max_length=30, choices = STATUS_CHOICES, blank=True, null=True)
	status = models.CharField(max_length=30, choices = STATUS_CHOICES, blank=True, null=True)

	class Meta:
		managed = True
		db_table = 'singlesMatching'
		unique_together = (('singlesRequestId1', 'singlesRequestId2'),)


class SinglesRequest(models.Model):
	singlesRequestId = models.AutoField(primary_key=True)
	playerId = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_playerId', blank=True, null=True)
	sportName = models.ForeignKey('Sport', on_delete=models.CASCADE, related_name='%(class)s_sportName', blank=True, null=True)
	startTime =models.TimeField(blank=True, null=True)
	endTime =models.TimeField(blank=True, null=True)
	startDate = models.DateField(blank=True, null=True)
	endDate = models.DateField(blank=True, null=True)
	locationId = models.ForeignKey('Location', on_delete=models.CASCADE, related_name='%(class)s_locationId', blank=True, null=True)
	status = models.CharField(max_length=30, choices = STATUS_CHOICES, blank=True, null=True)
	levelBase = models.IntegerField(choices=FILL_SLOT_LEVEL_CHOICES,blank=True, null=True)
	levelTop = models.IntegerField(choices=FILL_SLOT_LEVEL_CHOICES,blank=True, null=True)

	class Meta:
		managed = True
		db_table = 'singlesRequest'

class SinglesResult(models.Model):
	singlesResultId = models.AutoField(primary_key=True)
	playerId1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_playerId1', blank=True, null=True)
	playerId2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_playerId2', blank=True, null=True)
	sportName = models.ForeignKey('Sport', on_delete=models.CASCADE, related_name='%(class)s_sportName', blank=True, null=True)
	locationId = models.ForeignKey('Location', on_delete=models.CASCADE, related_name='%(class)s_locationId', blank=True, null=True)
	startTime =models.TimeField(blank=True, null=True)
	endTime =models.TimeField(blank=True, null=True)
	startDate = models.DateField(blank=True, null=True)
	endDate = models.DateField(blank=True, null=True)
	communityRatingTo1 = models.IntegerField(blank=True, null=True)
	communityRatingTo2 = models.IntegerField(blank=True, null=True)
	levelTo1 = models.CharField(max_length=30, choices = LEVEL_CHOICES, blank=True, null=True)
	levelTo2 = models.CharField(max_length=30, choices = LEVEL_CHOICES, blank=True, null=True)
	matchScore = models.CharField(max_length=50, blank=True, null=True)
	victorId = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_victorId', blank=True, null=True)
	status = models.CharField(max_length=30, choices = SCORESTATUS_CHOICES, blank=True, null=True)

	class Meta:
		managed = True
		db_table = 'singlesResult'

class Sport(models.Model):
	sportName = models.CharField(primary_key=True, max_length=50)
	sporttype = models.CharField(max_length=30, choices = SPORTTYPE_CHOICES)
	description = models.CharField(max_length=255, blank=True, null=True)

	class Meta:
		managed = True
		db_table = 'sport'

class Team(models.Model):
	teamId = models.AutoField(primary_key=True)
	sportName = models.ForeignKey('Sport', on_delete=models.CASCADE, related_name='%(class)s_sportName')
	teamName = models.CharField(max_length=50)
	formationDate = models.DateField(blank=True, null=True)
	disbandDate = models.DateField(blank=True, null=True)
	captainId = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_captainId')
	numplayers = models.IntegerField(blank=True, null=True)
	maximumplayers = models.IntegerField(blank=True, null=True)
	communityRating = models.IntegerField(blank=True, null=True)
	ladderScore = models.IntegerField(blank=True, null=True)
	level = models.CharField(max_length=30, choices = LEVEL_CHOICES, blank=True, null=True)
	city = models.CharField(max_length=30, blank=True, null=True)
	state = models.CharField(max_length=30, blank=True, null=True)
	country = models.CharField(max_length=30, blank=True, null=True)
	description = models.CharField(max_length=255, blank=True, null=True)

	class Meta:
		managed = True
		db_table = 'team'

class TeamBlacklist(models.Model):
	teamId1 = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='%(class)s_teamId1')
	teamId2 = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='%(class)s_teamId2')

	class Meta:
		managed = True
		db_table = 'teamBlacklist'
		unique_together = (('teamId1', 'teamId2'),)


class TeamChallenge(models.Model):
	teamId1 = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='%(class)s_teamId1')
	teamId2 = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='%(class)s_teamId2')
	startTime =models.TimeField()
	endTime =models.TimeField(blank=True, null=True)
	startDate = models.DateField()
	endDate = models.DateField(blank=True, null=True)
	locationId = models.ForeignKey('Location', on_delete=models.CASCADE, related_name='%(class)s_locationId')
	status = models.CharField(max_length=30, choices = STATUS_CHOICES, blank=True, null=True)

	class Meta:
		managed = True
		db_table = 'teamChallenge'
		unique_together = (('teamId1', 'teamId2', 'startTime', 'startDate', 'locationId'),)


class TeamInvite(models.Model):
	teamRequestId1 = models.ForeignKey('TeamRequest', on_delete=models.CASCADE, related_name='%(class)s_teamRequestId1')
	teamRequestId2 = models.ForeignKey('TeamRequest', on_delete=models.CASCADE, related_name='%(class)s_teamRequestId2')
	status = models.CharField(max_length=30, choices = STATUS_CHOICES, blank=True, null=True)

	class Meta:
		managed = True
		db_table = 'teamInvite'
		unique_together = (('teamRequestId1', 'teamRequestId2'),)


class TeamJoiningRequest(models.Model):
	teamId = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='%(class)s_teamId', blank=True, null=True)
	playerId = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_playerId', blank=True, null=True)
	requestType = models.CharField(choices = REQUESTTYPE_CHOICES, blank=True, null=True, max_length=30)
	sentDate = models.DateField(blank=True, null=True)
	status = models.CharField(max_length=30, choices = STATUS_CHOICES, blank=True, null=True)
	position = models.CharField(max_length=30, blank=True, null=True)

	class Meta:
		managed = True
		db_table = 'teamJoiningRequest'

class TeamMatching(models.Model):
	teamRequestId1 = models.ForeignKey('TeamRequest', on_delete=models.CASCADE, related_name='%(class)s_teamRequestId1')
	teamRequestId2 = models.ForeignKey('TeamRequest', on_delete=models.CASCADE, related_name='%(class)s_teamRequestId2')
	startTime =models.TimeField(blank=True, null=True)
	endTime =models.TimeField(blank=True, null=True)
	startDate = models.DateField(blank=True, null=True)
	endDate = models.DateField(blank=True, null=True)
	locationId = models.ForeignKey('Location', on_delete=models.CASCADE, related_name='%(class)s_locationId', blank=True, null=True)
	status = models.CharField(max_length=30, choices = STATUS_CHOICES, blank=True, null=True)
	
	class Meta:
		managed = True
		db_table = 'teamMatching'
		unique_together = (('teamRequestId1', 'teamRequestId2'),)


class TeamPlayerFeedback(models.Model):
	teamMatchId = models.ForeignKey('TeamResult', on_delete=models.CASCADE, related_name='%(class)s_teamMatchId')
	player1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_player1')
	player2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_player2')
	communityRatingTo2 = models.IntegerField(blank=True, null=True)
	levelTo2 = models.CharField(max_length=30, choices = LEVEL_CHOICES, blank=True, null=True)

	class Meta:
		managed = True
		db_table = 'teamPlayerFeedback'
		unique_together = (('teamMatchId', 'player1', 'player2'),)


class TeamPlayers(models.Model):
	teamId = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='%(class)s_teamId')
	playerId = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_playerId')
	position = models.CharField(max_length=30, blank=True, null=True)
	startDate = models.DateField(blank=True, null=True)
	endDate = models.DateField(blank=True, null=True)

	class Meta:
		managed = True
		db_table = 'teamPlayers'
		unique_together = (('teamId', 'playerId'),)


class TeamRequest(models.Model):
	teamRequestId = models.AutoField(primary_key=True)
	teamId = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='%(class)s_teamId', blank=True, null=True)
	startTime =models.TimeField(blank=True, null=True)
	endTime =models.TimeField(blank=True, null=True)
	startDate = models.DateField(blank=True, null=True)
	endDate = models.DateField(blank=True, null=True)
	locationId = models.ForeignKey('Location', on_delete=models.CASCADE, related_name='%(class)s_locationId', blank=True, null=True)
	status = models.CharField(max_length=30, choices = STATUS_CHOICES, blank=True, null=True)
	levelBase = models.IntegerField(choices=FILL_SLOT_LEVEL_CHOICES,blank=True, null=True)
	levelTop = models.IntegerField(choices=FILL_SLOT_LEVEL_CHOICES,blank=True, null=True)

	class Meta:
		managed = True
		db_table = 'teamRequest'

class TeamResult(models.Model):
	teamMatchId = models.AutoField(primary_key=True)
	teamId1 = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='%(class)s_teamId1', blank=True, null=True)
	teamId2 = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='%(class)s_teamId2', blank=True, null=True)
	locationId = models.ForeignKey('Location', on_delete=models.CASCADE, related_name='%(class)s_locationId', blank=True, null=True)
	startTime =models.TimeField(blank=True, null=True)
	endTime =models.TimeField(blank=True, null=True)
	startDate = models.DateField(blank=True, null=True)
	endDate = models.DateField(blank=True, null=True)
	communityRatingTo1 = models.IntegerField(blank=True, null=True)
	communityRatingTo2 = models.IntegerField(blank=True, null=True)
	levelTo1 = models.CharField(max_length=30, choices = LEVEL_CHOICES, blank=True, null=True)
	levelTo2 = models.CharField(max_length=30, choices = LEVEL_CHOICES, blank=True, null=True)
	matchScore = models.CharField(max_length=50, blank=True, null=True)
	victorId = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='%(class)s_victorId', blank=True, null=True)
	status = models.CharField(max_length=30, choices = SCORESTATUS_CHOICES, blank=True, null=True)

	class Meta:
		managed = True
		db_table = 'teamResult'

class UserBlacklist(models.Model):
	uid1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_uid1')
	uid2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_uid2')

	class Meta:
		managed = True
		db_table = 'userBlacklist'
		unique_together = (('uid1', 'uid2'),)

class UserSport(models.Model):
	playerId = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_playerId')
	sportName = models.ForeignKey('Sport', on_delete=models.CASCADE, related_name='%(class)s_sportName')
	ladderScore = models.IntegerField(blank=True, null=True)
	startingDate = models.CharField(max_length=30, choices = EXPERIENCE_CHOICES, blank=True, null=True)
	level = models.CharField(max_length=30, choices = LEVEL_CHOICES, blank=True, null=True)

	class Meta:
		managed = True
		db_table = 'userSport'
		unique_together = (('playerId', 'sportName'),)

class UserFriend(models.Model):
	uid1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_uid1')
	uid2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_uid2')
	startTime =models.DateTimeField(blank=True, null=True)

	class Meta:
		managed = True
		db_table = 'userFriend'
		unique_together = (('uid1', 'uid2'),)

class UserFriendRequest(models.Model):
	uid1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_uid1')
	uid2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_uid2')
	sentTime =models.DateTimeField(blank=True, null=True)
	status = models.CharField(max_length=20, choices = FRIEND_CHOICES, blank=True, null=True)


	class Meta:
		managed = True
		db_table = 'userFriendRequest'
		unique_together = (('uid1', 'uid2','sentTime'),)
