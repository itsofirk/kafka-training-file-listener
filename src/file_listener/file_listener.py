import base64
import os
import logging

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import atexit
from io import TextIOWrapper
from pathlib import Path

from .kafka_producer import KafkaProducer

logger = logging.getLogger(__name__)

APPDATA_NAME = 'FileListener'


class FileListener:
    def __init__(self, directory, kafka_addresses, topic_prefix, ignore_existing=True, recursive=False):
        self.target = directory
        self.kafka = KafkaProducer(kafka_addresses, topic_prefix)
        self.ignore_existing = ignore_existing
        self.recursive = recursive

        self.processed_file_path = self.get_appdata_file()
        self.processed_files = self.load_processed_files()
        self._fd: TextIOWrapper = None
        atexit.register(self.__close_file_descriptor__)

    def get_appdata_file(self):
        filename = base64.b64encode(bytes(self.target, 'utf-8')).decode('utf-8')
        appdata_path = Path(os.getenv('APPDATA'), APPDATA_NAME, filename)
        os.makedirs(appdata_path.parent, exist_ok=True)
        return appdata_path

    def load_processed_files(self):
        if self.ignore_existing:
            return set()
        if os.path.exists(self.processed_file_path):
            with open(self.processed_file_path, 'r') as file:
                return set(file.read().splitlines())

    @property
    def file_descriptor(self):
        if self._fd is None or self._fd.closed:
            self._fd = open(self.processed_file_path, 'a')
        return self._fd

    def mark_file_as_processed(self, file_path):
        self.processed_files.add(file_path)
        self.file_descriptor.write(f'{file_path}\n')

    def on_file_created(self, event):
        file_path = event.src_path
        if file_path not in self.processed_files:
            logger.info(f"New file created: {file_path}")
            # Process the file here
            # ...

            # Mark the file as processed
            self.mark_file_as_processed(file_path)

    def watch_directory(self):
        logger.info(f"Starts listening to new file events in {self.target} (press Ctrl+C to quit)...")

        event_handler = FileSystemEventHandler()
        event_handler.on_created = self.on_file_created

        observer = Observer()
        observer.schedule(event_handler, path=self.target, recursive=self.recursive)
        observer.start()
        try:
            while observer.is_alive():
                observer.join(1)
        finally:
            observer.stop()
            observer.join()

    def __close_file_descriptor__(self):
        if self._fd is not None:
            self._fd.close()
