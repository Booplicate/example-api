"""
Program entry point
"""

import argparse
import os

import uvicorn


APP_NAME = "test_api.application:main_app"


def _parse_args():
    parser = argparse.ArgumentParser(prog="test_api", description="An example API")
    parser.add_argument("--host", default=None, help="server address")
    parser.add_argument("--port", default=None, type=int, help="server port")

    return parser.parse_args()

def _get_env_var(name: str):
    try:
        return os.environ[name]

    except KeyError as e:
        raise RuntimeError(f"Missing required enviroment variable: {e}") from None

def _get_host_port(args) -> tuple[str, int]:
    host = args.host if args.host is not None else _get_env_var("APP_HOST")
    port = args.port if args.port is not None else int(_get_env_var("APP_PORT"))
    return (host, port)

def main():
    """
    Entry point
    """
    args = _parse_args()
    host, port = _get_host_port(args)

    config = uvicorn.Config(APP_NAME, host=host, port=port)
    server = uvicorn.Server(config)
    server.run()


if __name__ == "__main__":
    main()
