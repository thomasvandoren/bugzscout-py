#!/bin/bash

# Setup the environment with FogBugz configuration.
export BUGZSCOUT_URL='http://fogbugz/scoutSubmit.asp'
export BUGZSCOUT_USER='error-user'
export BUGZSCOUT_PROJECT='MyShellScript'
export BUGZSCOUT_AREA='Errors'

this_node=$(hostname --fqdn)

function bugzscout_wrap()
{
    # The call is all the arguments to this function.
    local call=$@

    # Call the function.
    bash -c "${call}"
    local exit_code=$?

    # If non-zero exit code, report error.
    if [ "${exit_code}" != "0" ] ; then
        bugzscout "${call} in ${0} failed with exit code ${exit_code} on ${this_node}" \
            || /bin/true
    fi

    return $exit_code
}
