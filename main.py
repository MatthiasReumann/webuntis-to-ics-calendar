from ics import Calendar, Event
import webuntis as wu
import datetime
import sys

class Subject:
    def __init__(self, name, start, end):
        self.name = name
        self.start = start
        self.end = end

def getTimetable(session):
    """Return timetable object of webuntis api"""

    today = datetime.date.today()
    monday = today - datetime.timedelta(days=today.weekday())
    lastday = monday + datetime.timedelta(days=100) #take that year

    schoolClass = session.klassen().filter(name=sys.argv[5])[0]; #issue: adds lessons that i dont have

    return session.timetable(klasse=schoolClass,start=monday, end=lastday); #get timetable of class 4CHIF

def getCalendar(session):
    """Return Calendar object with events from webuntis"""

    subjectList = []

    calendar = Calendar() #create new calender (todo: add to existing one)

    timetable = getTimetable(session)

    for i in range(len(timetable)):
        subject = timetable[i].subjects[0]
        start = timetable[i].start
        end = timetable[i].end

        event = createEvent(subject, start, end)
        calendar.events.add(event)

    return calendar

def createEvent(subject, start, end):
    """Return Event object"""

    event = Event()
    event.name = str(subject)
    event.begin = start + datetime.timedelta(hours=-2)
    event.end = end + datetime.timedelta(hours=-2)

    return event

def createICSFile(calendar):
    with open('webuntis-calender.ics', 'w') as f:
        f.writelines(calendar)

def createSession():
    session = wu.Session(
        server = sys.argv[1],
        username = sys.argv[2],
        password = sys.argv[3],
        school = sys.argv[4],
        useragent = 'webuntis-calender-sync'
    )

    session.login()

    createICSFile(getCalendar(session))

    session.logout()

def main():
    createSession()

main()
