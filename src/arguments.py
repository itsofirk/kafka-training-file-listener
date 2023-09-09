from file_listener.exceptions import FileListenerException
import os

import argparse


def directory(_arg):
    if not os.path.exists(_arg):
        raise FileListenerException("Provided path does not seem to exist.")
    if not os.path.isdir(_arg):
        raise FileListenerException("Provided path does not seem to be a directory.")
    return _arg


def kafka_host(_arg):
    parts = _arg.split(':')
    if not len(parts) == 2 or ' ' in _arg:
        raise FileListenerException("Provided kafka address is not in the correct format (host:port).")
    if not parts[1].isdigit() or 1 > int(parts[1]) or int(parts[1]) > 65535:
        raise FileListenerException("Kafka port must be a number.")
    return _arg


parser = argparse.ArgumentParser(
    prog='File Listener',
    description='File Listener listens for new files in a directory and alerts about each file to an '
                'extension-specific topic'
)

parser.add_argument('-d', '--directory', type=directory, help='The directory to listen to', required=True)
parser.add_argument('-k', '--kafka', type=kafka_host, nargs='+', metavar='hostname:port',
                    help='kafka address to send messages into', required=True)
parser.add_argument('-t', '--topic', default='fl', metavar='prefix',
                    help='specify a prefix for the kafka topics: prefix-jpeg, prefix-pdf (default: fl)', )
