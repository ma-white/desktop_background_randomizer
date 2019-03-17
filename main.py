import ctypes
import time
from unsplash.api import Api
from unsplash.auth import Auth
import unsplash
import requests

client_id = "c0efab2e6baaafa10d16d0266dc28b9658f7668d5b2047c0d32a5994af91d26e"
client_secret = "73e6f202e8bbffdc4b3e6d9ef0646244e09b4d7867d30db659110b5454d51bbe"
redirect_uri = ""
code = ""

auth = Auth(client_id, client_secret, redirect_uri, code=code)
api = Api(auth)

def main():

    link = getRandomPic()
    downloadPic(link)


def getRandomPic():
    kwargs = {'w':1920,'h':1080,'query':'wallpapers'}
    randomPic = api.photo.random(**kwargs)
    picId = unsplash.models.Photo.__str__(randomPic[0])
    picId = picId[10 : len(picId) - 2]
    photoLink = api.photo.download(picId)
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
    

if __name__ == "__main__":
    main()