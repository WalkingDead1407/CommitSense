import sys
from enum import Enum


class LogLevel(Enum):
    """Log level constants."""
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3


class Logger:

    def __init__(self, verbose: bool = False):
        """args:verbose: if true, print debug message"""
        self.verbose = verbose
        self.min_level = LogLevel.DEBUG if verbose else LogLevel.INFO

    def debug(self, message: str) -> None:
        """print debug message (verbose mode only).
        args: message: debug message to print"""
        if self.verbose:
            print(f"[DEBUG] {message}", file=sys.stderr)

    def info(self, message: str) -> None:
        if self.min_level <= LogLevel.INFO:
            print(f"[INFO] {message}", file=sys.stderr)

    def warning(self, message: str) -> None:
        if self.min_level <= LogLevel.WARNING:
            print(f"[WARNING] {message}", file=sys.stderr)

    def error(self, message: str) -> None:
        print(f"[ERROR] {message}", file=sys.stderr)

    def success(self, message: str) -> None:
        print(f"[SUCCESS] {message}")
