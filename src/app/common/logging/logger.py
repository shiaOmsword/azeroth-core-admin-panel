#logger.py
import logging
from rich.logging import RichHandler

def setup_logging(level: str = "INFO") -> None:

	rich_handler = RichHandler(
		rich_tracebacks=True,
		markup=True,
		show_time=True,
		show_level=True,
		show_path=True,
	)
	
	formatter = logging.Formatter("%(name)s | %(message)s")
	rich_handler.setFormatter(formatter)
	root_logger = logging.getLogger()
	root_logger.setLevel(getattr(logging, level.upper(), logging.INFO))
	root_logger.handlers.clear()
	root_logger.addHandler(rich_handler)