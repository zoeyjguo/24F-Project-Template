# CoLink Project Repository

CoLink is a data-driven application focused on improving the experiential learning space at Northeastern University. It does this by tackling the need for community among Northeastern students on co-op with an event-based, interest categorized, and location-centric social media platform.

## Description

Our app satisfies the need for community among Northeastern students on co-op by creating tailored opportunities to meet others with similar personal and professional interests, backgrounds, and experiences. Our platform emphasizes highly personalized, data-driven engagement, allowing users to set up profiles detailing interests and goals to form a curated feed of interest-based events. In particular, users can join groups, attend events, and even create posts to find others interested in joining activities. Users also have their point system where you can earn badges based on how many events you plan and attend! Key features like curated For You Pages (FYP) based on user interests, event posts with group chat integration, app-generated recommendations, and point system based on event attendance empower students to build a support network while they are on co-op. Our platform ensures that our members stay connected to the Northeastern student community no matter where they are around the world.

Accessing our app is very simple! As a user, you are able to look at your home page, create posts or even join group chats related to each post! Additionally, users are able to look at a list of suggested users who they can add as friends. Users are able to access their own profiles showcasing their basic information along with their posts and group chats, and they are able to see similar information for other users as well. Aside from student users, we also have a system administrator that maintains the platform. Administrators can look at reports, flag messages, and delete group chats as needed.

Finally, we have a data analyst in charge of collected user information to see how digital application can impact students experimental learning. Data analysts are able to view the most popular interests among students, user badge rankings, and the profile and ranking of a specific user.

### Handling User Role Access and Control

In most applications, when a user logs in, they assume a particular role. To do this in Streamlit, we've implemented a Role-based Access Control (**RBAC**) system that removes the need for using user authentication (usernames and passwords) as well as user profile set up. For simplicity's sake (and to render the UI for some of our pages), we've assumed each logged-in user has a username, biography, email address, phone number, profile picture, and background profile picture in the system, each initialized upon their profile creation, but these values cannot be changed within our application. To learn more about our RBAC system, navigate to the `pages` directory.

## Getting Started

### Project Components

Our project has three major components which will each run in their own Docker Containers:

- Streamlit App in the `./app` directory
- Flask REST API in the `./api` directory
- SQL files for our data model and database in the `./database-files` directory

### Controlling the Containers

- `docker compose up -d` to start all the containers in the background
- `docker compose down` to shutdown and delete the containers
- `docker compose up db -d` to only start the database container (replace db with the other services as needed)
- `docker compose stop` to "turn off" the containers but not delete them.

### Installing & executing program

To download our program,

- Clone this repository
- Add and/or update an .env file to the `./api` directory.  
   Below is an example of what this .env file should contain:

```
SECRET_KEY=someCrazyS3cR3T!Key.!
DB_USER=root
DB_HOST=db
DB_PORT=3306
DB_NAME=CoLink
MYSQL_ROOT_PASSWORD={enter_password_here}
```

- Run the following commands in the terminal:

```
docker compose up -d
```

Wait until the logs of the `mysql_db` container indicate that all the .sql files in the `./database-files` directory have been executed.

- View the application on [your machine's port 8501](http://localhost:8501)

## Authors

[Amy Wang](https://github.com/amywng)
[Sarah Zhang](https://github.com/Sarah-Zhang1)
[Zoey Guo](https://github.com/zoeyjguo)
[Deborah He](https://github.com/deborahhe2493)
[Julia Tan](https://github.com/juliaatan)
