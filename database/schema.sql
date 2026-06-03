-- Run this file once to set up the database
-- mysql -u root -p < database/schema.sql

CREATE DATABASE IF NOT EXISTS smartprepcollage
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE smartprepcollage;

CREATE TABLE IF NOT EXISTS certificates (
    id             INT AUTO_INCREMENT PRIMARY KEY,
    certificate_id VARCHAR(30)  NOT NULL UNIQUE,
    student_name   VARCHAR(120) NOT NULL,
    course_name    VARCHAR(200) NOT NULL,
    score          VARCHAR(20)  NOT NULL,
    issue_date     DATE         NOT NULL,
    image_path     VARCHAR(300) NOT NULL,
    created_at     TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
