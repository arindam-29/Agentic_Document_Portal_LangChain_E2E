import logging
import os
from datetime import datetime
import structlog

class CustomLogger:
    def __init__(self, log_dir="logs"):
        # Ensure "logs" directory exsist:
        self.log_dir=os.path.join(os.getcwd(), log_dir)
        os.makedirs(self.log_dir, exist_ok=True)

        # Create timestamped log file name format:
        log_file=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
        self.log_file_path=os.path.join(self.log_dir, log_file)

    def get_logger(self, name=__file__):
        logger_name = os.path.basename(name)

        # Config logging for file and console (JSON Format):
        file_handler = logging.FileHandler(self.log_file_path)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter("%(message)s")) # JSON Lines

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter("%(message)s"))

        logging.basicConfig(
            level=logging.INFO,
            format="%(message)s", #structlog JSON format
            handlers=[console_handler, file_handler]
        )

        # Config structlog for JSON structured logging:
        structlog.configure(
            processors=[
                structlog.processors.TimeStamper(fmt="iso", utc=True, key="timestamp"),
                structlog.processors.add_log_level,
                structlog.processors.EventRenamer(to="event"),
                structlog.processors.JSONRenderer()
            ],
            logger_factory=structlog.stdlib.LoggerFactory(),
            cache_logger_on_first_use=True,
        )

        return structlog.get_logger(logger_name)
    

if __name__=="__main__":
    logger=CustomLogger()
    logger=logger.get_logger(__file__)
    logger.info("Custome logger Testing..")
    logger.info("Test file uploaded", user_id=12345, filename="test.pdf")