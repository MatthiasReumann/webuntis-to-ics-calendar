from ics import Calendar, Event
import webuntis as wu
import datetime
import sys
import toml
import requests
import json

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

def getStudentId(id, config):
    session = requests.Session()
    
    req = session.get('https://{}/WebUntis/api/public/timetable/weekly/pageconfig?type=5'.format(config.server),
                cookies = {'JSESSIONID': id})
    
    req_json = json.loads(req.text)
    
    return req_json['data']['elements'][0]['id']



def getTimetable(student, schoolyear, session):
    """Return timetable object of webuntis api"""
    
    return session.timetable(student=student, start=getFirstDay(schoolyear), end=getLastDay(schoolyear));

def getCalendar(session, timetable):
    """Return Calendar object with events(subjects) from webuntis"""

    calendar = Calendar()
   
    for i in range(len(timetable)):
        subject = timetable[i].subjects
        start = timetable[i].start
        end = timetable[i].end
        
        if len(subject) > 0:
            event = createEvent(subject[0], start, end)
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
        useragent = 'webuntis-ics-calendar'
    )
    
    return session

def main():
    config = readTOMLFile(sys.argv[1])
    
    session = getSession(config)
    session.login()
    
    schoolyear = getCurrentSchoolyear(session)
    student = getStudentId(session.config['jsessionid'], config)
    
    timetable = getTimetable(student, schoolyear, session)
    calendar = getCalendar(session, timetable)
    createICSFile(calendar, "webuntis-timetable.ics")
           
    session.logout()

main()
