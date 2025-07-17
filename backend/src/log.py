import logging


def configure_logging(level=logging.DEBUG):
    logging.basicConfig(
        level=level,
        datefmt="%d-%m-%Y %H:%M:%S",
        format="[%(asctime)s.%(msecs)03d] %(module)s:%(lineno)d %(levelname)-7s - %(message)s"
    )


logger = logging.getLogger(__name__)
configure_logging()
