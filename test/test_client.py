#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Verify BugzScout behavior."""

from __future__ import print_function, unicode_literals

import mock
import unittest

import bugzscout


class BugzScoutTests(unittest.TestCase):
    """Verify BugzScout behavior."""

    @mock.patch('requests.post')
    def test_submit_error(self, mock_post):
        """Ensure a well formed request is made via requests."""
        b = bugzscout.BugzScout('http://my.url/scoutSubmit.asp',
                                'my-user',
                                'my-project',
                                'my-area')
        b.submit_error('my-description', extra='Extra Credit!')
        mock_post.assert_called_once_with(
            'http://my.url/scoutSubmit.asp',
            data={'ScoutUserName':       'my-user',
                  'ScoutProject':        'my-project',
                  'ScoutArea':           'my-area',
                  'Description':         'my-description',
                  'Extra':               'Extra Credit!',
                  'ForceNewBug':         0,
                  'ScoutDefaultMessage': None,
                  'FriendlyResponse':    0})
