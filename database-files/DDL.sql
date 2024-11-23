CREATE DATABASE IF NOT EXISTS PHASE2;
USE PHASE2;

DROP TABLE IF EXISTS EventInterests;
DROP TABLE IF EXISTS Flag;
DROP TABLE IF EXISTS Friend;
DROP TABLE IF EXISTS FriendSuggestion;
DROP TABLE IF EXISTS Message;
DROP TABLE IF EXISTS Post;
DROP TABLE IF EXISTS GroupChatMembers;
DROP TABLE IF EXISTS GroupChat;
DROP TABLE IF EXISTS Admin;
DROP TABLE IF EXISTS Event;
DROP TABLE IF EXISTS Report;
DROP TABLE IF EXISTS UserBadges;
DROP TABLE IF EXISTS Badge;
DROP TABLE IF EXISTS UserInterests;
DROP TABLE IF EXISTS Interest;
DROP TABLE IF EXISTS User;

CREATE TABLE IF NOT EXISTS User
(
    UserId INT PRIMARY KEY AUTO_INCREMENT,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Title VARCHAR(50) NOT NULL,
    HasNotifs BOOLEAN NOT NULL DEFAULT 0,
    Pronouns VARCHAR(50) NOT NULL,
    Points INT NOT NULL DEFAULT 0,
    Longitude FLOAT NOT NULL,
    Latitude FLOAT NOT NULL,
    CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    IsActive BOOLEAN NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS Badge
(
    BadgeId INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(50) NOT NULL,
    PointsWorth INT NOT NULL
);

CREATE TABLE IF NOT EXISTS UserBadges
(
    BadgeId INT,
    UserId INT,
    PRIMARY KEY (BadgeId, UserId),
    CONSTRAINT FOREIGN KEY (UserId) REFERENCES User(UserId)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT FOREIGN KEY (BadgeId) REFERENCES Badge(BadgeId)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Report
(
    ReportId INT PRIMARY KEY AUTO_INCREMENT,
    Reporter INT NOT NULL,
    Title VARCHAR(50) NOT NULL,
    Description VARCHAR(200),
    TimeReported DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT FOREIGN KEY (Reporter) REFERENCES User(UserId)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Friend
(
    FriendId INT,
    UserId INT,
    PRIMARY KEY (FriendId, UserId),
    CONSTRAINT FOREIGN KEY (UserId) REFERENCES User(UserId)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT FOREIGN KEY (FriendId) REFERENCES User(UserId)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS FriendSuggestion
(
    UserId INT,
    SuggestedUser INT,
    PRIMARY KEY (UserId, SuggestedUser),
    CONSTRAINT FOREIGN KEY (UserId) REFERENCES User(UserId)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT FOREIGN KEY (SuggestedUser) REFERENCES User(UserId)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Event
(
    EventId INT PRIMARY KEY AUTO_INCREMENT,
    Latitude FLOAT NOT NULL,
    Longitude FLOAT NOT NULL,
    StartTime DATETIME NOT NULL,
    EndTime DATETIME,
    PointsWorth INT NOT NULL,
    IsVerified BOOLEAN NOT NULL DEFAULT 0 # default
);

CREATE TABLE IF NOT EXISTS Admin
(
    AdminId INT PRIMARY KEY AUTO_INCREMENT,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Pronouns VARCHAR(50) NOT NULL,
    HasNotifs BOOLEAN NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS GroupChat
(
    GroupChatId INT UNIQUE AUTO_INCREMENT,
    EventId INT UNIQUE,
    Monitor INT NOT NULL,
    Name VARCHAR(50),
    PRIMARY KEY (GroupChatId, EventId),
    FOREIGN KEY (EventId) REFERENCES Event(EventId)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (Monitor) REFERENCES Admin(AdminId)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS Post
(
    PostId INT UNIQUE AUTO_INCREMENT,
    EventId INT UNIQUE,
    GroupChatId INT UNIQUE NOT NULL,
    Title VARCHAR(50) NOT NULL,
    Description TEXT,
    CreatedBy INT,
    PointsWorth INT,
    PRIMARY KEY (PostId, EventId),
    FOREIGN KEY (EventId) REFERENCES Event(EventId)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (GroupChatId) REFERENCES GroupChat(GroupChatId)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (CreatedBy) REFERENCES User(UserId)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS GroupChatMembers
(
    GroupChatId INT,
    EventId INT,
    UserId INT,
    PRIMARY KEY (GroupChatId, EventId, UserId),
    CONSTRAINT FOREIGN KEY (GroupChatId, EventId)
        REFERENCES GroupChat(GroupChatId, EventId)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT FOREIGN KEY (UserId) REFERENCES User(UserId)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Message
(
    MessageId INT UNIQUE AUTO_INCREMENT,
    GroupChatId INT,
    EventId INT,
    Sender INT NOT NULL,
    Text TEXT,
    ImageLink VARCHAR(200),
    TimeSent DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (MessageId, GroupChatId, EventId),
    FOREIGN KEY (GroupChatId, EventId)
        REFERENCES GroupChat(GroupChatId, EventId)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (Sender) REFERENCES User(UserId)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Flag
(
    FlagId INT AUTO_INCREMENT PRIMARY KEY,
    MessageId INT,
    PostId INT,
    Title VARCHAR(50) NOT NULL,
    Description VARCHAR(200),
    Flagger INT NOT NULL,
    Reviewer INT,
    CONSTRAINT FOREIGN KEY (Flagger) REFERENCES User(UserId)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT FOREIGN KEY (MessageId)
        REFERENCES Message(MessageId)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT FOREIGN KEY (Reviewer) REFERENCES Admin(AdminId)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    CONSTRAINT FOREIGN KEY (PostId) REFERENCES Post(PostId)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Interest
(
    InterestId INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS EventInterests
(
    EventId INT,
    InterestId INT,
    PostId INT,
    PRIMARY KEY (EventId, InterestId, PostId),
    CONSTRAINT FOREIGN KEY (PostId) REFERENCES Post(PostId)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT FOREIGN KEY (InterestId) REFERENCES Interest(InterestId)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT FOREIGN KEY (EventId) REFERENCES Event(EventId)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS UserInterests
(
    InterestId INT,
    UserId INT,
    PRIMARY KEY (InterestId, UserId),
    CONSTRAINT FOREIGN KEY (InterestId) REFERENCES Interest(InterestId)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT FOREIGN KEY (UserId) references User(UserId)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

-- Insert UserInterests table
INSERT INTO UserInterests (UserId, InterestId)
VALUES
(1, 1),
(2, 2),
(3, 1),
(3,2);

-- Insert Friend table
INSERT INTO Friend (FriendId, UserId)
VALUES
(1, 3),
(3, 1),
(3,2);

-- Insert FriendSuggestion table
INSERT INTO FriendSuggestion (UserId, SuggestedUser)
VALUES
(1, 3),
(2, 3),
(3,1);

-- Insert Post table
INSERT INTO Post (EventId, GroupChatId, CreatedBy, Title, Description, PointsWorth)
VALUES
(1, 1,1,'Photography Exhibition', 'see the best photos of the month',30),
(2, 2,2,'Film Festival', 'vote on your favorite films',30),
(3, 3,2,'Annual Photography Exhibition', 'see the new best photos of the month',30);
INSERT INTO Post (EventId, GroupChatId, Title, Description)
    VALUES (4, 4,'Grinch Viewing', 'Enjoy a classic Christmas movie to remind you of the holidays while abroad.');

-- Insert EventInterests table
INSERT INTO EventInterests (EventId, InterestId, PostId)
VALUES
(1,1, 1),
(2,2, 2),
(3,1, 3),
(4,2, 4);

-- Insert UserBadges table
INSERT INTO UserBadges (UserId, BadgeId)
VALUES
(1, 1),
(2, 2);

-- Insert GroupChatMembers table
INSERT INTO GroupChatMembers (GroupChatId, EventId, UserId)
VALUES
(1, 1, 1),
(2, 2, 1),
(2, 2, 2),
(3, 3, 3),
(4,4,2);

-- Insert Message table
INSERT INTO Message (MessageId, GroupChatId, EventId, Sender, Text, ImageLink)
VALUES
(1, 2,  2, 1, '%^&!#',NULL),
(3, 4,  4, 2, NULL, 'image.jpg'),
(2, 1, 1, 3, 'this is dumb', NULL);

-- Insert Flag table
INSERT INTO Flag (FlagId, MessageId, GroupChatId, EventId, Title, Description, Flagger, Reviewer)
VALUES
(1, 1, 2,  2, 'Duplicate Event', 'This event is already listed.', 2, 1),
(2, 2, 1, 1, 'Spam Message', 'Unnecessary repetitive content.', 2, 1);

-- USER QUERIES
-- User 1
-- Query 1
SELECT p.Title, p.Description
FROM Event e
    JOIN Post p ON e.EventId = p.EventId
	WHERE ABS(e.Latitude - 34.1462) <= 0.5
	AND ABS(e.Longitude - -118.1592) <= 0.5;

-- Query 2
SELECT p.Title, p.Description
FROM Event e
    JOIN Post p ON e.EventId = p.EventId
    JOIN User u ON p.CreatedBy = u.UserId
    JOIN EventInterests ei ON p.EventId = ei.EventId
    JOIN Interest i ON ei.InterestId = i.InterestId
	WHERE u.FirstName = 'Kali' AND u.LastName = 'Linux'
	AND i.Name = 'Photography';

-- Query 3
UPDATE UserInterests
	SET InterestId = 2
WHERE UserId = 1;
SELECT *
FROM UserInterests
WHERE UserId = 1;

-- Query 4
SELECT UserId, FirstName, LastName
FROM User
WHERE FirstName != 'Kali' AND LastName != 'Linux';

-- Query 5
SELECT UserId, FirstName, LastName
FROM User
WHERE User.FirstName != 'Kali' AND User.LastName != 'Linux'
	AND ABS(User.Latitude - 42.3601) <= 0.5
	AND ABS(User.Longitude - 71.0589) <= 0.5;

-- Query 6
SELECT p.Title, p.Description
FROM Event e
    JOIN Post p ON e.EventId = p.EventId
	WHERE p.CreatedBy IS NULL;

-- User 2
-- Query 1
UPDATE Event
SET IsVerified = TRUE
WHERE IsVerified = FALSE;

-- Query 2
DELETE FROM User
WHERE DATEDIFF('2024-11-25', CreatedAt) >= (5 * 365) AND IsActive = FALSE;

-- Query 3
DELETE FROM GroupChat
WHERE EventId In (
	SELECT EventId
	FROM Event
	WHERE EndTime < CURRENT_TIMESTAMP);

-- Query 4
DELETE FROM Event
WHERE EndTime < CURRENT_TIMESTAMP;

-- Query 5
DELETE FROM Message
WHERE Text LIKE '%dumb%';

-- Query 6
UPDATE Report SET Title = CONCAT('[High Priority] ', Title)
WHERE Title LIKE '2024-11-13' OR Description LIKE '%IMPORTANT%';

-- User 3
-- Query 1
UPDATE User
	SET Latitude = 45.4635, Longitude = 9.1824
	WHERE UserId = 2;

-- Query 2
UPDATE User
	SET HasNotifs = TRUE
	WHERE UserId = 2;

-- Query 3
SELECT Post.Title, Post.Description, Event.StartTime, Event.EndTime
FROM Event
    JOIN Post ON Event.EventId = Post.EventId
    JOIN GroupChat ON Event.EventId = GroupChat.EventId
    JOIN GroupChatMembers ON GroupChat.GroupChatId = GroupChatMembers.GroupChatId
	WHERE UserId = 2;

-- Query 4
SELECT ImageLink FROM Message
	WHERE Sender = 2;

-- Query 5
SELECT SuggestedUser FROM FriendSuggestion
WHERE UserId = 2;

-- Query 6
INSERT INTO Friend (FriendId, UserId)
	VALUES (2, 2);

-- User 4
-- Query 1
SELECT Latitude, Longitude, COUNT(UserId) AS StudentCount
FROM User
GROUP BY Latitude, Longitude
ORDER BY StudentCount DESC;

-- Query 2
SELECT Name, COUNT(InterestId) AS InterestCount
FROM Interest
GROUP BY InterestId
ORDER BY InterestCount DESC;

-- Query 3
SELECT EventId, COUNT(EventId) AS InterestStudentCount
FROM EventInterests GROUP BY EventId;

-- Query 4
SELECT UserId, COUNT(FriendId) AS FriendCount
FROM Friend
GROUP BY UserId
ORDER BY FriendCount DESC;

-- Query 5
SELECT ub.UserId, ub.BadgeId, b.Name AS BadgeName, b.PointsWorth
FROM UserBadges ub JOIN Badge b
	WHERE ub.BadgeId = b.BadgeId;

-- Query 6
SELECT UserId, Title
FROM User;