import torch
import logging

class GPUTools:
    # Function to determine the best available device
    def get_best_device():
        if torch.cuda.is_available():
            logging.info("Using CUDA")
            return "cuda"
        elif torch.backends.mps.is_available():
            logging.info("Using MPS")
            return "mps"
        else:
            logging.info("Using CPU")
            return "cpu"

class LoggingTools:
    # Define logger which manages all logging so that it is in syslog format
    # showing date, time, log level, method and message.
    def get_logger():
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        return logger