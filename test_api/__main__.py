"""
Program entry point
"""

import argparse

import uvicorn

from . import database


APP_NAME = "test_api.application:main_app"


def _parse_args():
    parser = argparse.ArgumentParser(prog="test_api", description="An example API")
    parser.add_argument("host", help="server address")
    parser.add_argument("port", type=int, help="server address")

    return parser.parse_args()

def main():
    """
    Entry point
    """
    args = _parse_args()

    database.init()

    config = uvicorn.Config(APP_NAME, host=args.host, port=args.port)
    server = uvicorn.Server(config)
    server.run()


if __name__ == "__main__":
    main()
