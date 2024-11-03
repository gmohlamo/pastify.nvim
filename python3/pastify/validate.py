from .type import Config


def validate_config(config: Config, logger, filetype: str) -> bool:
    c = config
    opts = c['opts']

    if filetype not in c["ft"]:
        logger(
            "Not in a filetype configured in config.ft",
            "WARN")

    if c is None:
        return False
    return True
