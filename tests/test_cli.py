import pytest
from src.cli.main import main, create_parser


def test_version_flag():
    exit_code = main(['--version'])
    assert exit_code == 0


def test_help_flag():
    exit_code = main(['--help'])
    assert exit_code == 0


def test_no_args():
    exit_code = main([])
    assert exit_code == 0


def test_unknown_command():
    exit_code = main(['unknown'])
    assert exit_code == 1


def test_analyze_command_without_ollama():
    exit_code = main(['analyze'])
    #this will fail because ollama check will fail
    assert exit_code == 1


def test_parser_creation():
    parser = create_parser()
    assert parser.prog == 'cs'


def test_verbose_flag():
    parser = create_parser()
    args = parser.parse_args(['--verbose', 'analyze'])
    assert args.verbose is True


def test_help_command():
    exit_code = main(['help'])
    assert exit_code == 0

def test_version_command():
    exit_code = main(['version'])
    assert exit_code == 0

def test_commit_command_without_ollama():
    exit_code = main(['commit'])
    assert exit_code == 1
