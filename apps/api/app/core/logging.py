import logging
import sys

def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format='{"time": "%(asctime)s", "level": "%(levelname)s", "module": "%(module)s", "message": "%(message)s"}',
        handlers=[logging.StreamHandler(sys.stdout)],
    )

logger = logging.getLogger("vapor.api")
