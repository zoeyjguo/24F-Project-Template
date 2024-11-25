CREATE DATABASE IF NOT EXISTS CoLink;
USE CoLink;

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
    Title VARCHAR(75) NOT NULL,
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