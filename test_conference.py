from conference import ConferenceApp
import time

def test_conference():
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

if __name__ == '__main__':
    test_conference()