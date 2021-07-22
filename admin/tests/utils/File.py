import io
import os
from pathlib import Path

from PIL import Image

from PlantApp import settings


# Create Page plant model
def removeAllImages():
    path = str(Path(__file__).parent.parent.parent.parent) + (settings.MEDIA_URL + 'images')
    if Path(path).is_dir():
        os.chmod(path, 0o777)
        files = os.listdir(path)
        for file in files:
            print(path + '/' + file)
            os.remove(path + '/' + file)
        os.rmdir(path)


def generateImage():
    file = io.BytesIO()
    image = Image.new("RGBA", size=(50, 50), color=(256, 0, 0))
    image.save(file, "png")
    file.seek(0)
    file.name = "images/test.png"
    return file
