GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other')
)

STATUS_CHOICES = (
    ('Waiting', 'Waiting'),
    ('Accepted', 'Accepted'),
    ('Rejected', 'Rejected'),
    ('Cancelled', 'Cancelled'),
    ('ResultEntered', 'ResultEntered'),
    ('Expired', 'Expired')
)

LEVEL_CHOICES = (
    ('NotPlayed', 'Not Played'),
    ('Beginner', 'Beginner'),
    ('Intermediate', 'Intermediate'),
    ('Advanced', 'Advanced'),
    ('Professional', 'Professional')
)

REQUESTTYPE_CHOICES = (
    ('Joining', 'Joining'),
    ('Recruiting', 'Recruiting')
)

SPORTTYPE_CHOICES = (
    ('Competitive', 'Competitive'),
    ('NonCompetitive', 'NonCompetitive')
)

SCORESTATUS_CHOICES = (
    ('NoneFilled', 'NoneFilled'),
    ('Player1Filled', 'Player1Filled'),
    ('Player2Filled', 'Player2Filled'),
    ('TwoFilled', 'TwoFilled')
)

SPORT_CHOICES = (
    ('Lawn Tennis', 'Lawn Tennis'),
    ('Table Tennis', 'Table Tennis'),
    ('Badminton', 'Badminton'),
    ('Squash', 'Squash'),
    ('Athletics', 'Athletics'),
    ('Cricket', 'Cricket'),
    ('Football', 'Football'),
    ('Hockey', 'Hockey'),
    ('Basketball', 'Basketball'),
    ('Baseball', 'Baseball')
)

EXPERIENCE_CHOICES = (
    ('Below 1 year', 'Below 1 year'),
    ('1-2 years', '1-2 years'),
    ('2-3 years', '2-3 years'),
    ('More than 3 years', 'More than 3 years')
)

LOCATION_NAME = (
    ('No Location', 'No Location'),
)

YESNO_CHOICES = (
    ('Yes', 'Yes'),
    ('No', 'No')
)

BIRTH_YEAR_CHOICES = tuple(i for i in reversed(range(1900, 2010)))

MAX_NUM_PLAYERS_CHOICES = tuple((i,i) for i in range(3, 21))

FILL_SLOT_LEVEL_CHOICES= tuple((i,i) for i in range(1, 11))

FRIEND_CHOICES = (
    ('Accepted', 'Accepted'),
    ('Rejected', 'Rejected'),
    ('Waiting', 'Waiting'),
    ('Cancelled', 'Cancelled')
)