import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('safts.log'), logging.StreamHandler()],
)

# Define um logger que pode ser importado
logger = logging.getLogger(__name__)
