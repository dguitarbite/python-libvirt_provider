#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_libvirt_provider
----------------------------------

Tests for `libvirt_provider` module.
"""

from click.testing import CliRunner

from libvirt_provider import cli


def test_command_line_interface():
    runner = CliRunner()
    result = runner.invoke(cli.cli)
    assert result.exit_code == 0
    assert 'Python libvirt provider.' in result.output
    help_result = runner.invoke(cli.cli, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output
