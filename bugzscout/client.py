#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Submit errors or issues to FogBugz via BugzScout."""

from __future__ import print_function, unicode_literals

import logging
import requests

LOG = logging.getLogger('bugzscout.client')


class BugzScout(object):
    __doc__ = __doc__

    def __init__(self, url, user, project, area):
        """Initialize a new instance of bugzscout client.

        :param url: string URL for bugzscout
        :param user: string fogbugz user to designate when submitting
                     via bugzscout
        :param project: string fogbugz project to designate for cases
        :param area: string fogbugz area to designate for cases
        """
        self.url = url
        self.user = user
        self.project = project
        self.area = area

        LOG.debug(self)

    def __repr__(self):
        """String representation of this instance."""
        attr_strings = map(
            lambda k: '='.join((k, str(getattr(self, k, None)))),
            ['url', 'user', 'project', 'area'])
        return '{0}({1})'.format(self.__class__.__name__,
                                 ', '.join(attr_strings))

    def submit_error(self, description, extra=None, default_message=None):
        """Send an error to bugzscout.

        Sends a request to the fogbugz URL for this instance. If a case exists
        with the **same** description, a new occurrence will be added to that
        case. It is advisable to remove personal info from the description for
        that reason. Account ids, emails, request ids, etc, will make the
        occurrence counting builtin to bugzscout less useful. Those values
        should go in the extra parameter, though, so the developer
        investigating the case has access to them.

        When extra is not specified, bugzscout will increase the number of
        occurrences for the case with the given description, but it will not
        include an entry for it (unless it is a new case).

        :param description: string description for error
        :param extra: string details for error
        :param default_message: string default message to return in responses
        """
        req_data = {'ScoutUserName':       self.user,
                    'ScoutProject':        self.project,
                    'ScoutArea':           self.area,

                    # When this matches, cases are grouped together.
                    'Description':         description,
                    'Extra':               extra,

                    # 1 forces a new bug to be created.
                    'ForceNewBug':         0,
                    'ScoutDefaultMessage': default_message,

                    # 0 sends XML response, 1 sends HTML response.
                    'FriendlyResponse':    0,
                    }

        LOG.debug('Making bugzscout request to {0} with body {1}'.format(
            self.url, req_data))
        resp = requests.post(self.url, data=req_data)
        LOG.debug('Response from bugzscout request: {0} body:\n{1}'.format(
            resp, resp.content))

        if resp.ok:
            LOG.info('Successfully submitted error to bugzscout.')
        else:
            LOG.warn('Failed to submit error to bugzscout: {0}'.format(
                resp.reason))
