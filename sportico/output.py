# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class AppUser(models.Model):
    uid = models.CharField(primary_key=True, max_length=30)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30, blank=True, null=True)
    nickname = models.CharField(max_length=30, blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    profilepicture = models.BinaryField(blank=True, null=True)
    gender = models.CharField(max_length=30, choices = GENDER_CHOICES, blank=True, null=True)
    street = models.CharField(max_length=30, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    state = models.CharField(max_length=30, blank=True, null=True)
    country = models.CharField(max_length=30, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    communityrating = models.IntegerField(blank=True, null=True)
    phonenumber = models.CharField(max_length=30)
    appjoindate = models.DateField()

    class Meta:
        managed = True
        db_table = 'AppUser'


class Doubles(models.Model):
    doublesid = models.AutoField(primary_key=True)
    player1 = models.ForeignKey(Appuser, models.DO_NOTHING, db_column='player1', blank=True, null=True)
    player2 = models.ForeignKey(Appuser, models.DO_NOTHING, db_column='player2', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'doubles'


class DoublesBlacklist(models.Model):
    doublesid1 = models.ForeignKey(Doubles, models.DO_NOTHING, db_column='doublesid1', primary_key=True)
    doublesid2 = models.ForeignKey(Doubles, models.DO_NOTHING, db_column='doublesid2')

    class Meta:
        managed = True
        db_table = 'doublesblacklist'
        unique_together = (('doublesid1', 'doublesid2'),)


class DoublesChallenge(models.Model):
    doublesid1 = models.ForeignKey(Doubles, models.DO_NOTHING, db_column='doublesid1', primary_key=True)
    doublesid2 = models.ForeignKey(Doubles, models.DO_NOTHING, db_column='doublesid2')
    sportname = models.ForeignKey('Sport', models.DO_NOTHING, db_column='sportname')
    starttime = models.TimeField()
    endtime = models.TimeField(blank=True, null=True)
    startdate = models.DateField()
    enddate = models.DateField(blank=True, null=True)
    locationid = models.ForeignKey('Location', models.DO_NOTHING, db_column='locationid')
    status = models.CharField(max_length=30, choices = STATUS_CHOICES, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'doubleschallenge'
        unique_together = (('doublesid1', 'doublesid2', 'sportname', 'starttime', 'startdate', 'locationid'),)


class DoublesFeedback(models.Model):
    doublesmatchid = models.ForeignKey('Doublesresult', models.DO_NOTHING, db_column='doublesmatchid', primary_key=True)
    playerid1 = models.ForeignKey(Appuser, models.DO_NOTHING, db_column='playerid1')
    playerid2 = models.ForeignKey(Appuser, models.DO_NOTHING, db_column='playerid2')
    communityratingto2 = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'doublesfeedback'
        unique_together = (('doublesmatchid', 'playerid1', 'playerid2'),)


class DoublesFormationRequest(models.Model):
    senderid = models.ForeignKey(Appuser, models.DO_NOTHING, db_column='senderid', blank=True, null=True)
    receiverid = models.ForeignKey(Appuser, models.DO_NOTHING, db_column='receiverid', blank=True, null=True)
    captainid = models.ForeignKey(Appuser, models.DO_NOTHING, db_column='captainid', blank=True, null=True)
    sportname = models.ForeignKey('Sport', models.DO_NOTHING, db_column='sportname', blank=True, null=True)
    senttime = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=30, choices = STATUS_CHOICES, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'doublesformationrequest'


class Doublesinvite(models.Model):
    doublesrequestid1 = models.ForeignKey('Doublesrequest', models.DO_NOTHING, db_column='doublesrequestid1', primary_key=True)
    doublesrequestid2 = models.ForeignKey('Doublesrequest', models.DO_NOTHING, db_column='doublesrequestid2')
    status = models.CharField(max_length=30, choices = STATUS_CHOICES, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'doublesinvite'
        unique_together = (('doublesrequestid1', 'doublesrequestid2'),)


class DoublesMatching(models.Model):
    doublesrequestid1 = models.ForeignKey('Doublesrequest', models.DO_NOTHING, db_column='doublesrequestid1', primary_key=True)
    doublesrequestid2 = models.ForeignKey('Doublesrequest', models.DO_NOTHING, db_column='doublesrequestid2')
    starttime = models.TimeField(blank=True, null=True)
    endtime = models.TimeField(blank=True, null=True)
    startdate = models.DateField(blank=True, null=True)
    enddate = models.DateField(blank=True, null=True)
    locationid = models.ForeignKey('Location', models.DO_NOTHING, db_column='locationid', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'doublesmatching'
        unique_together = (('doublesrequestid1', 'doublesrequestid2'),)


class DoublesRequest(models.Model):
    doublesrequestid = models.AutoField(primary_key=True)
    doublesid = models.ForeignKey(Doubles, models.DO_NOTHING, db_column='doublesid', blank=True, null=True)
    sportname = models.ForeignKey('Sport', models.DO_NOTHING, db_column='sportname', blank=True, null=True)
    starttime = models.TimeField(blank=True, null=True)
    endtime = models.TimeField(blank=True, null=True)
    startdate = models.DateField(blank=True, null=True)
    enddate = models.DateField(blank=True, null=True)
    locationid = models.ForeignKey('Location', models.DO_NOTHING, db_column='locationid', blank=True, null=True)
    status = models.CharField(max_length=30, choices = STATUS_CHOICES, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'doublesrequest'


class DoublesResult(models.Model):
    doublesmatchid = models.AutoField(primary_key=True)
    doublesid1 = models.ForeignKey(Doubles, models.DO_NOTHING, db_column='doublesid1', blank=True, null=True)
    doublesid2 = models.ForeignKey(Doubles, models.DO_NOTHING, db_column='doublesid2', blank=True, null=True)
    sportname = models.ForeignKey('Sport', models.DO_NOTHING, db_column='sportname', blank=True, null=True)
    locationid = models.ForeignKey('Location', models.DO_NOTHING, db_column='locationid', blank=True, null=True)
    starttime = models.TimeField(blank=True, null=True)
    endtime = models.TimeField(blank=True, null=True)
    startdate = models.DateField(blank=True, null=True)
    enddate = models.DateField(blank=True, null=True)
    communityratingto1 = models.IntegerField(blank=True, null=True)
    communityratingto2 = models.IntegerField(blank=True, null=True)
    levelto1 = models.CharField(max_length=30, choices = LEVEL_CHOICES, blank=True, null=True)
    levelto2 = models.CharField(max_length=30, choices = LEVEL_CHOICES, blank=True, null=True)
    matchscore = models.CharField(max_length=50, blank=True, null=True)
    victorid = models.ForeignKey(Doubles, models.DO_NOTHING, db_column='victorid', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'doublesresult'


class DoublesSport(models.Model):
    doublesid = models.ForeignKey(Doubles, models.DO_NOTHING, db_column='doublesid', primary_key=True)
    sportname = models.ForeignKey('Sport', models.DO_NOTHING, db_column='sportname')
    teamname = models.CharField(max_length=50, blank=True, null=True)
    captainnid = models.CharField(max_length=30, blank=True, null=True)
    ladderscore = models.IntegerField(blank=True, null=True)
    formationdate = models.DateField(blank=True, null=True)
    disbanddate = models.DateField(blank=True, null=True)
    level = models.CharField(max_length=30, choices = LEVEL_CHOICES, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'doublessport'
        unique_together = (('doublesid', 'sportname'),)


class Event(models.Model):
    eventid = models.AutoField(primary_key=True)
    sportname = models.ForeignKey('Sport', models.DO_NOTHING, db_column='sportname', blank=True, null=True)
    organiserid = models.ForeignKey(Appuser, models.DO_NOTHING, db_column='organiserid')
    locationid = models.ForeignKey('Location', models.DO_NOTHING, db_column='locationid')
    starttime = models.TimeField(blank=True, null=True)
    endtime = models.TimeField(blank=True, null=True)
    startdate = models.DateField(blank=True, null=True)
    enddate = models.DateField(blank=True, null=True)
    maxparticipants = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'event'


class EventJoiningRequest(models.Model):
    eventid = models.ForeignKey(Event, models.DO_NOTHING, db_column='eventid', primary_key=True)
    userid = models.ForeignKey(Appuser, models.DO_NOTHING, db_column='userid')
    requesttype = models.CharField(choices = REQUESTTYPE_CHOICES, blank=True, null=True, max_length=30)
    status = models.CharField(max_length=30, choices = STATUS_CHOICES, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'eventjoiningrequest'
        unique_together = (('eventid', 'userid'),)


class EventOrganiserFeedback(models.Model):
    eventid = models.ForeignKey(Event, models.DO_NOTHING, db_column='eventid', primary_key=True)
    attendance = models.IntegerField(blank=True, null=True)
    comments = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'eventorganiserfeedback'


class EventParticipant(models.Model):
    eventid = models.ForeignKey(Event, models.DO_NOTHING, db_column='eventid', primary_key=True)
    userid = models.ForeignKey(Appuser, models.DO_NOTHING, db_column='userid')
    status = models.CharField(max_length=30, choices = STATUS_CHOICES, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'eventparticipant'
        unique_together = (('eventid', 'userid'),)


class Location(models.Model):
    locationid = models.AutoField(primary_key=True)
    locationname = models.CharField(max_length=30)
    street = models.CharField(max_length=30, blank=True, null=True)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    description = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'location'


class LocationSport(models.Model):
    locationid = models.ForeignKey(Location, models.DO_NOTHING, db_column='locationid', primary_key=True)
    sportname = models.CharField(max_length=50)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'locationsport'
        unique_together = (('locationid', 'sportname'),)


class NonCompetitiveMatching(models.Model):
    noncompetitiveid = models.AutoField(primary_key=True)
    starttime = models.TimeField(blank=True, null=True)
    endtime = models.TimeField(blank=True, null=True)
    startdate = models.DateField(blank=True, null=True)
    enddate = models.DateField(blank=True, null=True)
    locationid = models.ForeignKey(Location, models.DO_NOTHING, db_column='locationid', blank=True, null=True)
    sportname = models.ForeignKey('Sport', models.DO_NOTHING, db_column='sportname', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'noncompetitivematching'


class NonCompetitiveMatchingFeedback(models.Model):
    noncompetitiveid = models.ForeignKey(Noncompetitivematching, models.DO_NOTHING, db_column='noncompetitiveid', primary_key=True)
    playerid1 = models.ForeignKey(Appuser, models.DO_NOTHING, db_column='playerid1')
    playerid2 = models.ForeignKey(Appuser, models.DO_NOTHING, db_column='playerid2')
    communityrating = models.IntegerField(blank=True, null=True)
    level = models.CharField(max_length=30, choices = LEVEL_CHOICES, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'noncompetitivematchingfeedback'
        unique_together = (('noncompetitiveid', 'playerid1', 'playerid2'),)


class NonCompetitiveMatchingParticipant(models.Model):
    noncompetitiveid = models.ForeignKey(Noncompetitivematching, models.DO_NOTHING, db_column='noncompetitiveid', primary_key=True)
    singlesrequestid = models.ForeignKey('Singlesrequest', models.DO_NOTHING, db_column='singlesrequestid')
    status = models.CharField(max_length=30, choices = STATUS_CHOICES, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'noncompetitivematchingparticipant'
        unique_together = (('noncompetitiveid', 'singlesrequestid'),)


class Password(models.Model):
    uid = models.ForeignKey(Appuser, models.DO_NOTHING, db_column='uid', primary_key=True)
    password = models.CharField(max_length=30)

    class Meta:
        managed = True
        db_table = 'password'


class SinglesChallenge(models.Model):
    playerid1 = models.ForeignKey(Appuser, models.DO_NOTHING, db_column='playerid1', primary_key=True)
    playerid2 = models.ForeignKey(Appuser, models.DO_NOTHING, db_column='playerid2')
    sportname = models.ForeignKey('Sport', models.DO_NOTHING, db_column='sportname')
    starttime = models.TimeField()
    endtime = models.TimeField(blank=True, null=True)
    startdate = models.DateField()
    enddate = models.DateField(blank=True, null=True)
    locationid = models.ForeignKey(Location, models.DO_NOTHING, db_column='locationid')
    status = models.CharField(max_length=30, choices = STATUS_CHOICES, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'singleschallenge'
        unique_together = (('playerid1', 'playerid2', 'sportname', 'starttime', 'startdate', 'locationid'),)


class SinglesInvite(models.Model):
    singlesrequestid1 = models.ForeignKey('Singlesrequest', models.DO_NOTHING, db_column='singlesrequestid1', primary_key=True)
    singlesrequestid2 = models.ForeignKey('Singlesrequest', models.DO_NOTHING, db_column='singlesrequestid2')
    status = models.CharField(max_length=30, choices = STATUS_CHOICES, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'singlesinvite'
        unique_together = (('singlesrequestid1', 'singlesrequestid2'),)


class SinglesMatching(models.Model):
    singlesrequestid1 = models.ForeignKey('Singlesrequest', models.DO_NOTHING, db_column='singlesrequestid1', primary_key=True)
    singlesrequestid2 = models.ForeignKey('Singlesrequest', models.DO_NOTHING, db_column='singlesrequestid2')
    starttime = models.TimeField(blank=True, null=True)
    endtime = models.TimeField(blank=True, null=True)
    startdate = models.DateField(blank=True, null=True)
    enddate = models.DateField(blank=True, null=True)
    locationid = models.ForeignKey(Location, models.DO_NOTHING, db_column='locationid', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'singlesmatching'
        unique_together = (('singlesrequestid1', 'singlesrequestid2'),)


class SinglesRequest(models.Model):
    singlesrequestid = models.AutoField(primary_key=True)
    playerid = models.ForeignKey(Appuser, models.DO_NOTHING, db_column='playerid', blank=True, null=True)
    sportname = models.ForeignKey('Sport', models.DO_NOTHING, db_column='sportname', blank=True, null=True)
    starttime = models.TimeField(blank=True, null=True)
    endtime = models.TimeField(blank=True, null=True)
    startdate = models.DateField(blank=True, null=True)
    enddate = models.DateField(blank=True, null=True)
    locationid = models.ForeignKey(Location, models.DO_NOTHING, db_column='locationid', blank=True, null=True)
    status = models.CharField(max_length=30, choices = STATUS_CHOICES, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'singlesrequest'


class SinglesResult(models.Model):
    playerid1 = models.ForeignKey(Appuser, models.DO_NOTHING, db_column='playerid1', blank=True, null=True)
    playerid2 = models.ForeignKey(Appuser, models.DO_NOTHING, db_column='playerid2', blank=True, null=True)
    sportname = models.ForeignKey('Sport', models.DO_NOTHING, db_column='sportname', blank=True, null=True)
    locationid = models.ForeignKey(Location, models.DO_NOTHING, db_column='locationid', blank=True, null=True)
    starttime = models.TimeField(blank=True, null=True)
    endtime = models.TimeField(blank=True, null=True)
    startdate = models.DateField(blank=True, null=True)
    enddate = models.DateField(blank=True, null=True)
    communityratingto1 = models.IntegerField(blank=True, null=True)
    communityratingto2 = models.IntegerField(blank=True, null=True)
    levelto1 = models.CharField(max_length=30, choices = LEVEL_CHOICES, blank=True, null=True)
    levelto2 = models.CharField(max_length=30, choices = LEVEL_CHOICES, blank=True, null=True)
    matchscore = models.CharField(max_length=50, blank=True, null=True)
    victorid = models.ForeignKey(Appuser, models.DO_NOTHING, db_column='victorid', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'singlesresult'


class Sport(models.Model):
    sportname = models.CharField(primary_key=True, max_length=50)
    sporttype = models.CharField(max_length=30, choices = SPORTTYPE_CHOICES)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'sport'


class Team(models.Model):
    teamid = models.AutoField(primary_key=True)
    sportname = models.ForeignKey(Sport, models.DO_NOTHING, db_column='sportname')
    teamname = models.CharField(max_length=30)
    formationdate = models.DateField(blank=True, null=True)
    disbanddate = models.DateField(blank=True, null=True)
    captainid = models.ForeignKey(Appuser, models.DO_NOTHING, db_column='captainid')
    numplayers = models.IntegerField(blank=True, null=True)
    maximumplayers = models.IntegerField(blank=True, null=True)
    communityrating = models.IntegerField(blank=True, null=True)
    ladderscore = models.IntegerField(blank=True, null=True)
    level = models.CharField(max_length=30, choices = LEVEL_CHOICES, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    state = models.CharField(max_length=30, blank=True, null=True)
    country = models.CharField(max_length=30, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'team'


class TeamBlacklist(models.Model):
    teamid1 = models.ForeignKey(Team, models.DO_NOTHING, db_column='teamid1', primary_key=True)
    teamid2 = models.ForeignKey(Team, models.DO_NOTHING, db_column='teamid2')

    class Meta:
        managed = True
        db_table = 'teamblacklist'
        unique_together = (('teamid1', 'teamid2'),)


class TeamChallenge(models.Model):
    teamid1 = models.ForeignKey(Team, models.DO_NOTHING, db_column='teamid1', primary_key=True)
    teamid2 = models.ForeignKey(Team, models.DO_NOTHING, db_column='teamid2')
    starttime = models.TimeField()
    endtime = models.TimeField(blank=True, null=True)
    startdate = models.DateField()
    enddate = models.DateField(blank=True, null=True)
    locationid = models.ForeignKey(Location, models.DO_NOTHING, db_column='locationid')
    status = models.CharField(max_length=30, choices = STATUS_CHOICES, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'teamchallenge'
        unique_together = (('teamid1', 'teamid2', 'starttime', 'startdate', 'locationid'),)


class TeamInvite(models.Model):
    teamrequestid1 = models.ForeignKey('Teamrequest', models.DO_NOTHING, db_column='teamrequestid1', primary_key=True)
    teamrequestid2 = models.ForeignKey('Teamrequest', models.DO_NOTHING, db_column='teamrequestid2')
    status = models.CharField(max_length=30, choices = STATUS_CHOICES, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'teaminvite'
        unique_together = (('teamrequestid1', 'teamrequestid2'),)


class TeamJoiningRequest(models.Model):
    teamid = models.ForeignKey(Team, models.DO_NOTHING, db_column='teamid', blank=True, null=True)
    playerid = models.ForeignKey(Appuser, models.DO_NOTHING, db_column='playerid', blank=True, null=True)
    requesttype = models.CharField(choices = REQUESTTYPE_CHOICES, blank=True, null=True, max_length=30)
    sentdate = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=30, choices = STATUS_CHOICES, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'teamjoiningrequest'


class TeamMatching(models.Model):
    teamrequestid1 = models.ForeignKey('Teamrequest', models.DO_NOTHING, db_column='teamrequestid1', primary_key=True)
    teamrequestid2 = models.ForeignKey('Teamrequest', models.DO_NOTHING, db_column='teamrequestid2')
    starttime = models.TimeField(blank=True, null=True)
    endtime = models.TimeField(blank=True, null=True)
    startdate = models.DateField(blank=True, null=True)
    enddate = models.DateField(blank=True, null=True)
    locationid = models.ForeignKey(Location, models.DO_NOTHING, db_column='locationid', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'teammatching'
        unique_together = (('teamrequestid1', 'teamrequestid2'),)


class TeamPlayerFeedback(models.Model):
    teammatchid = models.ForeignKey('Teamresult', models.DO_NOTHING, db_column='teammatchid', primary_key=True)
    player1 = models.ForeignKey(Appuser, models.DO_NOTHING, db_column='player1')
    player2 = models.ForeignKey(Appuser, models.DO_NOTHING, db_column='player2')
    communityratingto2 = models.IntegerField(blank=True, null=True)
    levelto2 = models.CharField(max_length=30, choices = LEVEL_CHOICES, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'teamplayerfeedback'
        unique_together = (('teammatchid', 'player1', 'player2'),)


class Teamplayers(models.Model):
    teamid = models.ForeignKey(Team, models.DO_NOTHING, db_column='teamid', primary_key=True)
    playerid = models.ForeignKey(Appuser, models.DO_NOTHING, db_column='playerid')
    position = models.CharField(max_length=30, blank=True, null=True)
    startdate = models.DateField(blank=True, null=True)
    enddate = models.DateField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'teamplayers'
        unique_together = (('teamid', 'playerid'),)


class TeamRequest(models.Model):
    teamrequestid = models.AutoField(primary_key=True)
    teamid = models.ForeignKey(Team, models.DO_NOTHING, db_column='teamid', blank=True, null=True)
    starttime = models.TimeField(blank=True, null=True)
    endtime = models.TimeField(blank=True, null=True)
    startdate = models.DateField(blank=True, null=True)
    enddate = models.DateField(blank=True, null=True)
    locationid = models.ForeignKey(Location, models.DO_NOTHING, db_column='locationid', blank=True, null=True)
    status = models.CharField(max_length=30, choices = STATUS_CHOICES, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'teamrequest'


class TeamResult(models.Model):
    teammatchid = models.AutoField(primary_key=True)
    teamid1 = models.ForeignKey(Team, models.DO_NOTHING, db_column='teamid1', blank=True, null=True)
    teamid2 = models.ForeignKey(Team, models.DO_NOTHING, db_column='teamid2', blank=True, null=True)
    locationid = models.ForeignKey(Location, models.DO_NOTHING, db_column='locationid', blank=True, null=True)
    starttime = models.TimeField(blank=True, null=True)
    endtime = models.TimeField(blank=True, null=True)
    startdate = models.DateField(blank=True, null=True)
    enddate = models.DateField(blank=True, null=True)
    communityratingto1 = models.IntegerField(blank=True, null=True)
    communityratingto2 = models.IntegerField(blank=True, null=True)
    levelto1 = models.CharField(max_length=30, choices = LEVEL_CHOICES, blank=True, null=True)
    levelto2 = models.CharField(max_length=30, choices = LEVEL_CHOICES, blank=True, null=True)
    matchscore = models.CharField(max_length=50, blank=True, null=True)
    victorid = models.ForeignKey(Team, models.DO_NOTHING, db_column='victorid', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'teamresult'


class UserBlacklist(models.Model):
    uid1 = models.ForeignKey(Appuser, models.DO_NOTHING, db_column='uid1', primary_key=True)
    uid2 = models.ForeignKey(Appuser, models.DO_NOTHING, db_column='uid2')

    class Meta:
        managed = True
        db_table = 'userblacklist'
        unique_together = (('uid1', 'uid2'),)


class UserSport(models.Model):
    playerid = models.ForeignKey(Appuser, models.DO_NOTHING, db_column='playerid', primary_key=True)
    sportname = models.ForeignKey(Sport, models.DO_NOTHING, db_column='sportname')
    ladderscore = models.IntegerField(blank=True, null=True)
    startingdate = models.CharField(max_length=30, blank=True, null=True)
    level = models.CharField(max_length=30, choices = LEVEL_CHOICES, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'usersport'
        unique_together = (('playerid', 'sportname'),)
