#####################################################
##  Alternian Calendar V2.0                        ##
##    by Abraxa, Leksee, Sollux, Nathan and more.  ##
##                                                 ##
## Enjoy the shitshow, fellow code-reading person. ##
#####################################################

#################
## [NOTES] Code Monkey Notes and Other Things
#################
## Time is considered to have "started being a thing" at the epoch (Jan 1, 1970 00:00:00 UTC) and this calendar isn't meant for times before that.
## You can figure that out if you want, but I'm not doing it here.
## However, for synchrosity with Earth Years, the Alternian calendar starts at (1970 years worth of sweeps, aka 912) instead of Sweep 0.
## Also, this doesn't deal with Alternian timezones- Alternian times are calculated from UTC, though.
## Earth-Specific Assumptions:
## > Each day is exactly 24*60*60 seconds, none of this leap-second bullshittery.
## Alternia-Specific Assumptions:
## > Date stuff is counting from 0, and then increased to 1 for the user (i.e. there is a 0th day internally)

## [IMPORTS]
import time
from datetime import datetime
import math

## [CONSTANTS]
# Provided the fundementals of time don't drastically change, these won't change.

SECONDSPERMINUTE = 60                        # [60]        60 seconds in a minute.
SECONDSPERHOUR   = (SECONDSPERMINUTE * 60)   # [3600]      60 minutes in an hour.
SECONDSPERBP     = (SECONDSPERHOUR * 52 )    # [187200]    52 hours in a BP.
SECONDSPERSWEEP  = (SECONDSPERBP * 364)      # [68140800]  Due to Time Shenanigans, there are 364 days per sweep, and an anti-leap-sweep every 10 sweeps
SWEEPOFFSET      = 912                       # In years. Note pre-epoch times aren't Officially Supported and are likely kind of innaccurate.

# Dict of each month, and relevant info related to them.
alternian_months = {
    "1" : {
        "monthLong"   : "1st dim season",
        "monthShort"  : "1di",
        "monthLength" : 16,
        "monthSeason" : "spring",
        "startDate"   : 0
    },
    "2" : {
        "monthLong"   : "1st dim season's equinox",
        "monthShort"  : "1iE",
        "monthLength" : 15,
        "monthSeason" : "summer",
        "startDate"   : 16
    },
    "3" : {
        "monthLong"   : "1st dark season",
        "monthShort"  : "1da",
        "monthLength" : 15,
        "monthSeason" : "summer",
        "startDate"   : 31
    },
    "4" : {
        "monthLong"   : "1st dark season's equinox",
        "monthShort"  : "1aE",
        "monthLength" : 15,
        "monthSeason" : "autumn",
        "startDate"   : 46
    },
    "5" : {
        "monthLong"   : "2nd dim season",
        "monthShort"  : "2di",
        "monthLength" : 15,
        "monthSeason" : "autumn",
        "startDate"   : 61
    },
    "6" : {
        "monthLong"   : "2nd dim season's equinox",
        "monthShort"  : "2iE",
        "monthLength" : 15,
        "monthSeason" : "winter",
        "startDate"   : 76
    },
    "7" : {
        "monthLong"   : "2nd dark season",
        "monthShort"  : "2da",
        "monthLength" : 16,
        "monthSeason" : "winter",
        "startDate"   : 91
    }, 
    "8" : {
        "monthLong"   : "2nd dark season's equinox",
        "monthShort"  : "2aE",
        "monthLength" : 15,
        "monthSeason" : "spring",
        "startDate"   : 107
    },
    "9" : {
        "monthLong"   : "3rd dim season",
        "monthShort"  : "3di",
        "monthLength" : 15,
        "monthSeason" : "spring",
        "startDate"   : 122
    },
    "10" : {
        "monthLong"   : "3rd dim season's equinox",
        "monthShort"  : "3iE",
        "monthLength" : 15,
        "monthSeason" : "summer",
        "startDate"   : 137
    },
    "11" : {
        "monthLong"   : "3rd dark season",
        "monthShort"  : "3da",
        "monthLength" : 15,
        "monthSeason" : "summer",
        "startDate"   : 152
    },
    "12" : {
        "monthLong"   : "3rd dark season's equinox",
        "monthShort"  : "3aE",
        "monthLength" : 15,
        "monthSeason" : "autumn",
        "startDate"   : 167
    },
    "13" : {
        "monthLong"   : "4th dim season",
        "monthShort"  : "4di",
        "monthLength" : 16,
        "monthSeason" : "autumn",
        "startDate"   : 182
    },
    "14" : {
        "monthLong"   : "4th dim season's equinox",
        "monthShort"  : "4iE",
        "monthLength" : 15,
        "monthSeason" : "winter",
        "startDate"   : 198
    },
    "15" : {
        "monthLong"   : "4th dark season",
        "monthShort"  : "4da",
        "monthLength" : 15,
        "monthSeason" : "winter",
        "startDate"   : 213
    },
    "16" : {
        "monthLong"   : "4th dark season's equinox",
        "monthShort"  : "4aE",
        "monthLength" : 15,
        "monthSeason" : "spring",
        "startDate"   : 228
    },
    "17" : {
        "monthLong"   : "5th dim season",
        "monthShort"  : "5di",
        "monthLength" : 15,
        "monthSeason" : "spring",
        "startDate"   : 243
    },
    "18" : {
        "monthLong"   : "5th dim season's equinox",
        "monthShort"  : "5iE",
        "monthLength" : 15,
        "monthSeason" : "summer",
        "startDate"   : 258
    },
    "19" : {
        "monthLong"   : "5th dark season",
        "monthShort"  : "5da",
        "monthLength" : 16,
        "monthSeason" : "summer",
        "startDate"   : 273
    },
    "20" : {
        "monthLong"   : "5th dark season's equinox",
        "monthShort"  : "5aE",
        "monthLength" : 15,
        "monthSeason" : "autumn",
        "startDate"   : 289
    },
    "21" : {
        "monthLong"   : "6th dim season",
        "monthShort"  : "6di",
        "monthLength" : 15,
        "monthSeason" : "autumn",
        "startDate"   : 304
    },
    "22" : {
        "monthLong"   : "6th dim season's equinox",
        "monthShort"  : "6iE",
        "monthLength" : 15,
        "monthSeason" : "winter",
        "startDate"   : 319
    },
    "23" : {
        "monthLong"   : "6th dark season",
        "monthShort"  : "6da",
        "monthLength" : 15,
        "monthSeason" : "winter",
        "startDate"   : 334
    },
    "24" : {
        "monthLong"   : "6th dark season's equinox",
        "monthShort"  : "6aE",
        "monthLength" : 15,
        "monthSeason" : "spring",
        "startDate"   : 349
    }
}


## [VARIABLES]
# These, however, *do* change. 
secondsSinceEpoch = time.time()                                           # Seconds since 1/1/1970 - surprisingly useful.

currentSweep            = (secondsSinceEpoch/SECONDSPERSWEEP)             # Outputs year as a float (use math.floor for just the year)
currentSweepAdjusted    = math.floor(currentSweep + SWEEPOFFSET)          # Adds the sweeps between 1/1/0 and 1/1/1970 to the current sweep number
currentSweepPercentage  = (currentSweep - math.floor(currentSweep))       # Outputs something like 0.94
currentSweepSeconds     = (currentSweepPercentage * SECONDSPERSWEEP)      # Seconds since 1/1di/current sweep
currentSweepBP          = (currentSweepSeconds / SECONDSPERBP )           # Days elapsed this sweep

for month in alternian_months.keys():                                     # for each month in a sweep
    for key, value in alternian_months[month].items():                    # for each thing inside each month
        if key == "startDate":
            if currentSweepBP >= value:                                   # This sets currentMonth, until currentSweepBP occurs before the start of the month
                currentMonth = int(month)                                 # TODO: find a less hacky way of doing this? maybe?

currentMonthLong   = alternian_months[str(currentMonth)]['monthLong']     # Gets the relevant items from the alternian_months dict
currentMonthShort  = alternian_months[str(currentMonth)]['monthShort']    # Each of these are used for different things
currentMonthLength = alternian_months[str(currentMonth)]['monthLength']   # And can easily be added to, because dicts are nice
currentSeason      = alternian_months[str(currentMonth)]['monthSeason']      
startDate          = alternian_months[str(currentMonth)]['startDate']             

if (currentSweepBP == 16) and (currentSweepAdjusted % 10 == 0):           # Every 10 years, an anti-leap-sweep occurs
    print("[LOG] Happy anti-leap day! Date adjusted to 1/1iE.")           # This code runs to ensure 16/1di/xx0 doesn't happen
    currentMonth       = 2
    currentMonthLong   = "1st dim season's equinox"
    currentMonthShort  = "1iE"
    currentMonthLength = 15
    currentSeason      = "summer"
    startDate          = 16

currentMonthBP         = (currentSweepBP - startDate)                     # Outputs something like 252.32987
currentBPPercentage    = (currentMonthBP - math.floor(currentMonthBP))    # Outputs something like 0.38


currentBPSecondsTotal = SECONDSPERBP * currentBPPercentage  # Seconds elapsed today (total!)
currentBPMinutesTotal = currentBPSecondsTotal / 60          # Minutes elapsed today (total!)
currentBPHours   = currentBPMinutesTotal / 60               # Hours elapsed today

currentBPMinute  = (math.floor(currentBPMinutesTotal - (math.floor(currentBPHours) * 60)))        # Minutes elapsed in the current hour
currentBPSecond  = (math.floor(currentBPSecondsTotal - (math.floor(currentBPMinutesTotal) * 60))) # Seconds elapsed in the current minute

# Formatting stuff

dd = str(math.floor(currentMonthBP)).zfill(2)               # These have prepended 0's when needed
mm = str(currentMonthShort)                                 # and are easy-to-read shorthand as a bonus.
sw = str(math.floor(currentSweep) + SWEEPOFFSET).zfill(3)
hh = str(math.floor(currentBPHours)).zfill(2)
mi = str(currentBPMinute).zfill(2)
ss = str(currentBPSecond).zfill(2)

currentTime  = datetime.now()
earthTime    = currentTime.strftime("%H:%M:%S  %d/%m/%Y") # 11:31:53  24/08/2000 (below is in comparable format)
alterniaTime = (str(hh) + ":" + str(mi) + ":" + str(ss) + "  " + str(dd) + "/" + str(mm) + "/" + str(sw))

## Main code the user sees ig

print("╒═╣ Date Stats ╠═══════════════════╣ " + alterniaTime + " ╠═╕")
print("│ Sweep          Month                Day                   │")
print("│ Number: " + str(sw) + "    Number: " + str(currentMonth).zfill(2) + " (" + str(mm) +  ")     Number: " + str(math.floor(currentSweepBP)).zfill(2) + " (" + str(dd) + ")      |")
print("│ %: " + str(round(currentSweepPercentage, 2)) + "        %: " + str(round((currentMonthBP / currentMonthLength), 2)) + "              %: " + str(round(currentBPPercentage, 2)) + "               │")
print("╘═══════════════════════════════════════════════════════════╛")
