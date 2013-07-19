#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Asynchronously submit errors to FogBugz via BugzScout."""

from __future__ import print_function, unicode_literals

import bugzscout
import logging

try:
    from celery import Celery
except ImportError as ex:
    raise ImportError(
        'celery must be installed to use this extension: {0}'.format(
            ex.message))

__all__ = ('celery', 'submit_error',)

LOG = logging.getLogger('buzscout.ext.celery_app')

# This can be configured by creating a celeryconfig.py module on the
# PYTHONPATH. See the celery documentation for details:
#
# http://docs.celeryproject.org/en/latest/configuration.html
celery = Celery()


@celery.task
def submit_error(url, user, project, area, description,
                 extra=None, default_message=None):
    LOG.debug('Creating new BugzScout instance.')
    client = bugzscout.BugzScout(
        url, user, project, area)

    LOG.debug('Submitting BugzScout error.')
    client.submit_error(
        description, extra=extra, default_message=default_message)
