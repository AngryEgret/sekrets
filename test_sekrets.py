#!/usr/bin/env python

"""Tests for Sekrets."""

from scripttest import TestFileEnvironment

class TestSekrets:
    def setup(self):
        self.env = TestFileEnvironment('./test-output')

    def test_sekrets_help(self):
        'Test: sekrets help text'

        result = self.env.run('sekrets --help')
        assert result.returncode == 0
        assert result.stderr == ''
