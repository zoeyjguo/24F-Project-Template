# `database-files` Folder

The `database-files` Folder holds two files, one for the DDL of our database **CoLink**, and one for populating the database with sample data for each of the tables, listed below. The data population file, named `SampleData.sql`, has a single line comment indicating the start of a different table's data. 

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

To re-bootstrap the database, open DataGrip, locate the "Run" tab in the menu bar, and click "Edit Configurations...". Click the plus sign in the top left of the Run/Debug Configurations window and select "Database Script". Change the name to "CoLink Script", add a target data source of your choosing, and select "Script files" out of the Execute options. Add `DDL.sql` and `SampleData.sql` and hit OK to add the new run configuration and close the Run/Debug Configurations window. Now locate the "Run" tab again and select "Run 'CoLink Script'".
TODO: Put some notes here about how this works.  include how to re-bootstrap the db. 