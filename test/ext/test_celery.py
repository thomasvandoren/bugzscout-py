#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Verify celery extension."""

from __future__ import print_function, unicode_literals

import mock
import unittest

import bugzscout.ext


@mock.patch('celery.Celery.task')
class CeleryTests(unittest.TestCase):
    """Verify celery extension."""

    def setup_celery(self, **kwargs):
        """Setup shortcuts to the class.

        :param kwargs: keyword args to be passed into intialize
        """
        self.celery = bugzscout.ext.CeleryHandler
        self.broker_url = 'sqla+sqlite:///buzscout.ext.celery.tests.sqlite'
        self.celery.initialize(self.broker_url, **kwargs)

    def test_initialize(self, mock_task):
        """Verify initialize sets up the creates a celery instance and
        configures the task.
        """
        self.setup_celery()
        self.assertIsNotNone(self.celery.celery)
        self.assertEqual(self.broker_url, self.celery.celery._preconf['BROKER_URL'])
        mock_task.assert_called_once_with(self.celery.submit_error)

    def test_error__no_init(self, mock_task):
        """Verify RuntimeError raised when initialize has not been called."""
        self.assertRaises(RuntimeError,
                          bugzscout.ext.CeleryHandler.submit_error,
                          'the description')

    @mock.patch('bugzscout.BugzScout.submit_error')
    def test_error(self, mock_submit, mock_task):
        """Verify bugzscout instance is created and submit_error is called."""
        self.setup_celery()
        self.celery.submit_error(
            'description', extra='extra', default_message='default_message')
        mock_submit.assert_called_once_with(
            'description', extra='extra', default_message='default_message')

    def test_bugzscout_init_args__all_set(self, mock_task):
        """Verify args are correctly set when all are passed in."""
        self.setup_celery()
        expected_args = ('url', 'user', 'project', 'area')
        actual_args = self.celery._bugzscout_init_args(
            'url', 'user', 'project', 'area')
        self.assertEqual(expected_args, actual_args)

    def test_bugzscount_init_args__none_set(self, mock_task):
        """Verify defaults are used when no args are passed in."""
        self.setup_celery(
            default_url='default_url',
            default_user='default_user',
            default_project='default_project',
            default_area='default_area')
        expected_args = ('default_url', 'default_user', 'default_project', 'default_area')
        actual_args = self.celery._bugzscout_init_args(None, None, None, None)
        self.assertEqual(expected_args, actual_args)

    def test_bugzscout_init_args__mixed(self, mock_task):
        """Verify some defaults and some passed in."""
        self.setup_celery(
            default_url='default_url',
            default_user='default_user',
            default_project='default_project',
            default_area='default_area')
        expected_args = ('url', 'user', 'default_project', 'default_area')
        actual_args = self.celery._bugzscout_init_args('url', 'user', None, None)
        self.assertEqual(expected_args, actual_args)
