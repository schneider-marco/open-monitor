import logging

class ColoredFormatter(logging.Formatter):
    # ANSI escape sequences for colors
    COLOR_CODES = {
        'DEBUG': '\033[94m',     # Blue
        'INFO': '\033[92m',      # Green
        'WARNING': '\033[93m',   # Yellow
        'ERROR': '\033[91m',     # Red
        'CRITICAL': '\033[95m',  # Magenta
    }
    RESET_CODE = '\033[0m'

    def format(self, record):
        # Format log with color based on level, including time
        log_fmt = f"{self.COLOR_CODES.get(record.levelname, '')}%(asctime)s - %(levelname)s: %(message)s{self.RESET_CODE}"
        formatter = logging.Formatter(log_fmt, datefmt='%Y-%m-%d %H:%M:%S')
        return formatter.format(record)

# Set up the global logger
logger = logging.getLogger("global_logger")
logger.setLevel(logging.DEBUG)

# Check if the logger already has handlers to avoid duplicate handlers
if not logger.handlers:
    # Create console handler with color support
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # Set color formatter for console
    console_handler.setFormatter(ColoredFormatter())

    # Add the handler to the logger
    logger.addHandler(console_handler)
