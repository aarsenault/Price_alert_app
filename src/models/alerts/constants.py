

import os


# setting these variables as environment variables so when I push to github
# they reamain hidden.


# for MAILGUN API


URL = os.environ.get('MAILGUN_URL')
API_KEY = os.environ.get('MAILGUN_API_KEY')
FROM = os.environ.get('MAILGUN_FROM')

# for mongodb
COLLECTION = "alerts"

# src file constants
ALERT_TIMEOUT = 10