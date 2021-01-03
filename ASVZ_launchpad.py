import ASVZ_bot
import datetime
import time
import sys


class wishes:
    def __init__(self):
        self.path = "/home/ec2-user/ASVZ_bot/ASVZ_bot/wishlist.txt"
        #self.path = "wishlist.txt"
        wishfile = open(self.path)
        temp = wishfile.read().split('\n')
        self.wishes = {wish.split(' ')[0]: wish.split(' ')[1] for wish in temp}
    def update(self):
        wishfile = open(self.path)
        temp = wishfile.read().split('\n')
        self.wishes = {wish.split(' ')[0]: wish.split(' ')[1] for wish in temp}
        print("Updated wishlist!")


def translate_day_to_german(day):
    if(day == "Monday"):
        return "Montag"
    if(day == "Tuesday"):
        return "Dienstag"
    if(day == "Wednesday"):
        return "Mittwoch"
    if(day == "Thursday"):
        return "Donnerstag"
    if(day == "Friday"):
        return "Freitag"
    if(day == "Saturday"):
        return "Samstag"
    if(day == "Sunday"):
        return "Sonntag"


one_minute = datetime.timedelta(minutes=1)
one_day = datetime.timedelta(hours=24)
wishlist = wishes()
# read in eth login as prompt
eth_username = sys.argv[1]
eth_password = sys.argv[2]

time_now = datetime.datetime.now()
time_tomorrow = time_now + one_day
current_day = translate_day_to_german(time_now.strftime("%A"))
tomorrow = translate_day_to_german(time_tomorrow.strftime("%A"))
print("\n Bot woke up at "+  time_now.strftime("%H:%M") +" on " + current_day)
print("Now waiting for " + wishlist.wishes[tomorrow] + " -one_minute to reserve slot on " + tomorrow)


while True:
    time_now = datetime.datetime.now()
    time_now_forward = time_now + one_minute
    current_time = time_now.strftime("%H:%M")

    # check if time and day are on wishlist -> start bot to reserve slot
    if ( wishlist.wishes[tomorrow] == time_now_forward.strftime("%H:%M") ):
        wishlist.update()
        print( "\n" + wishlist.wishes[tomorrow] + " == " + time_now_forward.strftime("%H:%M") + " on " + current_day + " at " + time_now.strftime("%H:%M"))
        print("Bot launchin to reserve...")
        bot = ASVZ_bot.ASVZ_bot(tomorrow,wishlist.wishes[tomorrow],eth_username,eth_password)
        bot.reserve()
        print( "Bot has tried to reserve and has come back...\n")

    if (current_time == "23:00"):
        print("Bot goes to sleep... at " + current_time)
        sys.exit()

    time.sleep(0.5)