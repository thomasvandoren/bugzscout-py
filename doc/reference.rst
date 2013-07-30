Reference
=========

.. autoclass:: bugzscout.BugzScout
    :members:
    :special-members: __init__

Celery Extension
----------------

.. automodule:: bugzscout.ext.celery_app
.. autofunction:: bugzscout.ext.celery_app.submit_error(url, user, project, area, description, extra=None, default_message=None)

    Celery task for submitting errors asynchronously.

    :param url: string URL for bugzscout
    :param user: string fogbugz user to designate when submitting
                 via bugzscout
    :param project: string fogbugz project to designate for cases
    :param area: string fogbugz area to designate for cases
    :param description: string description for error
    :param extra: string details for error
    :param default_message: string default message to return in responses
