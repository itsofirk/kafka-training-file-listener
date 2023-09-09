import logging
from confluent_kafka import Producer

logger = logging.getLogger(__name__)


class KafkaProducer:
    def __init__(self, addresses: list, topic_prefix=None):
        conf = {
            'bootstrap.servers': ','.join(addresses)
        }
        self.client = Producer(conf, logger=logger)
