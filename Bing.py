#!/usr/bin/python3
import os
import json
import datetime
from urllib import error, request
import codecs
import  time
import subprocess

SCRIPT = """/usr/bin/osascript<<END
tell application "Finder"
set desktop picture to POSIX file "%s"
end tell
END"""

zone = "en-US"
resolution = '1920x1080'
Dir =  "/Users/gpande2/Documents/BingWallPapers/"
Wallpaper_Name = "Today_wallpaper.jpg"


def main():
    i = 1
    while (i == 1):
        try:
            request.urlopen("https://www.google.co.in")
            print ("Checking network connectivity!!!")
        except error.URLError as e:
            time.sleep(5)
        else:
            print ("Connection Successfull!!")
            i = 0
            reader = codecs.getreader("utf-8")
            response = request.urlopen("http://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=" + zone)
            json_obj = json.load(reader(response))
            url = (json_obj['images'][0]['urlbase'])
            url = url = 'http://www.bing.com' + url + '_' + resolution + '.jpg'

            #create the Bing directory
            if not os.path.exists(Dir):
                os.makedirs(Dir)
            path = Dir + Wallpaper_Name


            if os.path.exists(path):
                today_date = datetime.datetime.now().strftime("%m/%d/%Y")
                file_date = time.strftime('%m/%d/%Y',time.gmtime(os.path.getatime(path)))
                if today_date == file_date:
                    print ("Already have the wallpaper for today")
                    setwallpaper(path)
                else:
                    print ("Downloading Bing wallpaper to %s" % path)
                    f = open(path,'wb')
                    bing_picture =  request.urlopen(url)
                    f.write(bing_picture.read())
                    setwallpaper(path)
            else:
                print ("Downloading Bing wallpaper to %s" % path)
                f = open(path,'wb')
                bing_picture = request.urlopen(url)
                f.write(bing_picture.read())
                setwallpaper(path)


def setwallpaper(path):
    print("setting as the desktop background")
    subprocess.Popen(SCRIPT % path, shell=True)



if __name__ == '__main__':
    main()

