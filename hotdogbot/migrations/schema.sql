-- This file is auto-generated. DO NOT EDIT.
-- PRAGMA user_version = 1;
BEGIN TRANSACTION;
CREATE TABLE event_log (
	timestamp TIMESTAMP NOT NULL DEFAULT current_timestamp,
	event_name TEXT NOT NULL,
	payload JSON
);
CREATE TABLE exchange_rates (
	timestamp TIMESTAMP PRIMARY KEY NOT NULL DEFAULT current_timestamp,
	value JSON NOT NULL,
	headers JSON
);
CREATE TABLE guild_settings (
	guild_id TEXT NOT NULL,
	key TEXT NOT NULL,
	value JSON NOT NULL,
	PRIMARY KEY (guild_id, key) ON CONFLICT REPLACE
);
CREATE TABLE ignored_channels (
	channel_id TEXT PRIMARY KEY
);
CREATE TABLE ignored_users (
	user_id TEXT PRIMARY KEY
);
CREATE TABLE user_settings (
	user_id TEXT NOT NULL,
	key TEXT NOT NULL,
	value JSON NOT NULL,
	PRIMARY KEY (user_id, key) ON CONFLICT REPLACE
);
COMMIT;
