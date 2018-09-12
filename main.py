from ics import Calendar, Event
import webuntis as wu
import datetime

class Subject:
    def __init__(self, name, start, end):
        self.name = name
        self.start = start
        self.end = end

def buildSubjectList(session):
    subjectList = []
    
    today = datetime.date.today()
    monday = today - datetime.timedelta(days=today.weekday())
    friday = monday + datetime.timedelta(days=4)
    
    myClass = session.klassen().filter(name="4CHIF")[0]; #issue: adds lessons that i dont have (bc of '4CHIF')
    
    subj = session.subjects();
    timetable = session.timetable(klasse=myClass, start=monday, end=friday); #get timetable of class 4CHIF
    
    calendar = Calendar() #create new calender (todo: add to existing one)
    
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


def createSession():
    session = wu.Session(
                   server= 'nete.webuntis.com',
                   username = 'reumann.matthias',
                   password = 'test',
                   school = 'htlwrn',
                   useragent = 'webuntis-calender-sync'
    )
    
    session.login()
    
    createICSFile(buildSubjectList(session))
    
    session.logout()

def main():
    createSession();

main()
