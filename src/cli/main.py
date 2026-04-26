import sys
import argparse
from typing import Dict, Type, Optional, List

from src.cli.__version__ import VERSION_STRING
from src.cli.commands.base import BaseCommand, HelpCommand, VersionCommand
from src.cli.commands.analyze import AnalyzeCommand
from src.cli.commands.commit import CommitCommand
from src.cli.llm.ollama import OllamaClient
from src.cli.utils.logger import Logger


COMMANDS: Dict[str, Type[BaseCommand]] = {
    'analyze': AnalyzeCommand,
    'commit': CommitCommand,
    'help': HelpCommand,
    'version': VersionCommand,
}


def create_parser() -> argparse.ArgumentParser:
    """returns: argument parser configured for cli"""
    parser = argparse.ArgumentParser(
        prog='cs',
        description='CommitSense: AI-powered developer companion',
        add_help=False    #handeling this the manual way
    )

    # global options
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )

    parser.add_argument(
        '--version',
        action='store_true',
        help='Show version information'
    )

    parser.add_argument(
        '-h', '--help',
        action='store_true',
        help='Show help information'
    )

    parser.add_argument(
        '--ollama-url',
        type=str,
        default=OllamaClient.DEFAULT_URL,
        help=f'Ollama server URL (default: {OllamaClient.DEFAULT_URL})'
    )

    # subparsers for commands
    subparsers = parser.add_subparsers(
        dest='command',
        help='Command to run'
    )

    # Register all commands
    for cmd_name, cmd_class in COMMANDS.items():
        if cmd_name in ['help', 'version']:
            continue  # handle separately

        sub = subparsers.add_parser(
            cmd_name,
            help=cmd_class.description,
            add_help=False
        )
        sub.add_argument('-h', '--help', action='store_true')
        cmd_class.add_args(sub)

    return parser


def verify_ollama(ollama_url: str, logger: Logger) -> bool:
    """args:ollama_url: url of Ollama server
        logger: logger instance
    returns: true if working, False otherwise"""
    client = OllamaClient(base_url=ollama_url)

    if not client.health_check():
        logger.error(
            f"Ollama not running or model not found.\n"
            f"  URL: {ollama_url}\n"
            f"  Model: {client.DEFAULT_MODEL}\n\n"
            f"To start Ollama, run:\n"
            f"  ollama run {client.DEFAULT_MODEL}"
        )
        return False

    return True


def main(argv: Optional[List[str]] = None) -> int:
    """args:argv: command-line arguments (if None, uses sys.argv[1:])
    returns: exit code"""
    parser = create_parser()
    if argv is None:
        argv = sys.argv[1:]
    if not argv:
        parser.print_help()
        return 0
    # parse arguments
    args = parser.parse_args(argv)
    # initialize logger
    logger = Logger(verbose=args.verbose)
    # handle global flags
    if args.version:
        print(VERSION_STRING)
        return 0
    if args.help or not args.command:
        parser.print_help()
        return 0
    # get command
    cmd_class = COMMANDS.get(args.command)
    if not cmd_class:
        logger.error(f"Unknown command: {args.command}")
        parser.print_help()
        return 1

    try:
        # handle help for specific commands
        if hasattr(args, 'help') and args.help:
            if cmd_class.help_text:
                print(cmd_class.help_text)
            return 0

        # verify ollama is running 
        if args.command not in ['help', 'version']:
            if not verify_ollama(args.ollama_url, logger):
                return 1

        # create and execute command
        command = cmd_class()
        exit_code = command.execute(args) 
        return exit_code

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


def cli_entry_point() -> None:
    exit_code = main()
    sys.exit(exit_code)


if __name__ == '__main__':
    cli_entry_point()
