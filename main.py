from ics import Calendar, Event
import webuntis as wu
import datetime
import sys
import toml

class Subject:
    def __init__(self, name, start, end):
        self.name = name
        self.start = start
        self.end = end

class Config:
    def __init__(self, server, username, password, schoolclass, school):
        self.server = server
        self.username = username
        self.password = password
        self.schoolclass = schoolclass
        self.school = school


def getFirstDay(schoolyear):
    """Return current monday"""
    
    return schoolyear.start

def getLastDay(schoolyear):
    """Return last day of current schoolyear"""
    
    return schoolyear.end

def getCurrentSchoolyear(session):
    year = session.schoolyears()
    return year.filter(id=year.current.id)[0]

def getSchoolClass(schoolclass, session):
    """Return schoolclass"""
    
    return session.klassen().filter(name=schoolclass)[0]

def getTimetable(schoolclass, session):
    """Return timetable object of webuntis api"""
    schoolyear = getCurrentSchoolyear(session)
    
    return session.timetable(klasse=getSchoolClass(schoolclass, session), start=getFirstDay(schoolyear), end=getLastDay(schoolyear));

def getExams(schoolclass, session):
    """Return exams object of webuntis api"""
    
    return session.exams(klasse=getSchoolClass(schoolclass,session), start=getFirstDay(schoolyear), end=getLastDay(schoolyear))

def getTimetableCalendar(session, timetable):
    """Return Calendar object with events(subjects) from webuntis"""

    calendar = Calendar()
   
    for i in range(len(timetable)):
        subject = timetable[i].subjects
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

def readTOMLFile(filename):
    """Return Config object"""
    
    toml_string = ""
    with open(filename, 'r') as f:
        toml_string = toml_string + f.read()

    parsed_toml = toml.loads(toml_string)
    user = parsed_toml["user"]
    return Config(user["server"],user["username"],user["password"],
                  user["class"],user["school"])

def getSession(config):
    """Return Session object"""
    
    session = wu.Session(
        server = config.server,
        username = config.username,
        password = config.password,
        school = config.school,
        useragent = 'webuntis-calender-sync'
    )
    
    return session

def main():
    config = readTOMLFile(sys.argv[1])
    
    session = getSession(config)
    session.login()
    
    timetable = getTimetable(config.schoolclass, session)
    calendar = getTimetableCalendar(session, timetable)
    createICSFile(calendar, "webuntis-timetable.ics")
   
    
    session.logout()

main()
