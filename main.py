import ctypes
import time
from unsplash.api import Api
from unsplash.auth import Auth
import unsplash
import requests
import schedule

#Setup for interfacing with unsplash API
client_id = "c0efab2e6baaafa10d16d0266dc28b9658f7668d5b2047c0d32a5994af91d26e"
client_secret = "73e6f202e8bbffdc4b3e6d9ef0646244e09b4d7867d30db659110b5454d51bbe"
redirect_uri = ""
code = ""

auth = Auth(client_id, client_secret, redirect_uri, code=code)
api = Api(auth)

def main():
    #Set schedule for when to set background
    schedule.every().monday.at("02:00").do(job)
    schedule.every().tuesday.at("02:00").do(job)
    schedule.every().wednesday.at("02:00").do(job)
    schedule.every().thursday.at("02:00").do(job)
    schedule.every().friday.at("02:00").do(job)
    schedule.every().saturday.at("02:00").do(job)
    schedule.every().sunday.at("02:00").do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)

def job():
    link = getRandomPic()
    downloadPic(link)
    setDesktopBackground()


def getRandomPic():
    #Ensure we grab a 1920 by 1080 image from the wallpapers collection
    kwargs = {'w':1920,'h':1080,'query':'wallpapers'}
    randomPic = api.photo.random(**kwargs)
    #Get the pic ID
    picId = unsplash.models.Photo.__str__(randomPic[0])
    picId = picId[10 : len(picId) - 2]
    #Get the download link
    photoLink = api.photo.download(picId)
    #Must add the client_id to the link so unsplash does not block the request
    photoLink = photoLink['url'] + client_id
    return photoLink

def downloadPic(photoLink):
    with open('background.jpg', 'wb') as handle:
        response = requests.get(photoLink, stream=True)

        if not response.ok:
            print(response)

        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)

def setDesktopBackground():
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER,0,"S:\Workspace\Coding\desktopBackgroundRandomizer\\background.jpg",0)

if __name__ == "__main__":
    main()