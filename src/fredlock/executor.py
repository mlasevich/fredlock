"""
External Command Executor

Runs the Specified Command, pass stdout/stderr
"""
import logging
import subprocess

from .utils import keyboard_interrupt_protection

log = logging.getLogger(__name__)


def execute(*command):
    """ Execute a command with args, return exit code"""

    with keyboard_interrupt_protection():
        try:
            proc = subprocess.run(command)

        except Exception as ex:
            log.warning("Got Exception: %s", ex)

        log.info("Command exit status/return code: %s", proc.returncode)
        return proc.returncode
