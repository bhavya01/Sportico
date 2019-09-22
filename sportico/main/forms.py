from django import forms
from login.choices import *
from login.models import *

class JQueryUIDatepickerWidget(forms.DateInput):
	def __init__(self, **kwargs):
		super(forms.DateInput, self).__init__(attrs={"size":20, "class": "dateinput", "name":"date", 'placeholder': 'Date'}, **kwargs)

	class Media:
		css = {"all":("http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.6/themes/redmond/jquery-ui.css",)}
		js = ("http://ajax.googleapis.com/ajax/libs/jquery/1.4.3/jquery.min.js",
              "http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.6/jquery-ui.min.js",)

class JQueryUIDatepickerWidget2(forms.DateInput):
	def __init__(self, **kwargs):
		super(forms.DateInput, self).__init__(attrs={"size":20, "class": "dateinput2", "name":"date", 'placeholder': 'Date'}, **kwargs)

	class Media:
		css = {"all":("http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.6/themes/redmond/jquery-ui.css",)}
		js = ("http://ajax.googleapis.com/ajax/libs/jquery/1.4.3/jquery.min.js",
              "http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.6/jquery-ui.min.js",)

class SportForm(forms.Form):
	sportName = forms.ChoiceField(
		label="Sport Name",
        required=True,
        widget=forms.Select,
        choices=SPORT_CHOICES,
    )

	level = forms.ChoiceField(
		label="Level of Proficiency",
        required=True,
        widget=forms.Select,
        choices=LEVEL_CHOICES,
    )

	experience = forms.ChoiceField(
    	label="Experience",
        required=True,
        widget=forms.Select,
        choices=EXPERIENCE_CHOICES,
    )

	def __init__(self, custom_choices=None, *args, **kwargs):
		super(SportForm, self).__init__(*args, **kwargs)
		if custom_choices:
			self.fields['sportName'].choices = custom_choices

class SinglesChallengeForm(forms.Form):
	sportName = forms.ChoiceField(
		label="Sport Name",
        required=True,
        widget=forms.Select,
        choices=(),
    )
    
	playerName = forms.CharField(label="Player Name", max_length=30, 
                               widget=forms.TextInput(attrs={'class': 'form-control', 'playerName': 'Player Name'}))

	locationName = forms.ChoiceField(
		label="Location Name",
        required=True,
        widget=forms.Select,
        choices=(),
	)

	startTime = forms.TimeField(label="From", widget=forms.TimeInput(attrs={'placeholder': 'Time'}, format='%H:%M'))

	startDate = forms.DateField(widget=JQueryUIDatepickerWidget)

	endTime = forms.TimeField(label="Till", widget=forms.TimeInput(attrs={'placeholder': 'Time'}, format='%H:%M'))

	endDate = forms.DateField(widget=JQueryUIDatepickerWidget)

	def __init__(self, customChoicesLocation=None, customChoicesSport=None,*args, **kwargs):
		super(SinglesChallengeForm, self).__init__(*args, **kwargs)
		if customChoicesLocation:
			self.fields['locationName'].choices = customChoicesLocation
		if customChoicesSport:
			self.fields['sportName'].choices = customChoicesSport

	def clean_playerName(self):
		playerName = self.cleaned_data['playerName']
		print("In clean function")
		print(User.objects.get(username=playerName).count())
		if not User.objects.get(username=playerName).count() == 1:
			raise forms.ValidationError("The user does not exist")
		return playerName

class SinglesFillSlotForm(forms.Form):
	sportName = forms.ChoiceField(
		label="Sport Name",
        required=True,
        widget=forms.Select,
        choices=(),
    )

	locationName = forms.ChoiceField(
		label="Location Name",
        required=True,
        widget=forms.Select,
        choices=(),
	)
	startTime = forms.TimeField(label="From", widget=forms.TimeInput(attrs={'placeholder': 'Time'}, format='%H:%M'))

	startDate2 = forms.DateField(widget=JQueryUIDatepickerWidget2)

	endTime = forms.TimeField(label="Till", widget=forms.TimeInput(attrs={'placeholder': 'Time'}, format='%H:%M'))

	endDate2 = forms.DateField(widget=JQueryUIDatepickerWidget2)

	levelBase = forms.IntegerField(label="Opponent Level", widget=forms.NumberInput(attrs={'placeholder': 'Min level', 'min': 1, 'max': 10}))
	levelTop = forms.IntegerField(label="Opponent Level", widget=forms.NumberInput(attrs={'placeholder': 'Max level', 'min': 1, 'max': 10}))

	def __init__(self, customChoicesSport=None,*args, **kwargs):
		super(SinglesFillSlotForm, self).__init__(*args, **kwargs)
		if customChoicesSport:
			self.fields['sportName'].choices = customChoicesSport

class doublesTeamForm(forms.Form):	
	sportName = forms.ChoiceField(
		label="Sport Name",
        required=True,
        widget=forms.Select,
        choices=(),
    )
    
	playerName = forms.CharField(label="Player Name", max_length=30, required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name' :'playerName', 'placeholder': 'Player Name'}))

	teamName = forms.CharField(label="Team Name", max_length=50, required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name' :'teamName', 'placeholder': 'Team Name'}))

	captain = forms.ChoiceField(label="Would you offer him the captaincy role?", choices=YESNO_CHOICES, widget=forms.RadioSelect(), required=True)

	def __init__(self, customChoicesSport = None, *args, **kwargs):
		super(doublesTeamForm, self).__init__(*args, **kwargs)
		if customChoicesSport:
			self.fields['sportName'].choices = customChoicesSport

class addTeamForm(forms.Form):	
	sportName = forms.ChoiceField(
		label="Sport Name",
        required=True,
        widget=forms.Select,
        choices=(),
    )
	teamName = forms.CharField(label="Name", max_length=30, required = True,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'teamName', 'placeholder': 'Team Name'}))
	maxPlayers = forms.ChoiceField(
		label="Maximum number of Players",
        required=True,
        widget=forms.Select,
        choices=MAX_NUM_PLAYERS_CHOICES,
    )
	city = forms.CharField(label="Location", max_length=30, required = False,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'city', 'placeholder': 'City'}))
	state = forms.CharField(label="Location", max_length=30, required = False,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'state', 'placeholder': 'State'}))
	country = forms.CharField(label="Location", max_length=30, required = False,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'country', 'placeholder': 'Country'}))
	
	def __init__(self, customChoicesSport = None, *args, **kwargs):
		super(addTeamForm, self).__init__(*args, **kwargs)
		if customChoicesSport:
			self.fields['sportName'].choices = customChoicesSport

class addPlayerForm(forms.Form):	
	teamName = forms.ChoiceField(
		label="Team Name",
        required=True,
        widget=forms.Select,
        choices=(),
    )
	playerName = forms.CharField(label="Player Name", max_length=30, 
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'playerName', 'placeholder': 'Player Name'}))
	position = forms.CharField(label="Position", max_length=30, required = False,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'position', 'placeholder': 'Playing Position'}))


	
	def __init__(self, userTeams = None, *args, **kwargs):
		super(addPlayerForm, self).__init__(*args, **kwargs)

		if userTeams:
			self.fields['teamName'].choices = userTeams

class sendRequestTeamForm(forms.Form):	
	sportName = forms.ChoiceField(
		label="Sport Name",
        required=True,
        widget=forms.Select,
        choices=(),
    )
	teamName = forms.CharField(label="Team Name", max_length=30, 
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'teamName', 'placeholder': 'Team Name'}))
	captainName = forms.ChoiceField(
		label="Captain Name",
        required=True,
        widget=forms.Select,
        choices=(),
    )
    
	position = forms.CharField(label="Position", max_length=30, required = False,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'position', 'placeholder': 'Playing Position'}))


	
	def __init__(self, userSports = None, *args, **kwargs):
		super(sendRequestTeamForm, self).__init__(*args, **kwargs)

		if userSports:
			self.fields['sportName'].choices = userSports

class DoublesChallengeForm(forms.Form):
	sportName = forms.ChoiceField(
		label="Sport Name",
        required=True,
        widget=forms.Select,
        choices=(),
    )

	teamNameUser = forms.ChoiceField(
		label="Your Team Name",
        required=True,
        widget=forms.Select,
        choices=(),
    )
    
	teamNameOpponent = forms.CharField(label="Opponent Team Name", max_length=30, 
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'teamName', 'placeholder': 'Team Name'}))

	captainName = forms.ChoiceField(
		label="Captain Name",
        required=True,
        widget=forms.Select,
        choices=(),
    )

	locationName = forms.ChoiceField(
		label="Location Name",
        required=True,
        widget=forms.Select,
        choices=(),
	)

	startTime = forms.TimeField(label="From", widget=forms.TimeInput(attrs={'placeholder': 'Time'}, format='%H:%M'))

	startDate = forms.DateField(widget=JQueryUIDatepickerWidget)

	endTime = forms.TimeField(label="Till", widget=forms.TimeInput(attrs={'placeholder': 'Time'}, format='%H:%M'))

	endDate = forms.DateField(widget=JQueryUIDatepickerWidget)

	def __init__(self, customChoicesLocation=None, customChoicesSport=None,*args, **kwargs):
		super(DoublesChallengeForm, self).__init__(*args, **kwargs)
		if customChoicesLocation:
			self.fields['locationName'].choices = customChoicesLocation
		if customChoicesSport:
			self.fields['sportName'].choices = customChoicesSport


class DoublesFillSlotForm(forms.Form):
	sportName = forms.ChoiceField(
		label="Sport Name",
        required=True,
        widget=forms.Select,
        choices=(),
    )

	teamNameUser = forms.ChoiceField(
		label="Your Team Name",
        required=True,
        widget=forms.Select,
        choices=(),
    )

	locationName = forms.ChoiceField(
		label="Location Name",
        required=True,
        widget=forms.Select,
        choices=(),
	)
	startTime = forms.TimeField(label="From", widget=forms.TimeInput(attrs={'placeholder': 'Time'}, format='%H:%M'))

	startDate2 = forms.DateField(widget=JQueryUIDatepickerWidget2)

	endTime = forms.TimeField(label="Till", widget=forms.TimeInput(attrs={'placeholder': 'Time'}, format='%H:%M'))

	endDate2 = forms.DateField(widget=JQueryUIDatepickerWidget2)

	levelBase = forms.IntegerField(label="Opponent Level", widget=forms.NumberInput(attrs={'placeholder': 'Min level', 'min': 1, 'max': 10}))
	levelTop = forms.IntegerField(label="Opponent Level", widget=forms.NumberInput(attrs={'placeholder': 'Max level', 'min': 1, 'max': 10}))

	def __init__(self, customChoicesSport=None,*args, **kwargs):
		super(DoublesFillSlotForm, self).__init__(*args, **kwargs)
		if customChoicesSport:
			self.fields['sportName'].choices = customChoicesSport

class TeamChallengeForm(forms.Form):
	sportName = forms.ChoiceField(
		label="Sport Name",
        required=True,
        widget=forms.Select,
        choices=(),
    )

	teamNameUser = forms.ChoiceField(
		label="Your Team Name",
        required=True,
        widget=forms.Select,
        choices=(),
    )
    
	teamNameOpponent = forms.CharField(label="Opponent Team Name", max_length=30, 
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'teamName', 'placeholder': 'Team Name'}))

	captainName = forms.ChoiceField(
		label="Captain Name",
        required=True,
        widget=forms.Select,
        choices=(),
    )
    
	locationName = forms.ChoiceField(
		label="Location Name",
        required=True,
        widget=forms.Select,
        choices=(),
	)

	startTime = forms.TimeField(label="From", widget=forms.TimeInput(attrs={'placeholder': 'Time'}, format='%H:%M'))

	startDate = forms.DateField(widget=JQueryUIDatepickerWidget)

	endTime = forms.TimeField(label="Till", widget=forms.TimeInput(attrs={'placeholder': 'Time'}, format='%H:%M'))

	endDate = forms.DateField(widget=JQueryUIDatepickerWidget)

	def __init__(self, customChoicesLocation=None, customChoicesSport=None,*args, **kwargs):
		super(TeamChallengeForm, self).__init__(*args, **kwargs)
		if customChoicesLocation:
			self.fields['locationName'].choices = customChoicesLocation
		if customChoicesSport:
			self.fields['sportName'].choices = customChoicesSport


class TeamFillSlotForm(forms.Form):
	sportName = forms.ChoiceField(
		label="Sport Name",
        required=True,
        widget=forms.Select,
        choices=()
    )

	teamNameUser = forms.ChoiceField(
		label="Your Team Name",
        required=True,
        widget=forms.Select,
        choices=(),
    )

	locationName = forms.ChoiceField(
		label="Location Name",
        required=True,
        widget=forms.Select,
        choices=(),
	)
	startTime = forms.TimeField(label="From", widget=forms.TimeInput(attrs={'placeholder': 'Time'}, format='%H:%M'))

	startDate2 = forms.DateField(widget=JQueryUIDatepickerWidget2)

	endTime = forms.TimeField(label="Till", widget=forms.TimeInput(attrs={'placeholder': 'Time'}, format='%H:%M'))

	endDate2 = forms.DateField(widget=JQueryUIDatepickerWidget2)

	levelBase = forms.IntegerField(label="Opponent Level", widget=forms.NumberInput(attrs={'placeholder': 'Min level', 'min': 1, 'max': 10}))
	levelTop = forms.IntegerField(label="Opponent Level", widget=forms.NumberInput(attrs={'placeholder': 'Max level', 'min': 1, 'max': 10}))

	def __init__(self, customChoicesSport=None,*args, **kwargs):
		super(TeamFillSlotForm, self).__init__(*args, **kwargs)
		if customChoicesSport:
			self.fields['sportName'].choices = customChoicesSport

class singlesResultForm(forms.Form):
	resultId = forms.IntegerField()

	username = forms.CharField(label="Username", max_length=30, 
                               widget=forms.TextInput(attrs={'class': 'form-control'}))

	playerName = forms.CharField(label="Player 2", max_length=30, 
                               widget=forms.TextInput(attrs={'class': 'form-control'}))

	sportName = forms.CharField(label="SportName", max_length=30, 
                               widget=forms.TextInput(attrs={'class': 'form-control'}))

	locationId = forms.CharField(label="Location", max_length=30, 
                               widget=forms.TextInput(attrs={'class': 'form-control'}))

	startTime = forms.TimeField(label="From", widget=forms.TimeInput(attrs={'placeholder': 'Time'}, format='%H:%M'))

	startDate = forms.DateField(widget=JQueryUIDatepickerWidget)

	endTime = forms.TimeField(label="Till", widget=forms.TimeInput(attrs={'placeholder': 'Time'}, format='%H:%M'))

	endDate = forms.DateField(widget=JQueryUIDatepickerWidget)

	communityRating = forms.IntegerField(label="Community Rating", widget=forms.NumberInput(attrs={'placeholder': 'Scale of 1-10', 'min': 1, 'max': 10}))

	level = forms.IntegerField(label="Proficiency Level", widget=forms.NumberInput(attrs={'placeholder': 'Scale of 1-5', 'min': 1, 'max': 5}))

	matchScore = forms.CharField(label="Match Score", max_length=30, 
                               widget=forms.TextInput(attrs={'placeholder': 'Match Score', 'class': 'form-control'}))

	winner = forms.ChoiceField(label="Did you Win?", choices=YESNO_CHOICES, widget=forms.RadioSelect(attrs={'class': 'inline'}))

class resultForm(forms.Form):
	resultId = forms.IntegerField()

	userTeamName = forms.CharField(label="UserTeamName", max_length=50, 
                               widget=forms.TextInput(attrs={'class': 'form-control'}))

	teamName = forms.CharField(label="Team Name", max_length=50, 
                               widget=forms.TextInput(attrs={'class': 'form-control'}))

	sportName = forms.CharField(label="SportName", max_length=30, 
                               widget=forms.TextInput(attrs={'class': 'form-control'}))

	locationId = forms.CharField(label="Location", max_length=30, 
                               widget=forms.TextInput(attrs={'class': 'form-control'}))

	startTime = forms.TimeField(label="From", widget=forms.TimeInput(attrs={'placeholder': 'Time'}, format='%H:%M'))

	startDate = forms.DateField(widget=JQueryUIDatepickerWidget)

	endTime = forms.TimeField(label="Till", widget=forms.TimeInput(attrs={'placeholder': 'Time'}, format='%H:%M'))

	endDate = forms.DateField(widget=JQueryUIDatepickerWidget)

	communityRating = forms.IntegerField(label="Community Rating", widget=forms.NumberInput(attrs={'placeholder': 'Scale of 1-10', 'min': 1, 'max': 10}))

	level = forms.IntegerField(label="Proficiency Level", widget=forms.NumberInput(attrs={'placeholder': 'Scale of 1-5', 'min': 1, 'max': 5}))

	matchScore = forms.CharField(label="Match Score", max_length=30, 
                               widget=forms.TextInput(attrs={'placeholder': 'Match Score', 'class': 'form-control'}))

	winner = forms.ChoiceField(label="Did you Win?", choices=YESNO_CHOICES, widget=forms.RadioSelect(attrs={'class': 'inline'}))

class EventForm(forms.Form):
	sportName = forms.ChoiceField(
		label="Sport Name",
        required=True,
        widget=forms.Select,
        choices=(),
    )
    
	locationName = forms.ChoiceField(
		label="Location Name",
        required=True,
        widget=forms.Select,
        choices=(),
	)

	description = forms.CharField(label="Description", max_length=255, 
                               widget=forms.Textarea(attrs={'class': 'form-control', 'rows':4, 'cols':40}))

	maxParticipants = forms.IntegerField()

	startTime = forms.TimeField(label="From", widget=forms.TimeInput(attrs={'placeholder': 'Time'}, format='%H:%M'))

	startDate = forms.DateField(widget=JQueryUIDatepickerWidget)

	endTime = forms.TimeField(label="Till", widget=forms.TimeInput(attrs={'placeholder': 'Time'}, format='%H:%M'))

	endDate = forms.DateField(widget=JQueryUIDatepickerWidget)

	def __init__(self, customChoicesLocation=None, customChoicesSport=None,*args, **kwargs):
		super(EventForm, self).__init__(*args, **kwargs)
		if customChoicesSport:
			self.fields['sportName'].choices = customChoicesSport

		if customChoicesLocation:
			self.fields['locationName'].choices = customChoicesLocation


class UploadImageForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()