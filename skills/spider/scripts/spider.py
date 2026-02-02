#!/usr/bin/env python3
"""
Spider Validator - Main Entry Point

This is a thin wrapper that imports from the modular spider package.
For backward compatibility, all functions are re-exported at module level.

Legacy monolithic implementation preserved in legacy.py.
"""

# Re-export everything from the spider package for backward compatibility
from spider import *
from spider import __all__

# CLI entry point
if __name__ == "__main__":
    from spider import main
    raise SystemExit(main())
