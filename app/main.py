"""Application entry point."""

from app.config.logging import setup_logging, get_logger
from app.config.di_container import Container
from app.config.settings import settings


def main() -> None:
    setup_logging()

    logger = get_logger(__name__)
    logger.info("Starting %s ...", settings.APP_NAME)

    container = Container()
    container.init_resources()
    logger.info("%s started successfully.", settings.APP_NAME)


if __name__ == "__main__":
    main()
