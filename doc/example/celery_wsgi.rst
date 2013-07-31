Example WSGI server using celery extension
==========================================

The :doc:`simple WSGI example <simple_wsgi>` provides a concise example of how
to use bugzscout, but it is not suitable for production use. In a production
environment, the bugzscout reporting should not make an HTTP request to a
FogBugz server during another request. It is much more performant to do so
asynchronously.

`Celery <http://celeryproject.org/>`_ is an asynchronous task queue that
supports several backend implementation, like AMQP. The bugzscout package comes
with a Celery extension that has a flexible configuration.

The celery extension is the recommended way to submit errors in production
environments. This example describes how to setup and use the celery extension
in the context of a WSGI server application.

Celery setup
------------

The rest of this example will assume the code is being added to a module
called, ``myapp.py``. The module first needs to import the celery extension and
set a global ``celery`` variable.

.. code-block:: python

    import bugzscout.ext.celery_app
    celery = bugzscout.ext.celery_app.celery

Setting a direct reference to the celery instance in bugzscout will be
important when consuming the messages in the `celery worker
<http://docs.celeryproject.org/en/latest/userguide/workers.html>`_.

Next, create a WSGI app. This example provides a slightly more interesting app,
which returns different responses based on the HTTP request method.

.. literalinclude:: src/celery_wsgi.py
    :start-after:     return ['']
    :end-before: __main__

The ``_handle_exc`` function, invoked when an exception is caught, will call
the celery extension. That will publish a task to be consumed by a celery
worker. By returning ``['']``, the response body will be of length zero.

.. literalinclude:: src/celery_wsgi.py
    :start-after: bugzscout.ext.celery_app.celery
    :end-before: def app

Finally, add a main block to run the Paste httpserver.

.. literalinclude:: src/celery_wsgi.py
    :start-after: return _handle_exc

The :ref:`full myapp.py module <full_myapp>` is below.

Overview of WSGI app
--------------------

When an error is thrown while processing a request, this app will:

1. Catch the error.
2. Call ``start_response`` with exception info, which is a WSGI convention for
   returning error responses.
3. Call ``_handle_exc``.
4. ``_handle_exc`` will publish a new task with the error message and stack
   trace. The description and extra are the same as the :doc:`simple WSGI
   example <simple_wsgi>`. The call to
   ``bugzscout.ext.celery_app.submit_error.delay`` will do different things
   depending on how celery is configured. If an AMQP broker is used, the call
   will publish a message to an exchange. Later, a celery worker will consume
   that message.
5. Finally, ``_handle_exc`` returns ``['']`` so the response body will be
   empty. Since this is designed to work in production environments, exposing
   internal stack traces is not be ideal.

At this point, each error is creating a new celery task. There needs to be a
celery worker present to consume those tasks.

Celery worker setup
-------------------

Since a ``celery`` variable is set in the module, the celery executable can use
it to start a worker. For example:

.. code-block:: bash

    celery --app=myapp worker --loglevel=DEBUG

Running celery in this way is suitable for development. For production
environments, see the `Running the worker as a daemon
<http://docs.celeryproject.org/en/latest/tutorials/daemonizing.html>`_ section
of the celery docs.

.. _full_myapp:

Full myapp.py source
--------------------

.. literalinclude:: src/celery_wsgi.py
    :linenos:
