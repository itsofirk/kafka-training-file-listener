import logging
from confluent_kafka import Producer
from confluent_kafka.cimpl import KafkaException

from .exceptions import KafkaConnectionError

logger = logging.getLogger(__name__)


class KafkaProducer:
    def __init__(self, addresses: list, topic_prefix=None):
        conf = {
            'bootstrap.servers': ','.join(addresses)
        }
        self.producer = Producer(conf, logger=logger)
        if not self.__is_alive__():
            raise KafkaConnectionError(f"Error connecting to Kafka brokers.")

    def __is_alive__(self):
        try:
            topics = self.producer.list_topics(timeout=5)
            logger.debug(f"Producer is connected")
            return True
        except KafkaException as e:
            return False

