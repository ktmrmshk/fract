###
#
#  git describe > .version
#

import os
from datetime import datetime, timedelta, timezone

VERSION="Not Defined"
with open('{}/.version'.format(os.path.dirname(__file__))) as f:
    ver=f.read()
    VERSION = ver.strip()


def strnow():
    JST = timezone(timedelta(hours=+9), 'JST')
    now = datetime.now(JST)
    return now.strftime("%Y/%m/%d, %H:%M:%S %Z")
