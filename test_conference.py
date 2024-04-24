from conference import ConferenceApp
import time

def general_tests():
    c = ConferenceApp(reset=True)

    # Joins
    c.join_meeting(1, 1)
    time.sleep(1)
    c.join_meeting(2, 1)
    time.sleep(1)
    c.join_meeting(1, 2)
    time.sleep(1)
    c.join_meeting(2, 2)
    time.sleep(1)

    print('\n')

    # Leaves
    c.leave_meeting(1, 1)
    time.sleep(1)
    c.leave_meeting(1, 2)
    time.sleep(1)
    c.leave_meeting(1, 2)

    print('\n')

    # Participants
    c.meeting_participants(1)
    c.meeting_participants(2)
    c.meeting_participants(3)

    print('\n')

    # Active Meetings
    c.show_active_meetings()
    
    print('\n')

    c.join_meeting(1, 3)
    time.sleep(1)
    c.join_meeting(2, 3)
    time.sleep(1)
    c.leave_meeting(2, 3)
    # time.sleep(31)

    c.leave_meeting(1, 3)
    c.leave_meeting(1, 3)
    time.sleep(1)

    print('\n')
    
    # End Meetings
    # stopMeeting=True stops the active meetinginstance
    # stopMeeting=False terminates the ended meetinginstance properly
    c.end_meeting(1, stopMeeting=True)
    print('\n')
    c.end_meeting(2, stopMeeting=False)
    print('\n')
    c.end_meeting(3)
    print('\n')

    print('\n')

    c.meeting_participants(1)
    c.meeting_participants(2)
    c.meeting_participants(3)

    print('\n')

    # Join times
    c.meeting_participants_join_time()

    print('\n')

    # Test messages
    c.post_message(1, 1, 'Hi Petros!')
    time.sleep(1)
    c.post_message(2, 1, "Hi Christos!")
    time.sleep(1)
    c.post_message(1, 1, "Sup?") 
    time.sleep(1)
    c.post_message(2, 1, "Nothing much.")
    time.sleep(1)
    c.post_message(1, 1, "Cool.")
    time.sleep(1)
    c.post_message(2, 1, "Yeah.")

    print('\n')

    # Meeting messages
    c.meeting_messages(1)

    print('\n')

    # Meeting - user messages
    c.show_meeting_user_messages(1, 1)
    c.show_meeting_user_messages(2, 1)


def test_join_meeting():
    c = ConferenceApp(reset=True)

    # Test joining a user to a public meeting
    print('\nCase 1:\n')
    c.join_meeting(1, 1)  # User 1 joins Meeting 1
    c.join_meeting(2, 1)  # User 2 joins Meeting 1

    # Test joining a user to a meeting that has already joined
    print('\nCase 2:\n')
    c.join_meeting(1, 1)  # User 1 tries to join Meeting 1 again
    
    # Test joining a user to a private meeting
    print('\nCase 3:\n')
    c.join_meeting(1, 2)  # User 1 joins Meeting 2 (private)

    # Test joining a user who is not invited to a private meeting
    print('\nCase 4:\n')
    c.join_meeting(2, 2)  # User 2 joins Meeting 2 (private)

    # Test joining a user to a non-existent meeting
    print('\nCase 5:\n')
    c.join_meeting(1, 5)  # User 1 tries to join Meeting 5 (non-existent)

    # Test joining a non-existent user to a meeting
    print('\nCase 6:\n')
    c.join_meeting(3, 1)  # User 4 tries to join Meeting 1 (non-existent user)

    # Test joining a non-existent user to a non-existent meeting
    print('\nCase 7:\n')
    c.join_meeting(3, 5)  # User 4 tries to join Meeting 5 (non-existent user and meeting)

    # Test joining a user to a meeting with no active instances
    print('\nCase 8:\n')
    c.join_meeting(1, 3)  # User 1 tries to join Meeting 3 (no active instances)

    # Test joining a user to a meeting with a future instance
    print('\nCase 9:\n')
    c.join_meeting(1, 4)  # User 1 tries to join Meeting 4 (future instance)

def test_leave_meeting():
    c = ConferenceApp(reset=True)

    c.join_meeting(1, 1)  # User 1 joins Meeting 1
    
    # Test leaving a meeting
    print('\nCase 1:\n')
    c.leave_meeting(1, 1)  # User 1 leaves Meeting 1
    c.leave_meeting(1, 1)  # User 1 leaves Meeting 1 again

    # Test leaving a meeting that the user hasn't joined
    print('\nCase 2:\n')
    c.leave_meeting(2, 1)  # User 2 tries to leave Meeting 1 (not joined)

    # Test leaving a non-existent meeting
    print('\nCase 3:\n')
    c.leave_meeting(1, 5)  # User 1 tries to leave Meeting 5 (non-existent)

    # Test leaving a meeting with an error
    print('\nCase 4:\n')
    c.leave_meeting(1, 4)  # User 1 tries to leave Meeting 4 (future instance)

    # Test leaving a meeting with a future instance
    print('\nCase 5:\n')
    c.leave_meeting(1, 3)  # User 1 tries to leave Meeting 4 (old instance)

def test_meeting_participants():
    c = ConferenceApp(reset=True)

    c.join_meeting(1, 1)  # User 1 joins Meeting 1
    c.join_meeting(2, 1)  # User 2 joins Meeting 1

    # Test getting participants of a meeting
    print('\nCase 1:\n')
    c.meeting_participants(1)  # Get participants of Meeting 1
    c.meeting_participants(2)  # Get participants of Meeting 2

    # Test getting participants of a meeting with no active instances
    print('\nCase 2:\n')
    c.meeting_participants(3)

    # Test getting participants of a non-existent meeting
    print('\nCase 3:\n')
    c.meeting_participants(5)  # Get participants of Meeting 5 (non-existent)

def test_show_active_meetings():
    c = ConferenceApp(reset=True)

    # Test showing active meetings
    print('\nCase 1:\n')
    c.show_active_meetings()  # Show active meetings


    # Create a new meeting instance
    print('\nCase 2:\n')
    new_instance = {
        'meetingID': 3,
        'orderID': 2,
        'fromdatetime': '2024-04-20 10:00:00',
        'todatetime': '2100-04-20 11:00:00'
    }
    c.db.set(f"meeting_instance:{new_instance['meetingID']}:{new_instance['orderID']}", value=new_instance)

    # Test showing active meetings with no active instances
    c.show_active_meetings()  # Show active meetings

def test_end_meeting():
    c = ConferenceApp(reset=True)

    # Test ended instance of a meeting
    print('\nCase 1:\n')
    c.end_meeting(1)  # End Meeting 1

    # Test ending an already ended meeting (no active or future instances)
    print('\nCase 2:\n')
    c.end_meeting(3)  # End Meeting 1 again

    # Test ending a meeting with a future instance
    print('\nCase 3:\n')
    c.end_meeting(4)  # End Meeting 4 (future instance)

    # Test ending a non-existent meeting
    print('\nCase 4:\n')
    c.end_meeting(5)  # End Meeting 5 (non-existent)


    # Join users to active instance of meeting 1
    print('\nCase 5:\n')
    c.join_meeting(1, 1)  # User 1 joins Meeting 1
    c.join_meeting(2, 1)  # User 2 joins Meeting 1
    time.sleep(1)
    c.leave_meeting(1, 1)  # User 1 leaves Meeting 1
    time.sleep(1)

    # Stop the active instance of meeting 1
    print('\n')
    c.end_meeting(1, stopMeeting=True)  # Stop Meeting 1


    # Join user to active instance of meeting 2
    print('\nCase 6:\n')
    c.join_meeting(1, 2)  # User 1 joins Meeting 2
    time.sleep(1)

    # Stop the active instance of meeting 2
    print('\n')
    c.end_meeting(2, stopMeeting=True)  # End Meeting 2


    # Create a new meeting instance
    print('\nCase 7:\n')
    current_time = time.localtime()
    new_time = time.mktime(time.struct_time((current_time.tm_year, current_time.tm_mon, current_time.tm_mday,
                                          current_time.tm_hour, current_time.tm_min, current_time.tm_sec + 10,
                                          current_time.tm_wday, current_time.tm_yday, current_time.tm_isdst)))
    new_instance = {
        'meetingID': 3,
        'orderID': 2,
        'fromdatetime': '2024-04-20 10:00:00',
        'todatetime': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(new_time))
    }
    c.db.set(f"meeting_instance:{new_instance['meetingID']}:{new_instance['orderID']}", value=new_instance)
    c.join_meeting(1, 3) # User 1 joins Meeting 3
    time.sleep(1)
    c.join_meeting(2, 3) # User 2 joins Meeting 3
    time.sleep(12)

    # Active instance of meeting 3 has ended and joined users are removed
    c.end_meeting(3)  # End Meeting 3

def test_meeting_participants_join_time():
    c = ConferenceApp(reset=True)

    # Case 1 - Only meeting 1 has joined users
    # Join users to active instance of meeting 1
    c.join_meeting(1, 1)  # User 1 joins Meeting 1
    c.join_meeting(2, 1)  # User 2 joins Meeting 1
    time.sleep(1)
    c.leave_meeting(1, 1)  # User 1 leaves Meeting 1
    time.sleep(1)

    # Test getting participants of a meeting with join times
    print('\nCase 1:\n')
    c.meeting_participants_join_time()

    print('++++++++++++++++++++++++++++++++++++++++++++++\n')

    # Case 2 - Meetings 1 and 2 have joined users
    # Join users to active instance of meeting 2
    c.join_meeting(1, 2)  # User 1 joins Meeting 2

    # Test getting participants of a meeting with join times
    print('\nCase 2:\n')
    c.meeting_participants_join_time()

def test_post_message():
    c = ConferenceApp(reset=True)

    # Test posting a message to a meeting
    print('\nCase 1:\n')
    c.post_message(1, 1, 'Hi Petros!')  # User 1 posts a message to Meeting 1
    time.sleep(1)
    c.post_message(2, 1, "Hi Christos!")  # User 2 posts a message to Meeting 1
    time.sleep(1)
    c.post_message(1, 1, "Sup?")  # User 1 posts a message to Meeting 1
    time.sleep(1)
    c.post_message(2, 1, "Nothing much.")  # User 2 posts a message to Meeting 1
    time.sleep(1)
    c.post_message(1, 1, "Cool.")  # User 1 posts a message to Meeting 1
    time.sleep(1)
    c.post_message(2, 1, "Yeah.")  # User 2 posts a message to Meeting 1

    # Test posting a message to a non-existent meeting
    print('\nCase 2:\n')
    c.post_message(1, 5, 'Hi someone!')  # User 1 posts a message to Meeting 5 (non-existent)

    # Test posting a message to a meeting with no active instances
    print('\nCase 3:\n')
    c.post_message(1, 3, 'Is anybody there!')  # User 1 posts a message to Meeting 3 (no active instances)

    # Test posting a message to a meeting with a future instance
    print('\nCase 4:\n')
    c.post_message(1, 4, 'Hello there!')  # User 1 posts a message to Meeting 4 (future instance)

def test_meeting_messages():
    c = ConferenceApp(reset=True)

    c.post_message(1, 1, 'Hi Petros!')  # User 1 posts a message to Meeting 1
    time.sleep(1)
    c.post_message(2, 1, "Hi Christos!")  # User 2 posts a message to Meeting 1
    time.sleep(1)
    c.post_message(1, 1, "Sup?")  # User 1 posts a message to Meeting 1
    time.sleep(1)
    c.post_message(2, 1, "Nothing much.")  # User 2 posts a message to Meeting 1
    time.sleep(1)
    c.post_message(1, 1, "Cool.")  # User 1 posts a message to Meeting 1
    time.sleep(1)
    c.post_message(2, 1, "Yeah.")  # User 2 posts a message to Meeting 1
    
    # Test getting messages of a meeting
    print('\nCase 1:\n')
    c.meeting_messages(1)  # Get messages of Meeting 1

    # Test getting messages of a meeting with no posts
    print('\nCase 2:\n')
    c.meeting_messages(2)  # Get messages of Meeting 2

    # Test getting messages of a non-existent meeting
    print('\nCase :\n')
    c.meeting_messages(5)  # Get messages of Meeting 5 (non-existent)

def test_show_meeting_user_messages():
    c = ConferenceApp(reset=True)

    c.post_message(1, 1, 'Hi Petros!')  # User 1 posts a message to Meeting 1
    time.sleep(1)
    c.post_message(2, 1, "Hi Christos!")  # User 2 posts a message to Meeting 1
    time.sleep(1)
    c.post_message(1, 1, "Sup?")  # User 1 posts a message to Meeting 1
    time.sleep(1)
    c.post_message(2, 1, "Nothing much.")  # User 2 posts a message to Meeting 1
    time.sleep(1)
    c.post_message(1, 1, "Cool.")  # User 1 posts a message to Meeting 1
    time.sleep(1)
    c.post_message(2, 1, "Yeah.")  # User 2 posts a message to Meeting 1

    # Test getting messages of a meeting
    print('\nCase 1:\n')
    c.show_meeting_user_messages(1, 1)  # Get messages of Meeting 1 by User 1

    # Test getting messages of a meeting with no posts
    print('\nCase 2:\n')
    c.show_meeting_user_messages(2, 1)  # Get messages of Meeting 1 by User 2

    # Test getting messages of a meeting with no posts
    print('\nCase 3:\n')
    c.post_message(2, 2, 'Hi Christos!')  # User 2 posts a message to Meeting 2
    c.post_message(2, 2, 'Are you there?...')  # User 2 posts a message to Meeting 2
    c.show_meeting_user_messages(1, 2)  # Get messages of Meeting 2 by User 1 (non-existent)

    # Test getting messages of a non-existent meeting
    print('\nCase 4:\n')
    c.show_meeting_user_messages(1, 5)  # Get messages of Meeting 5 by User 1 (non-existent)

    # Test getting messages of a non-existent user
    print('\nCase 5:\n')
    c.show_meeting_user_messages(5, 1)  # Get messages of Meeting 1 by User 5 (non-existent)


if __name__ == '__main__':
    test_join_meeting()
    print("-----------------------------------------------------------------------------------")
    
    test_leave_meeting()
    print("-----------------------------------------------------------------------------------")

    test_meeting_participants()
    print("-----------------------------------------------------------------------------------")

    test_show_active_meetings()
    print("-----------------------------------------------------------------------------------")

    test_end_meeting()
    print("-----------------------------------------------------------------------------------")

    test_meeting_participants_join_time()
    print("-----------------------------------------------------------------------------------")

    test_post_message()
    print("-----------------------------------------------------------------------------------")

    test_meeting_messages()
    print("-----------------------------------------------------------------------------------")

    test_show_meeting_user_messages()
    print("-----------------------------------------------------------------------------------")
