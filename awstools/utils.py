# -*- coding: utf-8 -*-
import json

class AwsClsEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return int(mktime(obj.timetuple()))

        return json.JSONEncoder.default(self, obj)

# class TColor:
#     pink = '\033[95m'
#     blue = '\033[94m'
#     green = '\033[92m'
#     yellow = '\033[93m'
#     red = '\033[91m'
#     white = '\033[1m'
#     underline = '\033[4m'
#     reset = '\033[0m'
