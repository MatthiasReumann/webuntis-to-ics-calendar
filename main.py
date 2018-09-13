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

def getSchoolClass(schoolclass, session):
    return session.klassen().filter(name=schoolclass)[0]


def getTimetable(schoolclass, session):
    """Return timetable object of webuntis api"""
    
    return session.timetable(klasse=getSchoolClass(schoolclass, session), start=getFirstDay(), end=getLastDay());

def getExams(schoolclass, session):
    """Return exams object of webuntis api"""
    return session.exams(klasse=getSchoolClass(schoolclass,session), start=getFirstDay(), end=getLastDay())


def getTimetableCalendar(session, timetable):
    """Return Calendar object with events(subjects) from webuntis"""

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
    """Return Calendar object with events(exams) from webuntis"""
    
    examList = []
    
    calendar = Calendar()
    
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

def createICSFile(calendar, filename):
    with open(filename, 'w') as f:
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

def validateArguments(args):
    session = getSession(args)
    session.login()
    
    if "-exams" in args:
        exams = getExams(args[5], session)
        calendar = getExamCalendar(session, exams)
    #createICSFile(calendar, "exams.ics")
    else:
        timetable = getTimetable(args[5], session)
        calendar = getTimetableCalendar(session, timetable)
        createICSFile(calendar, "webuntis-timetable.ics")

    session.logout()



def main():
    validateArguments(sys.argv)

main()
