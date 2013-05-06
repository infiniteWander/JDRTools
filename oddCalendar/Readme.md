oddCalendar
=========

Handle odd calendars operations

Using it in a nutshell
-------
+ `./oddCalendar.py` or `ledit ./oddCalendar.py` launch and interactive shell
+ `./oddCalendar.py 33/22/11 + 33d -1m` will display the date 33 days less one month from 33/22/11

Allowed operations
-------
Formatting:
+ The dates uses Gregorian little-endian standart: `Day/Month[optionnal /Year]`
+ Dates and durations are separated by `-` and `+` allowing you to substract and add them
+ Dates must have at least days and month specified, by default the year is `baseYear` (see config.py)
+ Days must end with `d` (for instance `44d` or `22 d`)
+ Months must end with `m`
+ You can't add or substract years (if you really want it, I'll add that feature but come on...)
+ You may use operators `/` and `*` between days (or months) like `22*3d` or `44/2d` or `33/4*55m`
 + (For now) You can't use `+` or `-` between days, only between dates (example: `44d+3m-2*3d + 1/11/1` is ok, `44+3d` is not (what unit is 44 of ?))

Usage
-------
oddCalendar will always display two results: 
+ The date given by adding days/months to another date (or the date 0 if nothing precised)
+ The difference of days (if two dates werent precised, the number of days between the date and year 0)

Examples:
+ `1/1/1111 + 33d + 2m` will show the date 33 days and 2 months from 1/1/1111 and what it means in term of days
+ `1/1/11 - 1/11/1111` will show the date number of days/month/years between that date, and that time gap just in days
+ `33d + 444m` will show the number of days/months/years that this duration represents, and that duration in days

You may have noticed that despite the explaination is different, the calculation is strictly identical, the program handles dates as days spent between the aforementionned and year 0, hence allowing you to add and substract time and other dates from it (wether it makes sense or not).

Notes
-------
This program is `ledit` friendly
