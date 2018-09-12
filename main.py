from ics import Calendar, Event
import webuntis as wu
import datetime
import sys

class Subject:
    def __init__(self, name, start, end):
        self.name = name
        self.start = start
        self.end = end

def createTimetable(session):
    """Return timetable object of webuntis api"""
    
    today = datetime.date.today()
    monday = today - datetime.timedelta(days=today.weekday())
    friday = monday + datetime.timedelta(days=4)

    schoolClass = session.klassen().filter(name=sys.argv[5])[0]; #issue: adds lessons that i dont have
    
    return session.timetable(klasse=schoolClass, start=monday, end=friday); #get timetable of class 4CHIF

def createSubjectList(session):
    """Return Calendar object with events from webuntis"""
    
    subjectList = []
    
    calendar = Calendar() #create new calender (todo: add to existing one)
    
    timetable = createTimetable(session)
    
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
    event.begin = start
    event.end = end
    
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
    
    createICSFile(createSubjectList(session));
    
    session.logout()

def validateArguments():
    if len(sys.argv) != 6 or sys.argv[1] == "-help":
        usage()
    else:
        createSession()


def usage():
    print("usage")

def main():
    validateArguments();

main()
