from conference import ConferenceApp
import time

def test_conference():
    c = ConferenceApp(init=True)

    print(c.join_meeting(1, 1))
    time.sleep(1)
    print(c.join_meeting(2, 1))
    time.sleep(1)
    print(c.join_meeting(1, 2))
    time.sleep(1)
    print(c.join_meeting(2, 2))
    time.sleep(1)

    print(c.leave_meeting(1, 1))
    time.sleep(1)
    print(c.leave_meeting(1, 1))
    time.sleep(1)
    print(c.leave_meeting(1, 2))

    print(c.meeting_participants(1))
    print(c.meeting_participants(2))
    print(c.meeting_participants(3))

    # print(c.show_active_meetings())

    print(c.join_meeting(1, 3))
    time.sleep(1)
    print(c.join_meeting(2, 3))
    # time.sleep(31)

    print(c.leave_meeting(1, 3))
    print(c.leave_meeting(1, 3))
    # time.sleep(1)

    # c.end_meeting(3)

    # print(c.meeting_participants(1))
    # print(c.meeting_participants(2))
    # print(c.meeting_participants(3))


if __name__ == '__main__':
    test_conference()