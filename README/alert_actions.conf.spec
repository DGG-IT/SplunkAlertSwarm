# This file contains values intended to be shared across
# all user-created Alert Action inputs.  These values will
# have corresponding entries in setup.xml, which defines the
# setup interface shown at Settings->Alert Actions->My Alert
# under the "Setup" column.

# The keys and value types specified here should match
# the keys and values in "default/alert_actions.conf".

# NOTE: This file and the corresponding setup.xml file are
# optional components.

# TODO: Change 'alertaction_template' to the name of your app.
[SHC_SwarmAlertWebhook]
# Parameter Key/Value pair template

# TODO: Define required parameters below
# param.<key_name> = <input_type> (e.g. <string>)
param.SwarmURL = <string>
param.SwarmUsername = <string>
param.SwarmPassword = <string>
