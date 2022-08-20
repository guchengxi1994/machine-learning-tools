/*
 Navicat Premium Data Transfer

 Source Server         : 111
 Source Server Type    : SQLite
 Source Server Version : 3017000
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3017000
 File Encoding         : 65001

 Date: 20/08/2022 18:35:30
*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for _project_old_20220820
-- ----------------------------
DROP TABLE IF EXISTS "_project_old_20220820";
CREATE TABLE "_project_old_20220820" (
  "project_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "project_name" TEXT,
  "project_file_path" TEXT,
  "create_at" TEXT,
  "is_deleted" integer
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
  "is_deleted" integer
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

PRAGMA foreign_keys = true;
