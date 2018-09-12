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

    schoolClass = session.klassen().filter(name="4CHIF")[0]; #issue: adds lessons that i dont have (bc of '4CHIF')
    
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
        
        createEvent(subject, start, end, calendar)

    return calendar

def createEvent(subject, start, end, calendar):
    event = Event()
    event.name = str(subject)
    event.begin = start
    event.end = end
    calendar.events.add(event)

def createICSFile(calendar):
    with open('webuntis.ics', 'w') as f:
        f.writelines(calendar)

def createSession(server, username, password, school):
    session = wu.Session(
        server = server,
        username = username,
        password = password,
        school = school,
        useragent = 'webuntis-calender-sync'
    )
    
    session.login()
    
    createICSFile(createSubjectList(session))
    
    session.logout()

def validateArguments():
    if len(sys.argv) != 6:
        usage()




def usage():
    print("usage")


def main():
    validateArguments();
    createSession(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]);

main()
