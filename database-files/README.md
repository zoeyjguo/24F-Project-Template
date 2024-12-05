# `database-files` Folder

The `database-files` Folder holds 17 files to set up our database **CoLink**, one for the DDL and 16 for populating the database with sample data for each of the tables, listed below.

Database: CoLink

Tables:
- **User**, representing a user of the app
- **Badge**, representing a badge (achievement) a user can acquire
- **UserBadges**, holding what badges are associated with a user
- **Report**, representing a report sent to an admin by a user
- **Friend**, representing a friend relationship between two users
- **FriendSuggestion**, representing a friend suggestion relationship between two users
- **Event**, representing an event activity in the app
- **Admin**, representing an admin of the app
- **GroupChat**, representing a group chat in the app
- **Post**, representing a post advertising an event in the app
- **GroupChatMembers**, holding the members of group chats
- **Message**, representing a message in a group chat
- **Flag**, representing a flag on either a post or a messasge in the app
- **Interest**, representing categories of user interests
- **EventInterests**, representing interest categories associated with an event
- **UserInterests**, representing the interest categories a user is interested in

To re-bootstrap the database, run `docker compose down` to shutdown and delete any running containers (to ensure the container runs the most updated data) and then run `docker compose up db -d` to start the database container. Wait until the Docker logs indicate that all files in this folder have executed.