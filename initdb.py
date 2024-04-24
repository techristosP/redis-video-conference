# Description: This file is used to initialize the Redis database with some data for testing purposes.
class InitDB:

    def __init__(self, db0, db1):
        self.__createUsers(db0)
        self.__createMeetings(db0)
        self.__createMeetingInstances(db0)
        self.__createEventsLog(db1)


    def __createUsers(self, db):
        users = [
            {
                'userID': 1,
                'name': 'Christos',
                'age': 26,
                'gender': 'male',
                'email': 'p3200150@aueb.gr',
            },
            {
                'userID': 2,
                'name': 'Petros',
                'age': 20,
                'gender': 'male',
                'email': 'p3200300@aueb.gr',
            },
        ]

        for user in users:
            db.set(f"user:{user['userID']}", value=user)

    def __createMeetings(self, db):
        meetings = [
            {
                'meetingID': 1,
                'title': 'Student Meeting',
                'description': 'General meeting for students.',
                'isPublic': 'True',
                'audience': 'all'
            },
            {
                'meetingID': 2,
                'title': 'Teacher Meeting',
                'description': 'Invitation only meeting for teachers.',
                'isPublic': 'False',
                'audience': b'p3200150@aueb.gr,p3200400@aueb.gr'
            },
            {
                'meetingID': 3,
                'title': 'Test Meeting',
                'description': 'This is a test purpose meeting.',
                'isPublic': 'True',
                'audience':'all'
            },
            {
                'meetingID': 4,
                'title': 'Future Meeting',
                'description': 'This is a future meeting.',
                'isPublic': 'True',
                'audience':'all'
            }
        ]

        for meeting in meetings:
            db.set(f"meeting:{meeting['meetingID']}", value=meeting)

    def __createMeetingInstances(self, db):
        meeting_instances = [
            {
                'meetingID': 1,
                'orderID': 1,
                'fromdatetime': '2024-04-20 10:00:00',
                'todatetime': '2024-04-20 11:00:00'
            },
            {
                'meetingID': 1,
                'orderID': 2,
                'fromdatetime': '2024-04-20 12:00:00',
                'todatetime': '2024-04-20 13:00:00'
            },
            {
                'meetingID': 1,
                'orderID': 3,
                'fromdatetime': '2024-04-20 15:00:00',
                'todatetime': '2024-05-13 13:00:00'
            },
            {
                'meetingID': 2,
                'orderID': 1,
                'fromdatetime': '2024-04-20 10:00:00',
                'todatetime': '2024-04-20 11:00:00'
            },
            {
                'meetingID': 2,
                'orderID': 2,
                'fromdatetime': '2024-04-20 12:00:00',
                'todatetime': '2024-04-20 13:00:00'
            },
            {
                'meetingID': 2,
                'orderID': 3,
                'fromdatetime': '2024-04-20 15:00:00',
                'todatetime': '2024-05-13 13:00:00'
            },
            {
                'meetingID': 3,
                'orderID': 1,
                'fromdatetime': '2024-04-21 01:00:00',
                'todatetime': '2024-04-24 17:20:00'
            },
            {
                'meetingID': 4,
                'orderID': 1,
                'fromdatetime': '2026-04-25 10:00:00',
                'todatetime': '2026-04-25 11:30:00'
            }
        ]

        for _instance in meeting_instances:
            db.set(f"meeting_instance:{_instance['meetingID']}:{_instance['orderID']}", value=_instance)

    def __createEventsLog(self, db):
        db.set('event_id_counter', hash=False, value=1)
