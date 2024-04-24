from conference import ConferenceApp
import time

def test_conference():
    c = ConferenceApp(init=True)

    # Joins
    c.join_meeting(1, 1)
    time.sleep(1)
    c.join_meeting(2, 1)
    time.sleep(1)
    c.join_meeting(1, 2)
    time.sleep(1)
    c.join_meeting(2, 2)
    time.sleep(1)

    # Leaves
    c.leave_meeting(1, 1)
    time.sleep(1)
    c.leave_meeting(1, 2)
    time.sleep(1)
    c.leave_meeting(1, 2)

    # Participants
    # print(c.meeting_participants(1))
    # print(c.meeting_participants(2))
    # print(c.meeting_participants(3))

    # Active Meetings
    # c.show_active_meetings()

    # c.join_meeting(1, 3)
    # time.sleep(1)
    # c.join_meeting(2, 3)
    # time.sleep(1)
    # c.leave_meeting(2, 3)
    # time.sleep(31)

    # c.leave_meeting(1, 3)
    # c.leave_meeting(1, 3)
    # time.sleep(1)

    # End Meetings
    # stopMeeting=True stops the active meetinginstance
    # stopMeeting=False terminates the ended meetinginstance properly
    c.end_meeting(1, stopMeeting=True)
    c.end_meeting(2, stopMeeting=False)
    c.end_meeting(3)

    # c.meeting_participants(1)
    # c.meeting_participants(2)
    # c.meeting_participants(3)

    # Join times
    # c.meeting_participants_join_time()

    # Test messages
    # c.post_message(1, 1, 'Hi Petros!')
    # time.sleep(1)
    # c.post_message(2, 1, "Hi Christos!")
    # time.sleep(1)
    # c.post_message(1, 1, "Sup?") 
    # time.sleep(1)
    # c.post_message(2, 1, "Nothing much.")
    # time.sleep(1)
    # c.post_message(1, 1, "Cool.")
    # time.sleep(1)
    # c.post_message(2, 1, "Yeah.")

    # Meeting messages
    # c.meeting_messages(1)

    # Meeting - user messages
    # c.show_meeting_user_messages(1, 1)
    # c.show_meeting_user_messages(2, 1)

if __name__ == '__main__':
    test_conference()