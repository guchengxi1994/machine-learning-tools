/*
 Navicat Premium Data Transfer

 Source Server         : 11111
 Source Server Type    : SQLite
 Source Server Version : 3030001
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3030001
 File Encoding         : 65001

 Date: 22/08/2022 14:34:29
*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for file
-- ----------------------------
DROP TABLE IF EXISTS "file";
CREATE TABLE "file" (
  "file_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "file_md5" TEXT,
  "file_path" TEXT,
  "file_size" REAL,
  "project_id" INTEGER,
  "update_at" TEXT DEFAULT CURRENT_TIMESTAMP,
  "create_at" TEXT DEFAULT CURRENT_TIMESTAMP,
  "is_deleted" integer DEFAULT 0
);

-- ----------------------------
-- Table structure for project
-- ----------------------------
DROP TABLE IF EXISTS "project";
CREATE TABLE "project" (
  "project_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "project_name" TEXT,
  "project_file_path" TEXT,
  "update_at" TEXT DEFAULT CURRENT_TIMESTAMP,
  "create_at" TEXT DEFAULT CURRENT_TIMESTAMP,
  "is_deleted" integer DEFAULT 0
);

-- ----------------------------
-- Table structure for sqlite_sequence
-- ----------------------------
DROP TABLE IF EXISTS "sqlite_sequence";
CREATE TABLE "sqlite_sequence" (
  "name",
  "seq"
);

-- ----------------------------
-- Auto increment value for project
-- ----------------------------
UPDATE "sqlite_sequence" SET seq = 8 WHERE name = 'project';

PRAGMA foreign_keys = true;
