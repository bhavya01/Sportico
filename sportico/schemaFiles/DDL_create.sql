create sequence if not exists doublesId start 1;
create sequence if not exists teamId start 1;
create sequence if not exists singlesRequestId start 1;
create sequence if not exists doublesRequestId start 1;
create sequence if not exists teamRequestId start 1;
create sequence if not exists locationId start 1;
create sequence if not exists nonCompetitiveId start 1;
create sequence if not exists doublesMatchId start 1;
create sequence if not exists teamMatchId start 1;
create sequence if not exists eventId start 1;

CREATE TYPE gender AS ENUM ('Male', 'Female', 'Other');
CREATE TYPE status AS ENUM ('Waiting', 'Accepted', 'Rejected', 'Cancelled', 'Expired');
CREATE TYPE level AS ENUM ('NotPlayed', 'Beginner', 'Intermediate', 'Advanced', 'Professional');
CREATE TYPE requestType AS ENUM ('Joining', 'Recruiting');
CREATE TYPE sportType AS ENUM ('Competitive', 'NonCompetitive');

CREATE TABLE appUser(			-- done
	uid			 	VARCHAR(30),
	firstName		VARCHAR(30) not null,
	lastName 		VARCHAR(30),
	nickName 		VARCHAR(30),
	birthDate 		date,
	profilePicture 	bytea, 
	gender 			gender, 
	street 			VARCHAR(30),
	city			VARCHAR(30),
	state 			VARCHAR(30),
	country 		VARCHAR(30),
	email 			VARCHAR(50),
	communityRating int,
	phoneNumber 	VARCHAR(30) not null,
	appJoinDate 	date not null,		
	PRIMARY KEY (uid)
);

CREATE TABLE password(		-- Done
	uid			VARCHAR(30),
	password	VARCHAR(30) not null,
	PRIMARY KEY (uid),
	FOREIGN KEY (uid) REFERENCES appUser(uid)
		ON DELETE CASCADE
);

CREATE TABLE doubles(		-- Done
	doublesId 	int primary key default nextval('doublesId'),
	player1 	VARCHAR(30),
	player2 	VARCHAR(30),
	FOREIGN KEY (player1) REFERENCES appUser(uid)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	FOREIGN KEY (player2) REFERENCES appUser(uid)
		ON DELETE CASCADE
		ON UPDATE CASCADE
);

CREATE TABLE sport(
	sportName 			VARCHAR(50) not null,	-- Done
	sportType 			sportType not null, 
	description			VARCHAR(255),
	PRIMARY KEY (sportName)
);

CREATE TABLE doublesFormationRequest(		-- DOne
	senderId 	VARCHAR(30),
	receiverId 	VARCHAR(30),
	captainId 	VARCHAR(30),
	sportName 	VARCHAR(50),	
	sentTime 	TIMESTAMP, 
	status 		status,
	FOREIGN KEY (senderId) REFERENCES appUser(uid)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	FOREIGN KEY (receiverId) REFERENCES appUser(uid)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	FOREIGN KEY (captainId) REFERENCES appUser(uid)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	FOREIGN KEY (sportName) REFERENCES sport(sportName)
		ON DELETE CASCADE
		ON UPDATE CASCADE
);

CREATE TABLE team(		-- Not done captain Id and sport to form -- Done	
						-- temp relationship		-- Done
	teamId			int primary key default nextval('teamId'),
	sportName 		VARCHAR(50) not null,
	teamName 		VARCHAR(30) not null,
	formationDate 	date, 
	disbandDate		date, 
	captainId		VARCHAR(30) not null,
	numPlayers 		int, 	 
	maximumPlayers	int,
	communityRating int, 
	ladderScore 	int,
	level 			level not null,   
	city 			VARCHAR(30),
	state 			VARCHAR(30),
	country 		VARCHAR(30),
	description		VARCHAR(255), 
	FOREIGN KEY (sportName) REFERENCES sport(sportName)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	FOREIGN KEY (captainId) REFERENCES appUser(uid)
		ON DELETE CASCADE
		ON UPDATE CASCADE
);

CREATE TABLE userBlacklist(		--Done
	uid1		VARCHAR(30),
	uid2 		VARCHAR(30),
	PRIMARY KEY (uid1, uid2),
	FOREIGN KEY (uid1) REFERENCES appUser(uid)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	FOREIGN KEY (uid2) REFERENCES appUser(uid)
		ON DELETE CASCADE
		ON UPDATE CASCADE
);

CREATE TABLE doublesBlacklist(		-- Done
	doublesId1 	int, 
	doublesId2  int,
	PRIMARY KEY (doublesId1, doublesId2),
	FOREIGN KEY (doublesId1) REFERENCES doubles(doublesId)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	FOREIGN KEY (doublesId2) REFERENCES doubles(doublesId)
		ON DELETE CASCADE
		ON UPDATE CASCADE 
);

CREATE TABLE teamBlacklist(			-- Done
	teamId1 int, 
	teamId2 int,
	PRIMARY KEY (teamId1, teamId2),
	FOREIGN KEY (teamId1) REFERENCES team(teamId)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	FOREIGN KEY (teamId2) REFERENCES team(teamId)
		ON DELETE CASCADE
		ON UPDATE CASCADE 
);

CREATE TABLE userSport(			-- Done
	playerId 		VARCHAR(30),
	sportName 		VARCHAR(50),
	ladderScore 	int, 
	startingDate	VARCHAR(30),
	level 			level,
	PRIMARY KEY (playerId, sportName), 
	FOREIGN KEY (playerId) REFERENCES appUser(uid)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	FOREIGN KEY (sportName) REFERENCES sport(sportName)
		ON DELETE CASCADE
		ON UPDATE CASCADE
);

CREATE TABLE doublesSport(		-- Done
	doublesId 		int, 
	sportName 		VARCHAR(50), 
	teamName		VARCHAR(50), 
	captainnId		VARCHAR(30),	-- **** if we are keeping captain 
									--		over here so shouldn't we make a foreign key 
									--		refernecing user for the captain
	ladderScore		int, 
	formationDate 	date, 
	disbandDate		date, 
	level 			level,
	PRIMARY KEY (doublesId, sportName), 
	FOREIGN KEY (doublesId) REFERENCES doubles(doublesId)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	FOREIGN KEY (sportName) REFERENCES sport(sportName)
		ON DELETE CASCADE
		ON UPDATE CASCADE
);

CREATE TABLE teamJoiningRequest (		-- Done
	teamId 		int, 
	playerId 	VARCHAR(30),
	requestType requestType, 
	sentDate 	date, 
	status 		status,
	FOREIGN KEY (teamId) REFERENCES team(teamId)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	FOREIGN KEY (playerId) REFERENCES appUser(uid)
		ON DELETE CASCADE
		ON UPDATE CASCADE
);

CREATE TABLE teamPlayers (			-- Done
	teamId 		int, 
	playerId 	VARCHAR(30),
	position 	VARCHAR(30),
	startDate 	date, 
	endDate     	date,
	PRIMARY KEY (teamId, playerId),  
	FOREIGN KEY (teamId) REFERENCES team(teamId)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	FOREIGN KEY (playerId) REFERENCES appUser(uid)
		ON DELETE CASCADE
		ON UPDATE CASCADE
);

CREATE TABLE location (			-- Done
	locationId			int primary key default nextval('locationId'), 
	locationName 		VARCHAR(30) not null,  
	street 				VARCHAR(30), 
	city 				VARCHAR(30) not null, 
	state 				VARCHAR(30) not null, 
	country 			VARCHAR(30) not null, 
	description			VARCHAR(30) 
);

CREATE TABLE singlesRequest (		-- Done
	singlesRequestId	int primary key default nextval('singlesRequestId'),
	playerId 			VARCHAR(30), 
	sportName 			VARCHAR(50), 
	startTime 			time, 
	endTime 			time, 
	startDate 			date, 
	endDate 			date, 
	locationId			int, 
	status 				status, 
	FOREIGN KEY (playerId) REFERENCES appUser(uid)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	FOREIGN KEY (sportName) REFERENCES sport(sportName)
		ON DELETE CASCADE
		ON UPDATE CASCADE, 
	FOREIGN KEY (locationId) REFERENCES location(locationId)
		ON DELETE CASCADE
		ON UPDATE CASCADE
);

CREATE TABLE nonCompetitiveMatching (		-- ? sport which is going to cater ??
											-- Sport ?? not there but I am still adding 

	-- ****************** Done **********************


	nonCompetitiveId 	int primary key default nextval('nonCompetitiveId'),
	startTime			time, 
	endTime 			time, 
	startDate 			date, 
	endDate 			date, 
	locationId 			int,
	sportName			VARCHAR(50),
	FOREIGN KEY (locationId) REFERENCES location(locationId)
		ON DELETE CASCADE
		ON UPDATE CASCADE,  
	FOREIGN KEY (sportName) REFERENCES sport(sportName)
		ON DELETE CASCADE
		ON UPDATE CASCADE  	
);

CREATE TABLE nonCompetitiveMatchingParticipant (		-- Done
	nonCompetitiveId	int, 
	singlesRequestId    int, 
	status				status,
	PRIMARY KEY (nonCompetitiveId, singlesRequestId), 
	FOREIGN KEY (nonCompetitiveId) REFERENCES nonCompetitiveMatching(nonCompetitiveId)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	FOREIGN KEY (singlesRequestId) REFERENCES singlesRequest(singlesRequestId)
		ON DELETE CASCADE
		ON UPDATE CASCADE   
);

CREATE TABLE nonCompetitiveMatchingFeedback(		-- Done
	nonCompetitiveId 	int, 
	playerId1 			VARCHAR(30), 
	playerId2 			VARCHAR(30), 
	communityRating 	int, 
	level 				level,
	PRIMARY KEY (nonCompetitiveId, playerId1, playerId2), 
	FOREIGN KEY (nonCompetitiveId) REFERENCES nonCompetitiveMatching(nonCompetitiveId)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	FOREIGN KEY (playerId1) REFERENCES appUser(uid)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	FOREIGN KEY (playerId2) REFERENCES appUser(uid)
		ON DELETE CASCADE
		ON UPDATE CASCADE
);

CREATE TABLE singlesMatching (		-- Done
	singlesRequestId1	 	int, 
	singlesRequestId2		int, 
	startTime 				time, 
	endTime 				time, 
	startDate 				date, 
	endDate 				date, 
	locationId 				int,
	PRIMARY KEY (singlesRequestId1, singlesRequestId2),
	FOREIGN KEY (singlesRequestId1) REFERENCES singlesRequest(singlesRequestId)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	FOREIGN KEY (singlesRequestId2) REFERENCES singlesRequest(singlesRequestId)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	FOREIGN KEY (locationId) REFERENCES location(locationId)
		ON DELETE CASCADE
		ON UPDATE CASCADE	  
);

CREATE TABLE doublesRequest (		--Done
	doublesRequestId	int primary key default nextval('doublesRequestId'),
	doublesId 			int, 
	sportName 			VARCHAR(50), 
	startTime 			time, 
	endTime 			time, 
	startDate 			date, 
	endDate 			date, 
	locationId			int, 
	status 				status, 
	FOREIGN KEY (doublesId) REFERENCES doubles(doublesId)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	FOREIGN KEY (sportName) REFERENCES sport(sportName)
		ON DELETE CASCADE
		ON UPDATE CASCADE, 
	FOREIGN KEY (locationId) REFERENCES location(locationId)
		ON DELETE CASCADE
		ON UPDATE CASCADE
);

CREATE TABLE doublesMatching (		-- Done
	doublesRequestId1	 	int, 
	doublesRequestId2		int, 
	startTime 				time, 
	endTime 				time, 
	startDate 				date, 
	endDate 				date, 
	locationId 				int,
	PRIMARY KEY (doublesRequestId1, doublesRequestId2),
	FOREIGN KEY (doublesRequestId1) REFERENCES doublesRequest(doublesRequestId)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	FOREIGN KEY (doublesRequestId2) REFERENCES doublesRequest(doublesRequestId)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	FOREIGN KEY (locationId) REFERENCES location(locationId)
		ON DELETE CASCADE
		ON UPDATE CASCADE
);

CREATE TABLE teamRequest(		-- Done
	teamRequestId 		int primary key default nextval('teamRequestId'), 
	teamId 				int, 
	startTime 			time, 
	endTime 			time, 
	startDate 			date, 
	endDate 			date, 
	locationId 			int, 
	status 				status, 
	FOREIGN KEY (teamId) REFERENCES team(teamId)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	FOREIGN KEY (locationId) REFERENCES location(locationId)
		ON DELETE CASCADE
		ON UPDATE CASCADE
);

CREATE TABLE teamMatching (		-- Done
	teamRequestId1	 		int, 
	teamRequestId2			int, 
	startTime 				time, 
	endTime 				time, 
	startDate 				date, 
	endDate 				date, 
	locationId 				int,
	PRIMARY KEY (teamRequestId1, teamRequestId2),
	FOREIGN KEY (teamRequestId1) REFERENCES teamRequest(teamRequestId)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	FOREIGN KEY (teamRequestId2) REFERENCES teamRequest(teamRequestId)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	FOREIGN KEY (locationId) REFERENCES location(locationId)
		ON DELETE CASCADE
		ON UPDATE CASCADE
);

CREATE TABLE singlesInvite (		-- Done
	singlesRequestId1	 	int, 
	singlesRequestId2		int, 	
	status 					status,
	PRIMARY KEY (singlesRequestId1, singlesRequestId2), 
	FOREIGN KEY (singlesRequestId1) REFERENCES singlesRequest(singlesRequestId)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	FOREIGN KEY (singlesRequestId2) REFERENCES singlesRequest(singlesRequestId)
		ON DELETE CASCADE
		ON UPDATE CASCADE
);

CREATE TABLE doublesInvite (		--Done
	doublesRequestId1	 	int, 
	doublesRequestId2		int,
	status 					status,
	PRIMARY KEY (doublesRequestId1, doublesRequestId2), 
	FOREIGN KEY (doublesRequestId1) REFERENCES doublesRequest(doublesRequestId)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	FOREIGN KEY (doublesRequestId2) REFERENCES doublesRequest(doublesRequestId)
		ON DELETE CASCADE
		ON UPDATE CASCADE
);

CREATE TABLE teamInvite (		-- Done
	teamRequestId1	 		int, 
	teamRequestId2			int,
	status 					status,
	PRIMARY KEY (teamRequestId1, teamRequestId2),  
	FOREIGN KEY (teamRequestId1) REFERENCES teamRequest(teamRequestId)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	FOREIGN KEY (teamRequestId2) REFERENCES teamRequest(teamRequestId)
		ON DELETE CASCADE
		ON UPDATE CASCADE 
);

CREATE TABLE singlesChallenge (			-- I was not sure how to represent primary key constraint in relationship
	playerId1 			VARCHAR(30), 	-- This still loks somewhat fishy I think apart from status all of them should be there in the promary key?	
	playerId2 			VARCHAR(30), 	-- Done
	sportName 			VARCHAR(50), 
	startTime 			time, 
	endTime 			time, 
	startDate 			date, 
	endDate 			date, 
	locationId 			int, 
	status 				status, 
	PRIMARY KEY (playerId1,playerId2,sportName,startTime,startDate,locationId),
	FOREIGN KEY (playerId1) REFERENCES appUser(uid)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	FOREIGN KEY (playerId2) REFERENCES appUser(uid)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	FOREIGN KEY (sportName) REFERENCES sport(sportName)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	FOREIGN KEY (locationId) REFERENCES location(locationId)
		ON DELETE CASCADE
		ON UPDATE CASCADE  
);

CREATE TABLE doublesChallenge (		--Done
	doublesId1 			int, 		
	doublesId2 			int, 
	sportName 			VARCHAR(50), 
	startTime 			time, 
	endTime 			time, 
	startDate 			date, 
	endDate 			date, 
	locationId 			int, 
	status				status, 
	PRIMARY KEY (doublesId1,doublesId2,sportName,startTime,startDate,locationId),
	FOREIGN KEY (doublesId1) REFERENCES doubles(doublesId)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	FOREIGN KEY (doublesId2) REFERENCES doubles(doublesId)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	FOREIGN KEY (sportName) REFERENCES sport(sportName)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	FOREIGN KEY (locationId) REFERENCES location(locationId)
		ON DELETE CASCADE
		ON UPDATE CASCADE    
);

CREATE TABLE teamChallenge (	-- Done
	teamId1 		int, 
	teamId2 		int, 
	startTime 		time, 
	endTime 		time, 
	startDate 		date, 
	endDate 		date, 
	locationId 		int, 
	status 			status,
	PRIMARY KEY (teamId1,teamId2,startTime,startDate,locationId),
	FOREIGN KEY (teamId1) REFERENCES team(teamId)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	FOREIGN KEY (teamId2) REFERENCES team(teamId)
		ON DELETE CASCADE
		ON UPDATE CASCADE, 
	FOREIGN KEY (locationId) REFERENCES location(locationId)
		ON DELETE CASCADE
		ON UPDATE CASCADE  
);

CREATE TABLE singlesResult (
	playerId1 			VARCHAR(30), 
	playerId2			VARCHAR(30), 
	sportName 			VARCHAR(50), 
	locationId 			int, 
	startTime 			time, 	
	endTime 			time, 
	startDate 			date, 
	endDate 			date, 
	communityRatingTo1	int, 
	communityRatingTo2	int, 
	levelto1 			level, 
	levelto2 			level, 
	matchScore 			VARCHAR(50), 
	victorId			VARCHAR(30), 
	FOREIGN KEY (playerId1) REFERENCES appUser(uid)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	FOREIGN KEY (playerId2) REFERENCES appUser(uid)
		ON DELETE CASCADE
		ON UPDATE CASCADE, 
	FOREIGN KEY (sportName) REFERENCES sport(sportName)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	FOREIGN KEY (locationId) REFERENCES location(locationId)
		ON DELETE CASCADE
		ON UPDATE CASCADE, 
	FOREIGN KEY (victorId) REFERENCES appUser(uid)
		ON DELETE CASCADE
		ON UPDATE CASCADE
);

CREATE TABLE doublesResult (
	doublesMatchId  	int primary key default nextval('doublesMatchId'),
	doublesId1 			int, 
	doublesId2 			int, 
	sportName 			VARCHAR(50), 
	locationId 			int, 
	startTime 			time, 
	endTime 			time, 
	startDate 			date, 
	endDate 			date, 
	communityRatingTo1	int, 
	communityRatingTo2	int, 
	levelTo1 			level, 
	levelTo2 			level, 
	matchScore 			VARCHAR(50),
	victorId			int, 
	FOREIGN KEY (doublesId1) REFERENCES doubles(doublesId)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	FOREIGN KEY (doublesId2) REFERENCES doubles(doublesId)
		ON DELETE CASCADE
		ON UPDATE CASCADE, 
	FOREIGN KEY (sportName) REFERENCES sport(sportName)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	FOREIGN KEY (locationId) REFERENCES location(locationId)
		ON DELETE CASCADE
		ON UPDATE CASCADE, 
	FOREIGN KEY (victorId) REFERENCES doubles(doublesId)
		ON DELETE CASCADE
		ON UPDATE CASCADE  
);

CREATE TABLE doublesFeedback (
	doublesMatchId 		int, 
	playerId1 			VARCHAR(30), 
	playerId2 			VARCHAR(30) 	, 
	communityRatingTo2 	int,
	PRIMARY KEY (doublesMatchId, playerId1, playerId2),
	FOREIGN KEY (doublesMatchId) REFERENCES doublesResult(doublesMatchId)
		ON DELETE CASCADE
		ON UPDATE CASCADE, 
	FOREIGN KEY (playerId1) REFERENCES appUser(uid)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	FOREIGN KEY (playerId2) REFERENCES appUser(uid)
		ON DELETE CASCADE
		ON UPDATE CASCADE	
);

CREATE TABLE teamResult (
	teamMatchId 		int primary key default nextval('teamMatchId'),
	teamId1 			int, 
	teamId2 			int, 
	locationId 			int, 
	startTime 			time, 
	endTime 			time, 
	startDate 			date, 
	endDate 			date, 
	communityRatingTo1	int, 
	communityRatingTo2 	int, 
	levelTo1 			level, 
	levelTo2 			level, 
	matchScore			VARCHAR(50), 
	victorId 			int, 
	FOREIGN KEY (teamId1) REFERENCES team(teamId)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	FOREIGN KEY (teamId2) REFERENCES team(teamId)
		ON DELETE CASCADE
		ON UPDATE CASCADE, 
	FOREIGN KEY (locationId) REFERENCES location(locationId)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	FOREIGN KEY (victorId) REFERENCES team(teamId)
		ON DELETE CASCADE
		ON UPDATE CASCADE 
);

CREATE TABLE teamPlayerFeedback (
	teamMatchId			int, 
	player1 			VARCHAR(30), 
	player2 			VARCHAR(30), 
	communityRatingTo2  int,
	levelTo2 			level,
	PRIMARY KEY (teamMatchId, player1, player2), 
	FOREIGN KEY (teamMatchId) REFERENCES teamResult(teamMatchId)
		ON DELETE CASCADE
		ON UPDATE CASCADE, 
	FOREIGN KEY (player1) REFERENCES appUser(uid)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	FOREIGN KEY (player2) REFERENCES appUser(uid)
		ON DELETE CASCADE
		ON UPDATE CASCADE 
);

CREATE TABLE locationSport (
	locationId 		int, 
	sportName 		VARCHAR(50), 
	description 	VARCHAR(255),
	PRIMARY KEY (locationId, sportName), 
	FOREIGN KEY (locationId) REFERENCES location(locationId)
		ON DELETE CASCADE
		ON UPDATE CASCADE
);

CREATE TABLE event (
	eventId 		int primary key default nextval('eventId'), 
	sportName 		VARCHAR(50), 
	organiserId 	VARCHAR(30) not null, 
	locationId		int not null, 
	startTime 		time, 
	endTime 		time, 
	startDate 		date, 
	endDate 		date,
	maxParticipants int, 
	description 	VARCHAR(255),
	FOREIGN KEY (sportName) REFERENCES sport(sportName)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	FOREIGN KEY (organiserId) REFERENCES appUser(uid)
		ON DELETE CASCADE
		ON UPDATE CASCADE, 	
	FOREIGN KEY (locationId) REFERENCES location(locationId)
		ON DELETE CASCADE
		ON UPDATE CASCADE 
);	

CREATE TABLE eventJoiningRequest (
	eventId 			int,
	userId				VARCHAR(30),
	type 				requestType,
	status 				status,
	PRIMARY KEY (eventId, userId), 
	FOREIGN KEY (eventId) REFERENCES event(eventId)
		ON DELETE CASCADE
		ON UPDATE CASCADE, 
	FOREIGN KEY (userId) REFERENCES appUser(uid)
		ON DELETE CASCADE
		ON UPDATE CASCADE 
);

CREATE TABLE eventParticipant (
	eventId 		int, 
	userId 			VARCHAR(30), 
	status 			status,
	PRIMARY KEY (eventId, userId), 
	FOREIGN KEY (eventId) REFERENCES event(eventId)
		ON DELETE CASCADE
		ON UPDATE CASCADE, 
	FOREIGN KEY (userId) REFERENCES appUser(uid)
		ON DELETE CASCADE
		ON UPDATE CASCADE
);

CREATE TABLE eventOrganiserFeedback (
	eventId 		int, 
	attendance 		int, 
	comments 		VARCHAR(255),
	PRIMARY KEY (eventId), 
	FOREIGN KEY (eventId) REFERENCES event(eventId)
		ON DELETE CASCADE
		ON UPDATE CASCADE
);
