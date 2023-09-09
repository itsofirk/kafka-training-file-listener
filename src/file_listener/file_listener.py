from .kafka_producer import KafkaProducer


class FileListener:
    def __init__(self, directory, kafka_addresses, topic_prefix):
        self.kafka = KafkaProducer(kafka_addresses, topic_prefix)

    def listen(self):
        pass
