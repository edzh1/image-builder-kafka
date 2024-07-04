from time import sleep

from wand.exceptions import BlobError
from wand.image import Image
from wand.resource import limits
import os

limits["memory"] = 1024 * 1024 * 2000


def compress(path: str):
    print("compress start")
    file_name, file_extension = os.path.splitext(path)
    try:
        with Image(filename=path) as img:
            with img.clone() as i:
                i.resize(int(i.width * 0.1), int(i.height * 0.1))
                i.save(filename=f"{file_name}-compressed.{file_extension}")

        print("compress done")
    except (FileNotFoundError, BlobError):
        print("file not found, skipping")


def blur(path: str):
    print("blur start")
    sleep(60)
    file_name, file_extension = os.path.splitext(path)
    try:
        with Image(filename=path) as img:
            img.gaussian_blur(sigma=10)
            img.save(filename=f"{file_name}-blured.{file_extension}")

        print("blur done")
    except (FileNotFoundError, BlobError):
        print("file not found, skipping")
