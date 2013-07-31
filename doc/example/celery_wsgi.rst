Example WSGI server using celery extension
==========================================

* intro mentioning prod and security
* celery setup
* app
* _handle_exc
* running the server

* What happens now when an error is thrown? ...

* celery worker


.. literalinclude:: src/celery_wsgi.py
    :start-after: __future__
    :end-before: def _handle_exc
    :linenos:


.. literalinclude:: src/celery_wsgi.py
    :start-after: bugzscout.ext.celery_app.celery
    :end-before: def app
    :linenos:


.. literalinclude:: src/celery_wsgi.py
    :start-after:     return ['']
    :end-before: __main__
    :linenos:


.. literalinclude:: src/celery_wsgi.py
    :start-after: return _handle_exc
    :linenos:


.. literalinclude:: src/celery_wsgi.py
    :linenos:


.. code-block:: bash
    :linenos:

    celery --app=myapp worker --loglevel=DEBUG
