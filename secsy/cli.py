import logging
import os
import sys

import rich_click as click

from secsy.cmd import CommandRunner
from secsy.decorators import (OrderedGroup, register_commands, register_scans,
                              register_workflows)
from secsy.utils import (find_external_commands, find_internal_commands,
                         setup_logging)

DEBUG = bool(int(os.environ.get('DEBUG', '0')))
YAML_MODE = bool(int(os.environ.get('YAML_MODE', '0')))
ALL_CMDS = find_internal_commands() + find_external_commands()

level = logging.DEBUG if DEBUG else logging.INFO
setup_logging(level)


#--------#
# GROUPS #
#--------#

@click.group(cls=OrderedGroup)
def cli():
	"""Secsy CLI."""
	pass


@cli.group(cls=OrderedGroup)
def cmd():
	"""Run a command."""
	pass


@cli.group()
def workflow():
	"""Run a workflow."""
	pass


@cli.group()
def scan():
	"""Run a scan."""
	pass


@cli.group()
def utils():
	"""Run a utility."""
	pass


@cli.command()
def worker():
	"""Run a Celery worker."""
	CommandRunner.run_command(
		'celery -A secsy.celery.app worker',
		print_timestamp=True
	)

register_commands(cmd)
register_workflows(workflow)
register_scans(scan)


#-------#
# UTILS #
#-------#


@utils.command()
@click.argument('cmds', required=False)
def install(cmds):
	"""Install commands."""
	if cmds is not None:
		cmds = cmds.split(',')
		cmds = [cls for cls in ALL_CMDS if cls.__name__ in cmds]
	else:
		cmds = ALL_CMDS
	for cls in cmds:
		cls.install()


#------#
# TEST #
#------#
DEFAULT_CMD_OPTS = {
	'print_timestamp': True,
	'print_line': True,
	'print_cmd': True,
}


@utils.group()
def test():
	"""Run secsy tests."""
	pass


@test.command()
def integration():
	result = CommandRunner.run_command(
		'python3 -m unittest discover -v tests.integration',
		**DEFAULT_CMD_OPTS
	)
	sys.exit(result.return_code)


@test.command()
@click.option('--commands', '-c', type=str, default='', help='Secsy commands to test (comma-separated)')
@click.option('--coverage', '-x', is_flag=True, help='Run coverage on results')
def unit(commands, coverage=False):
	os.environ['TEST_COMMANDS'] = commands or ''
	result = CommandRunner.run_command(
		'coverage run --omit="*test*" -m unittest discover -v tests.unit',
		**DEFAULT_CMD_OPTS
	)
	if coverage:
		CommandRunner.run_command(
			'coverage report -m',
			**DEFAULT_CMD_OPTS
		)
	sys.exit(result.return_code)


@test.command()
def lint():
	result = CommandRunner.run_command(
		'flake8 secsy/',
		**DEFAULT_CMD_OPTS
	)
	sys.exit(result.return_code)


# @cli.command('scan')
# @click.argument('scan_name')
# @click.argument('host')
# @click.option('-table', is_flag=True, default=False, help='Table mode')
# @click.option('-verbose', '-v', is_flag=True, default=False, help='Verbose mode')
# def scan_run(scan_name, host, table, verbose):
# 	"""Run a scan."""
# 	opts = {
# 		'table': table,
# 		'quiet': not verbose,
# 		# 'print_timestamp': True,
# 		'json': True
# 	}
# 	list(run_scan(scan_name, host, **opts))