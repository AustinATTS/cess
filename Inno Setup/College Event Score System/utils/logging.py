import logging
import os

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", handlers=[logging.FileHandler(os.path.join("logs", "cess.log")), logging.StreamHandler()])
logger = logging.getLogger(__name__)