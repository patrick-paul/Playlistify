#!/usr/bin/env python3
"""
Entry point for Playlistfy when run as a module
"""
from .cli import CLI

def main():
    cli = CLI()
    cli.run()

if __name__ == "__main__":
    main()