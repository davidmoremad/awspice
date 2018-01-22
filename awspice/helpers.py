# -*- coding: utf-8 -*-
import json
import datetime
from time import mktime

class ClsEncoder(json.JSONEncoder):
    '''
    JSON encoder extension.

    Sometimes Boto3 returns a non-serializable result to JSON and we get the following error when dumping that result:
    `TypeError: datetime.datetime (2015, 12, 3, 21, 20, 17, 326000, tzinfo = tzutc ()) is not JSON serializable`
    Solve it using this class encoder in ``cls`` argument

    Examples:
        $ json.dumps(results, indent=4, cls=awspice.ClsEncoder)
    '''

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return int(mktime(obj.timetuple()))

        return json.JSONEncoder.default(self, obj)
