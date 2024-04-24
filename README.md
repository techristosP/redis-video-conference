# Conference App

A set of methods that allows users to do basic video-conference tasks.
The app uses Redis as a backend storage service to store meetings, users, events, and messages.

### Features

- **Join and Leave Meetings**: Users can join and leave meetings, with support for checking if a meeting is public or if the user is invited.
- **Retrieve Meeting Participants**: Retrieve a list of participants for a given meeting.
- **Show Active Meetings**: Retrieve a list of active meetings.
- **End Meeting Instances**: End the latest instance of a meeting.
- **Show User Join Time**: Retrieve a list of active meetings and the time each user joined it.
- **Post Messages in Meetings**: Users can post messages in meetings, and the messages are stored in Redis for retrieval.
- **Retrieve Meeting Messages**: Retrieve and display all messages sent in a given meeting in chronological order.
- **Show Meeting User Messages**: Retrieve and display all messages sent by a specific user in a given meeting.

### Schema

A database (db0) of:
- users (userID, name, age, gender, email)
- meetings (meetingID, title, description, isPublic, audience)
- meeting_instances (meetingID, orderID, fromdatetime, todatetime)

A database (db1) of:
- events (event_id, userID, meetingID, event_type, timestamp)
- messages (meetingID, orderID, userID, text, timestamp)

1. event_type can be 1 (join_meeting), 2 (leave_meeting), 3 (timeout)
2. A meeting either has an audience (a list of emails) or it is public.

#### Assumptions
- Only one instance of a meeting can be active at a time, the one with the highest orderID.

### Prerequisites

Before running the application, make sure you have the following installed:

- Python 3.x
- Redis server

### Installation

Install Redis in your system using the following command:

```bash
sudo apt-get update
sudo apt-get install redis-server
```
Intall Redis python package using the following command:
```bash
pip install redis
```

### Usage

1. Check if the Redis server is running. If not, start the server using the following command:
    ```bash
    sudo systemctl status redis-server #to check the status of the server
    sudo systemctl start redis-server #to run the server
    ```

2. Import ConferenceApp class from conference.py and create an object of it. Use the object to call the methods of the class.

    ```python
    from conference import ConferenceApp
    conference = ConferenceApp()
    ```

    You can now use the object to call the methods of the class.
    Databases 'db0' and 'db1' are created when the object is created and are initialized with some sample data you can find in the initdb.py file using InitDB class.

#### Test file

You can run the test file `test_conference.py` to see how the methods work.

```bash
python3 test_conference.py
```
