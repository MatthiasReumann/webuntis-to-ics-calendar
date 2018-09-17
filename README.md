# webuntis-calendar-sync
Create .ics file from webuntis timetable

.ics files can be used to get your webuntis timetable to:
- Google Calendar
- macOS Calendar
- ...

## Config file

Configuration file [(.toml)](https://github.com/toml-lang/toml) syntax

```
[user]
server = "nete.webuntis.com"
username = "firstname.lastname"
password = "supersecret"
school = "superschool"
class = "SUPER4"
```


## Usage
```
python3 main.py <config>
```
