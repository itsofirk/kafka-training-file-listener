class FileListenerException(Exception):
    pass


class KafkaError(FileListenerException):
    pass


class KafkaConnectionError(KafkaError):
    pass
