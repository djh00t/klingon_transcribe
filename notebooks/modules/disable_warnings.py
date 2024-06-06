import warnings
import logging
import contextlib
import os
import sys

# Ensure install_klingon_logtools is run first
from .utils import install_klingon_logtools

# Import the LogTools class after ensuring it's installed
from klingon_tools import LogTools

def disable_warnings_function():
    warnings.filterwarnings("ignore", category=UserWarning, message=".*set_audio_backend has been deprecated.*")

@LogTools.method_state(name="Disable Warnings")
def disable_warnings():
    disable_warnings_function()
    configure_logging()

# Function to configure logging
def configure_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.ERROR)  # Suppress lower-severity messages globally

    # Optionally, you can suppress specific loggers if you know their names
    specific_loggers = [
        "pytorch_lightning",  # Example logger name, change as needed
        "whisperx",           # Example logger name, change as needed
        "pyannote.audio",     # Example logger name, change as needed
    ]

    for log_name in specific_loggers:
        specific_logger = logging.getLogger(log_name)
        specific_logger.setLevel(logging.CRITICAL)  # Suppress specific log messages

    # Suppress specific unwanted log messages by creating a custom handler
    class SuppressLoggingHandler(logging.Handler):
        def emit(self, record):
            if "Lightning automatically upgraded your loaded checkpoint" in record.msg or \
                "No language specified" in record.msg or \
                "Model was trained with pyannote.audio" in record.msg or \
                "Model was trained with torch" in record.msg:
                return
            # Optionally, you can log other messages if needed
            print(self.format(record))

    handler = SuppressLoggingHandler()
    handler.setLevel(logging.ERROR)  # Only log ERROR and CRITICAL messages

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

# Utility function to suppress stderr
@contextlib.contextmanager
def suppress_stderr():
    stderr_fileno = sys.stderr.fileno()
    with open(os.devnull, 'w') as devnull:
        old_stderr = os.dup(stderr_fileno)
        os.dup2(devnull.fileno(), stderr_fileno)
        try:
            yield
        finally:
            os.dup2(old_stderr, stderr_fileno)

# Run the function on import
disable_warnings()
