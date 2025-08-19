import sys
import types
import pytest
from unittest import mock
from src.main import main
from src import main as main_module
from src import main as main_module

@pytest.fixture(autouse=True)
def patch_sys_exit():
    with mock.patch("sys.exit") as exit_mock:
        yield exit_mock

@pytest.fixture(autouse=True)
def patch_print():
    with mock.patch("builtins.print") as print_mock:
        yield print_mock

@pytest.fixture(autouse=True)
def patch_argparse_parse_args():
    with mock.patch("argparse.ArgumentParser.parse_args") as parse_args_mock:
        yield parse_args_mock

@pytest.fixture(autouse=True)
def patch_cli_and_cache(monkeypatch):
    cli_mock = types.SimpleNamespace()
    cli_mock.get_user_choice = mock.Mock(return_value="Kyiv")
    cli_mock.watch_mode = mock.Mock()
    cli_mock.fetch_and_display_weather = mock.Mock(return_value=True)
    cache_mock = types.SimpleNamespace()
    cache_mock.DEFAULT_TTL = 300
    monkeypatch.setattr("src.main.cli", cli_mock)
    monkeypatch.setattr("src.main.cache", cache_mock)
    return cli_mock, cache_mock

def test_main_default_args(patch_argparse_parse_args, patch_cli_and_cache):
    cli_mock, cache_mock = patch_cli_and_cache
    patch_argparse_parse_args.return_value = mock.Mock(
        city=None, watch=None, no_cache=False, ttl=cache_mock.DEFAULT_TTL
    )
    main()
    cli_mock.get_user_choice.assert_called_once()
    cli_mock.fetch_and_display_weather.assert_called_once_with(
        city="Kyiv", use_cache=True, ttl=cache_mock.DEFAULT_TTL
    )

def test_main_city_arg(patch_argparse_parse_args, patch_cli_and_cache):
    cli_mock, cache_mock = patch_cli_and_cache
    patch_argparse_parse_args.return_value = mock.Mock(
        city="London", watch=None, no_cache=False, ttl=cache_mock.DEFAULT_TTL
    )
    main()
    cli_mock.get_user_choice.assert_not_called()
    cli_mock.fetch_and_display_weather.assert_called_once_with(
        city="London", use_cache=True, ttl=cache_mock.DEFAULT_TTL
    )

def test_main_no_cache(patch_argparse_parse_args, patch_cli_and_cache):
    cli_mock, cache_mock = patch_cli_and_cache
    patch_argparse_parse_args.return_value = mock.Mock(
        city="Paris", watch=None, no_cache=True, ttl=cache_mock.DEFAULT_TTL
    )
    main()
    cli_mock.fetch_and_display_weather.assert_called_once_with(
        city="Paris", use_cache=False, ttl=cache_mock.DEFAULT_TTL
    )

def test_main_watch_mode_with_city(patch_argparse_parse_args, patch_cli_and_cache):
    cli_mock, cache_mock = patch_cli_and_cache
    patch_argparse_parse_args.return_value = mock.Mock(
        city="Berlin", watch=60, no_cache=False, ttl=cache_mock.DEFAULT_TTL
    )
    main()
    cli_mock.watch_mode.assert_called_once_with(
        city="Berlin", interval=60, use_cache=True, ttl=cache_mock.DEFAULT_TTL
    )

def test_main_watch_mode_without_city(patch_argparse_parse_args, patch_cli_and_cache):
    cli_mock, cache_mock = patch_cli_and_cache
    patch_argparse_parse_args.return_value = mock.Mock(
        city=None, watch=120, no_cache=False, ttl=cache_mock.DEFAULT_TTL
    )
    main()
    cli_mock.get_user_choice.assert_called_once()
    cli_mock.watch_mode.assert_called_once_with(
        city="Kyiv", interval=120, use_cache=True, ttl=cache_mock.DEFAULT_TTL
    )

def test_main_fetch_and_display_weather_failure(patch_argparse_parse_args, patch_cli_and_cache, patch_sys_exit):
    cli_mock, cache_mock = patch_cli_and_cache
    cli_mock.fetch_and_display_weather.return_value = False
    patch_argparse_parse_args.return_value = mock.Mock(
        city="Rome", watch=None, no_cache=False, ttl=cache_mock.DEFAULT_TTL
    )
    main()
    patch_sys_exit.assert_called_once_with(1)

def test_main_keyboard_interrupt(monkeypatch, patch_print, patch_sys_exit):
    def raise_keyboard_interrupt():
        raise KeyboardInterrupt()
    monkeypatch.setattr("src.main.main", raise_keyboard_interrupt)
    main_module.__name__ = "__main__"
    with pytest.raises(KeyboardInterrupt):
        raise_keyboard_interrupt()

def test_main_unhandled_exception(monkeypatch, patch_print, patch_sys_exit):
    def raise_exception():
        raise RuntimeError("fail!")
    monkeypatch.setattr("src.main.main", raise_exception)
    main_module.__name__ = "__main__"
    with pytest.raises(RuntimeError):
        raise_exception()