import os, sys, logging, re
from datetime import datetime

BASE_OUTPUT_PATH = "LOOT/"
BASE_ERROR_PATH = "ERRORS/"
LOGGER = None
ORIGINAL_STDOUT = sys.stdout
ORIGINAL_STDERR = sys.stderr

class LoggerWriter:
    def __init__(self, level_func, stream):
        self.level_func = level_func
        self.stream = stream
        # Regex to match ANSI escape sequences for color codes when logging
        self.ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')

    def write(self, message):
        # Send the original message to the terminal while keeping the terminal colors
        self.stream.write(message)
        self.stream.flush()

        # For logging, clean each line and remove ANSI codes
        for line in message.rstrip().splitlines():
            if line.strip():  # Skip empty lines
                clean_line = self.ansi_escape.sub('', line)
                self.level_func(clean_line)

    def flush(self):
        self.stream.flush()

def create_logging_directories(path):
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

def init_logger():
    global LOGGER
    if LOGGER:  # Already initialized
        return LOGGER

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    logger = logging.getLogger("AWSRAID_Logger")
    logger.setLevel(logging.DEBUG)

    # Ensure directories exist
    create_logging_directories(BASE_OUTPUT_PATH)
    create_logging_directories(BASE_ERROR_PATH)

    # Handlers
    output_handler = logging.FileHandler(f"{BASE_OUTPUT_PATH}AWSRAID_Output.log", mode='w')
    output_handler.setLevel(logging.INFO)
    # Add filter so output handler ignores ERROR and above
    output_handler.addFilter(lambda record: record.levelno < logging.ERROR)

    error_handler = logging.FileHandler(f"{BASE_ERROR_PATH}{timestamp}_Errors.log")
    error_handler.setLevel(logging.ERROR)
    #error_formatter = logging.Formatter('%(asctime)s - %(message)s')
    #error_handler.setFormatter(error_formatter)

    logger.addHandler(output_handler)
    logger.addHandler(error_handler)

    return logger

def log_error(message):
    global LOGGER
    LOGGER = init_logger()
    LOGGER.error(message)

def log_output(message):
    global LOGGER
    LOGGER = init_logger()
    LOGGER.info(message)

# This function will intercept stdout and stderr and log them based on LoggerWriter class functions
# Text will still get printed to terminal
def enable_print_logging():
    global LOGGER
    LOGGER = init_logger()
    sys.stdout = LoggerWriter(LOGGER.info, ORIGINAL_STDOUT)
    sys.stderr = LoggerWriter(LOGGER.error, ORIGINAL_STDERR)