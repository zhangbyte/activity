DROP database if EXISTS activity;

CREATE database activity;

use activity;

GRANT SELECT, INSERT, UPDATE, DELETE ON activity.* TO 'activity'@'localhost' identified BY 'activity';

CREATE TABLE user (
  user_id INTEGER PRIMARY KEY auto_increment,
  email VARCHAR(255) NOT NULL,
  password VARCHAR(255) NOT NULL,
  name VARCHAR(50) NOT NULL,
  phone VARCHAR(50) NOT NULL,
  avatar_url VARCHAR(255) DEFAULT '' NOT NULL,
  gender INTEGER NOT NULL DEFAULT 1 COMMENT '1: 男 2：女',
  type INTEGER NOT NULL DEFAULT 1 COMMENT '1: 用户 2: 组织者'
) engine=innodb DEFAULT charset=utf8;


CREATE TABLE activity (
  activity_id INTEGER PRIMARY KEY auto_increment,
  user_id INTEGER NOT NULL,
  title VARCHAR(50) NOT NULL,
  tags VARCHAR(255) NOT NULL,
  sort VARCHAR(255) NOT NULL,
  place VARCHAR(255) NOT NULL,
  description VARCHAR(255) NOT NULL,
  stars INTEGER DEFAULT 0 NOT NULL,
  guests VARCHAR(255) DEFAULT '' NOT NULL,
  activity_img VARCHAR(255) DEFAULT '' NOT NULL,
  date TIMESTAMP NOT NULL
) engine=innodb DEFAULT charset=utf8;


CREATE TABLE star (
  activity_id INTEGER NOT NULL,
  user_id INTEGER NOT NULL,
  UNIQUE KEY (activity_id, user_id)
) engine=innodb DEFAULT charset=utf8;


CREATE TABLE registration (
  activity_id INTEGER NOT NULL,
  user_id INTEGER NOT NULL,
  name VARCHAR(50) NOT NULL,
  email VARCHAR(255) NOT NULL,
  phone VARCHAR(50) NOT NULL,
  gender INTEGER NOT NULL DEFAULT 1 COMMENT '1: 男 2：女',
  create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
) engine=innodb DEFAULT charset=utf8;
