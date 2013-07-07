#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Command line interface for sumbitting cases to FogBugz via BugzScout.

Environment variables can be used to set the FogBugz arguments with:

 * BUGZSCOUT_URL
 * BUGZSCOUT_USER
 * BUGZSCOUT_PROJECT
 * BUGZSCOUT_AREA
"""

from __future__ import print_function, unicode_literals

import argparse
import logging
import os

import bugzscout

LOG = logging.getLogger('bugzscout')


class _CliFormatter(argparse.RawDescriptionHelpFormatter,
                    argparse.ArgumentDefaultsHelpFormatter):
    pass


def _defaults():
    """Returns a dict of default args from the environment, which can be
    overridden by command line args.
    """
    d = {}
    d['url'] = os.environ.get('BUGZSCOUT_URL')
    d['user'] = os.environ.get('BUGZSCOUT_USER')
    d['project'] = os.environ.get('BUGZSCOUT_PROJECT')
    d['area'] = os.environ.get('BUGZSCOUT_AREA')
    return d


def _from_args(args):
    """Factory method to create a new instance from command line args.

    :param args: instance of :class:`argparse.Namespace`
    """
    return bugzscout.BugzScout(args.url, args.user, args.project, args.area)


def _init_logging(verbose):
    """Enable logging o stream."""
    hdlr = logging.StreamHandler()
    hdlr.setFormatter(logging.Formatter(
        '%(asctime)s [%(levelname)s] [%(module)s] %(message)s'))
    LOG.addHandler(hdlr)
    if verbose:
        LOG.setLevel(logging.DEBUG)
        LOG.debug('Verbose output enabled.')
    else:
        LOG.setLevel(logging.INFO)


def _parse_args():
    """Parse and return command line arguments."""
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=_CliFormatter)
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Enable verbose output.')

    fb_group = parser.add_argument_group('FogBugz arguments')
    fb_group.add_argument(
        '-u', '--url', help=(
            'URL for bugzscout requests to be sent. Should be something '
            'like .../scoutSubmit.asp.'))
    fb_group.add_argument(
        '--user', help='User to designate when submitting via bugzscout.')
    fb_group.add_argument(
        '--project', help='Fogbugz project to file cases under.')
    fb_group.add_argument(
        '--area', help='Fogbugz area to file cases under.')

    error_group = parser.add_argument_group('error arguments')
    error_group.add_argument('-e', '--extra',
                             help='Extra data to send with error.')
    error_group.add_argument('--default-message',
                             help='Set default message if case is new.')
    error_group.add_argument('description',
                             help=('Description of error. Will be matched '
                                   'against existing cases.'))

    parser.set_defaults(**_defaults())

    return parser.parse_args()


def main():
    """Create a new instance and publish an error from command line args.

    There is a console script for invoking this function from the command
    line directly.
    """
    args = _parse_args()
    _init_logging(args.verbose)
    client = _from_args(args)
    client.submit_error(args.description, args.extra,
                        default_message=args.default_message)


if __name__ == '__main__':
    main()
