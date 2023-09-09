import logging
from arguments import parser
from file_listener import FileListener

logger = logging.getLogger('file_listener')


if __name__ == '__main__':
    logger.info("File Listener initializing!")
    args = parser.parse_args()
    listener = FileListener(args.directory, args.kafka, args.topic, ignore_existing=False)
    listener.watch_directory()
    logger.info("File Listener exits!")
