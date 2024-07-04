import json
import os

from ninja import NinjaAPI, UploadedFile, Schema, Form, File
from kafka import KafkaProducer
from enum import Enum
from django.core.files.storage import FileSystemStorage
from django.conf import settings

PRIVATE_DIR = os.path.join(settings.BASE_DIR, "uploads")
fs = FileSystemStorage(location=PRIVATE_DIR)


class Action(str, Enum):
    COMPRESS = "compress"
    BLUR = "blur"


api = NinjaAPI()

producer = KafkaProducer(bootstrap_servers=["kafka:9092"])


class UploadIn(Schema):
    file: UploadedFile
    action: Action


@api.post("/upload")
def upload(request, file: UploadedFile = File(...), action: Action = Form(...)):
    filename = fs.save(file.name, file)

    producer.send(
        "compress",
        value=json.dumps({"file_url": f"{filename}", "action": action}).encode("utf-8"),
    )

    return {"name": filename}
