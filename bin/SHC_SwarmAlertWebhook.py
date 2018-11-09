"""
This script is intended to show the basic interaction between Splunk,
this script and an endpoint.

The script receives the JSON or XML payload from Splunk, parses out a URL
and a message, builds a message object and then sends the message to the
custom endpoint.

Alert action message payload contents include:
    * Environment Information - splunkd access information (url, session keys, etc)
    * Alert action information - Custom alert keys as defined savedsearches.conf
    * First search result - All extracted field values from the first search
      result (useful in certain situations).

   The structure of the JSON payload looks like:

    {
        "app": <app name that alert was sent from>,
        "owner": <owner of sending app>,
        "results_file": <absolute path to a file containing gzipped results>
        "Results_link": <url to view the results in splunk>
        "server_host": <hostname of splunk instance where the alert was fired>,
        "server_uri": <url to the Splunk REST endpoint>,
        "session_key": <session key>,
        "sid": <search id>,
        "search_name": <search name>,
        "configuration":
        {
            "param1": "value of parameter specified for alert (see alert_actions.conf.spec)."
        },
        "result":{
            "_raw": <the attributes of the _first_ event will be in this object>
        }
    }

Any output to STDERR will be captured by Splunk and logged.  You can control the
log level by supplying 'DEBUG', 'INFO', or 'ERROR' as the first word of a line output
by your script.  To find your logs, go to 'Settings' > 'Alert Actions' and select
'View log events' for your app.

"""

import sys
import json
import requests
from string import Template
from subprocess import call


def send_message(settings):

    print >> sys.stderr, "DEBUG Sending message with settings %s" % settings

    # retrieve endpoint url
    SwarmURL = settings.get('SwarmURL')
    SwarmUsername = settings.get('SwarmUsername')
    SwarmPassword = settings.get('SwarmPassword')
    SwarmEndpointTopic = settings.get('SwarmEndpointTopic')
    SwarmEndpointID = settings.get('SwarmEndpointID')
    SwarmEndpointComment = settings.get('SwarmEndpointComment')
    SwarmPostTarget = "%s/%s" % (SwarmEndpointTopic, SwarmEndpointID)
    print >> sys.stderr, "INFO Settings=%s" % (settings)
    print >> sys.stderr, "INFO Sending message to Swarm URL=%s , SwarmPostTarget=%s , Username=%s , Topic=%s , ID=%s , Comment=%s " % (SwarmURL, SwarmPostTarget, SwarmUsername, SwarmEndpointTopic, SwarmEndpointID, SwarmEndpointComment)
    
    try:
	r = requests.post(SwarmURL, data={"topic":SwarmPostTarget,"body":SwarmEndpointComment}, verify=False, auth=(SwarmUsername,SwarmPassword))
        print >> sys.stderr, 'DEBUG r=%s' % (r.text)
	return 200 <= r.status_code < 300
    except requests.exceptions.RequestException as e:
	print >> sys.stderr, e
	return False
	
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--execute":
        payload = json.loads(sys.stdin.read())
        if not send_message(payload.get('configuration')):
	    print >> sys.stderr, "FATAL Failed trying to send Payload"
	    sys.exit(2)
	else:
	    print >> sys.stderr, "INFO Payload successfully sent"
    else:
        print >> sys.stderr, "FATAL Unsupported execution mode (expected --execute flag)"
        sys.exit(1)
