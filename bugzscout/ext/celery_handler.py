#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Asynchronously submit errors to FogBugz via BugzScout."""

from __future__ import print_function, unicode_literals

import bugzscout
import logging
import threading

try:
    import celery
except ImportError as ex:
    raise ImportError(
        'celery must be installed to use this extension: {0}'.format(
            ex.message))

LOG = logging.getLogger('buzscout.ext.celery')


class CeleryHandler(threading.local):
    __doc__ = __doc__

    celery = None
    default_url = None
    default_user = None
    default_project = None
    default_area = None

    @classmethod
    def initialize(cls, celery_broker, default_url=None, default_user=None,
                   default_project=None, default_area=None):
        """Initialize celery class attribute with celery_instance. Optionally,
        default BugzScout initialization parameters can be provided.

        :param celery_broker: string URL for Celery broker
        :param default_url: string URL for bugzscout
        :param default_user: string fogbugz user to designate when submitting
                             via bugzscout
        :param default_project: string fogbugz project to designate for cases
        :param default_area: string fogbugz area to designate for cases
        """
        LOG.info('Creating new Celery instance for broker: {0}'.format(
            celery_broker))
        cls.celery = celery.Celery(__name__, broker=celery_broker)
        cls.celery.task(cls.submit_error)

        cls.default_url = default_url
        cls.default_user = default_user
        cls.default_project = default_project
        cls.default_area = default_area

    @classmethod
    def submit_error(cls, description, extra=None, default_message=None,
                     bugzscout_url=None, bugzscout_user=None,
                     bugzscout_project=None, bugzscout_area=None):
        """Creates a new bugzscout instance and call submit_error on it.

        Raises RuntimeError if initialize has not been called on the class.

        Default versions of url, user, project, and area are used if not set
        here.

        :param description: string description for error
        :param extra: string details for error
        :param default_message: string default message to return in responses
o        :param bugzscout_url: string URL for bugzscout
        :param bugzscout_user: string fogbugz user to designate when submitting
                             via bugzscout
        :param bugzscout_project: string fogbugz project to designate for cases
        :param bugzscout_area: string fogbugz area to designate for cases
        """
        if cls.celery is None:
            raise RuntimeError('Please call intialize with a celery '
                               'instance before submitting errors.')

        LOG.debug('Creating new BugzScout instance.')
        init_args = cls._bugzscout_init_args(
            bugzscout_url, bugzscout_user, bugzscout_project, bugzscout_area)
        client = bugzscout.BugzScout(*init_args)

        LOG.debug('Submitting BugzScout error.')
        client.submit_error(
            description, extra=extra, default_message=default_message)

    @classmethod
    def _bugzscout_init_args(cls, url, user, project, area):
        """Returns list of initialization args for BugzScout. If any of the
        parameters to this function are None, the default class attributes are
        used.

        :param url: string URL for bugzscout
        :param user: string fogbugz user to designate when submitting
                     via bugzscout
        :param project: string fogbugz project to designate for cases
        :param area: string fogbugz area to designate for cases
        """
        def _choose(param, default):
            """Returns param if it is not None, otherwise returns default."""
            if param is not None:
                return param
            else:
                return default

        url = _choose(url, cls.default_url)
        user = _choose(user, cls.default_user)
        project = _choose(project, cls.default_project)
        area = _choose(area, cls.default_area)

        return (url, user, project, area)
