from ics import Calendar, Event
import webuntis as wu
import datetime
import sys

class Subject:
    def __init__(self, name, start, end):
        self.name = name
        self.start = start
        self.end = end

def getFirstDay():
    """Return current monday"""
    
    today = datetime.date.today()
    return today - datetime.timedelta(days=today.weekday())

def getLastDay():
    """Return last day of the current schoolyear"""
    
    return getFirstDay() + datetime.timedelta(weeks=38)

def getTimetable(session):
    """Return timetable object of webuntis api"""

    schoolClass = session.klassen().filter(name=sys.argv[5])[0]; #issue: adds lessons that i dont have

    return session.timetable(klasse=schoolClass,start=getFirstDay(), end=getLastDay()); #get timetable of class 4CHIF

def getExams(session):
    print("test")


def getTimetableCalendar(session, timetable):
    """Return Calendar object with events from webuntis"""

    subjectList = []

    calendar = Calendar()

    for i in range(len(timetable)):
        subject = timetable[i].subjects[0]
        start = timetable[i].start
        end = timetable[i].end

        event = createEvent(subject, start, end)
        calendar.events.add(event)

    return calendar

def getExamCalendar(session):
    
    examList = []



def createEvent(subject, start, end):
    """Return Event object"""

    event = Event()
    event.name = str(subject)
    event.begin = start + datetime.timedelta(hours=-2)
    event.end = end + datetime.timedelta(hours=-2)

    return event

def createICSFile(calendar):
    with open('webuntis-timetable.ics', 'w') as f:
        f.writelines(calendar)

def getSession(args):
    """Return Session object"""
    
    session = wu.Session(
        server = args[1],
        username = args[2],
        password = args[3],
        school = args[4],
        useragent = 'webuntis-calender-sync'
    )
    
    return session

#session.login()

# createICSFile(getCalendar(session))

#session.logout()

def validateArguments(args):
    session = getSession(args)
    session.login()
    
    if "-exams" in args:
    #calendar = getTimetableCalendar(session)
        print("sopron")
    else:
        timetable = getTimetable(session)
        calendar = getTimetableCalendar(session, timetable)
        createICSFile(calendar)

    session.logout()



def main():
    validateArguments(sys.argv)

main()
