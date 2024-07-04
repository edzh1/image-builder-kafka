import json
from random import choice

from kafka import KafkaConsumer
from kafka.structs import TopicPartition, OffsetAndMetadata
from concurrent.futures import ThreadPoolExecutor
from .image_edit import blur, compress

number_of_threads = 4
topic_name = "compress"

consumer = KafkaConsumer(
    topic_name,
    group_id="compress_group",
    bootstrap_servers=["kafka:9092"],
    auto_offset_reset="earliest",
    enable_auto_commit=False,
)


def process_job(kafka_message, topic_offset):
    message = json.loads(kafka_message.value.decode("utf-8"))
    print(message["action"])

    is_broken = choice([True, False])
    if is_broken:
        return None

    if message["action"] == "blur":
        blur(f"/app/uploads/{message['file_url']}")

    elif message["action"] == "compress":
        compress(f"/app/uploads/{message['file_url']}")

    consumer.commit(offsets=topic_offset)


def run():
    print("run")
    for kafka_message in consumer:
        print(kafka_message)
        topic_partition = TopicPartition(topic_name, kafka_message.partition)
        offset = OffsetAndMetadata(kafka_message.offset + 1, None)
        topic_offset = {topic_partition: offset}

        executor = ThreadPoolExecutor(max_workers=number_of_threads)
        executor.submit(process_job, kafka_message, topic_offset)
