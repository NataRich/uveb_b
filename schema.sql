CREATE DATABASE uveb;

USE uveb;

CREATE TABLE users (
	id INT(11) NOT NULL PRIMARY KEY UNIQUE AUTO_INCREMENT,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    identity SMALLINT(6) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    date DATE NOT NULL,
    numVideos INT(11) NOT NULL DEFAULT 0,
    authenticated TINYINT(4) NOT NULL DEFAULT 0,
    thumbImage VARCHAR(255) NULL,
	mediumImage VARCHAR(255) NULL
);

CREATE TABLE videos (
	id INT(11) NOT NULL PRIMARY KEY UNIQUE AUTO_INCREMENT,
    userId INT(11) NOT NULL,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    description TEXT DEFAULT NULL,
    duration FLOAT NOT NULL,
    trackId VARCHAR(255) NOT NULL UNIQUE,
    resW SMALLINT(6) NOT NULL,
    resH SMALLINT(6) NOT NULL,
    dir VARCHAR(255) NOT NULL,
    size INT(11) NOT NULL,
    date TIMESTAMP NOT NULL,
    likes INT(11) DEFAULT 0,
    views INT(11) DEFAULT 0,
    hotness INT(11) DEFAULT 0,

	FOREIGN KEY (userId) REFERENCES users(id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (author) REFERENCES users(username) ON UPDATE CASCADE ON DELETE CASCADE

);

CREATE TABLE tags (
	id INT(11) NOT NULL PRIMARY KEY UNIQUE AUTO_INCREMENT,
    videoId INT(11) NOT NULL,
    trackId VARCHAR(255) NOT NULL,
    vr TINYINT NOT NULL DEFAULT 0,
    campus TINYINT NOT NULL DEFAULT 0,
    event TINYINT NOT NULL DEFAULT 0,

    FOREIGN KEY (videoId) REFERENCES videos(id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (trackId) REFERENCES videos(trackId) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE map (
	id INT(11) PRIMARY KEY UNIQUE AUTO_INCREMENT,
    tableName VARCHAR(255) NOT NULL UNIQUE,
	column_1 VARCHAR(255) DEFAULT NULL,
    column_2 VARCHAR(255) DEFAULT NULL,
    column_3 VARCHAR(255) DEFAULT NULL,
    column_4 VARCHAR(255) DEFAULT NULL,
    column_5 VARCHAR(255) DEFAULT NULL,
    column_6 VARCHAR(255) DEFAULT NULL,
    column_7 VARCHAR(255) DEFAULT NULL,
    column_8 VARCHAR(255) DEFAULT NULL,
    column_9 VARCHAR(255) DEFAULT NULL,
    column_10 VARCHAR(255) DEFAULT NULL,
    column_11 VARCHAR(255) DEFAULT NULL,
    column_12 VARCHAR(255) DEFAULT NULL,
    column_13 VARCHAR(255) DEFAULT NULL,
    column_14 VARCHAR(255) DEFAULT NULL,
    column_15 VARCHAR(255) DEFAULT NULL,
    column_16 VARCHAR(255) DEFAULT NULL,
    column_17 VARCHAR(255) DEFAULT NULL,
    column_18 VARCHAR(255) DEFAULT NULL,
    column_19 VARCHAR(255) DEFAULT NULL,
    column_20 VARCHAR(255) DEFAULT NULL,
    column_21 VARCHAR(255) DEFAULT NULL,
    column_22 VARCHAR(255) DEFAULT NULL,
    column_23 VARCHAR(255) DEFAULT NULL,
    column_24 VARCHAR(255) DEFAULT NULL,
    column_25 VARCHAR(255) DEFAULT NULL
);

INSERT INTO map (tableName, column_1, column_2, column_3, column_4, column_5, column_6, column_7, column_8, column_9, column_10)
VALUES ('users', 'id', 'username', 'email', 'identity', 'password_hash', 'date', 'numVideos', 'authenticated', 'thumbImage', 'mediumImage');

INSERT INTO map (tableName, column_1, column_2, column_3, column_4, column_5, column_6, column_7, column_8, column_9, column_10,
								column_11, column_12, column_13, column_14, column_15)
VALUES ('videos', 'id', 'userId', 'title', 'author', 'description','duration', 'trackId', 'resW', 'resH', 'dir', 'size', 'date', 'likes', 'views', 'hotness');

INSERT INTO map (tableName, column_1, column_2, column_3, column_4, column_5, column_6)
VALUES ('tags', 'id', 'videoId', 'trackId', 'vr', 'campus', 'event');
