from abc import ABC, abstractmethod
from argparse import ArgumentParser, Namespace
from typing import Optional


class BaseCommand(ABC):      #all cli commands inherit this base class
    name: str
    description: str
    help_text: Optional[str] = None

    def __init__(self):
        pass

    @classmethod
    def add_args(cls, parser: ArgumentParser) -> None:     # add command-specific arguments to the parser
        pass
    @abstractmethod
    def execute(self, args: Namespace) -> int:
        """args:Parsed arguments from argparse
        returns: exit code (0 = success, 1+ = error)"""
        pass


class HelpCommand(BaseCommand):       #built-in help command
    name = "help"
    description = "Show help information"
    def execute(self, args: Namespace) -> int:
        print("""
CommitSense: AI-powered developer companion

Usage:
  cs <command> [options]

Commands:
  fix                 Analyze errors and suggest fixes
  commit              Generate meaningful commit messages
  triage              Auto-label and assign PRs
  config              Manage configuration
  version             Show version information
  help                Show this help message

Examples:
  cs fix < error.log >
  python app.py 2>&1 | cs fix
  cs commit
  cs triage --pr 42

To get help on a specific command:
  cs <command> --help
        """)
        return 0


class VersionCommand(BaseCommand):

    name = "version"
    description = "Show version information"

    def execute(self, args: Namespace) -> int:
        from cli.__version__ import VERSION_STRING
        print(VERSION_STRING)
        return 0
