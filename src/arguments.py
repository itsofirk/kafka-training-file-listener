import argparse

parser = argparse.ArgumentParser(
    prog='File Listener',
    description='File Listener listens for new files in a directory and alerts about each file to an '
                'extension-specific topic'
)

parser.add_argument('-d', '--directory', help='The directory to listen to', required=True)
parser.add_argument('-k', '--kafka', metavar='hostname:port', help='kafka address to send messages into', required=True)
parser.add_argument('-t', '--topic', default='fl', metavar='prefix',
                    help='specify a prefix for the kafka topics: prefix-jpeg, prefix-pdf (default: fl)', )
