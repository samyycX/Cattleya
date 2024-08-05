import json

from rest_framework.renderers import JSONRenderer


class JSONResponseRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response_dict = {}
        if not (isinstance(data, dict) and 'code' in data):
            response_dict = {
                'code': 200,
                'data': data
            }
        else:
            response_dict = data

        return json.dumps(response_dict)
