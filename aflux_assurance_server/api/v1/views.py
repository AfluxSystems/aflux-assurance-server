import pprint
import traceback
from flask import current_app
from flask.views import MethodView
from aflux_assurance_server.api.v1 import api
from aflux_assurance_server.utils.jobs import ExampleWorker  # Import your jobs
#from aflux_assurance_server.api.v1.schemas import RealtimeDeviceSchema  # Import your schemas


@api.route('/')
def index():
    current_app.logger.info("I just used current_app!")
    return "Hello, World!"


# Example of MethodView (PREFERRED OVER FUNCTION-BASED VIEWS)
# class RealtimePollingAPI(MethodView):
#     """
#     This class controls the API for sending config update requests down to collectors.
#     """
#
#     def post(self):
#         """POST method handling"""
#         # Grab raw JSON data
#         raw_data = flask.request.get_json(force=True)
#         current_app.logger.debug(
#             "Received realtime request with JSON data:\n{}".format(
#                 pprint.pformat(raw_data, indent=2)
#             )
#         )
#         # Initialize Schema used to deserialize JSON data
#         schema = RealtimeDeviceSchema(many=isinstance(raw_data, list))
#         # Attempt to load the data into schema
#         json_data = schema.load(raw_data)
#         # Schema will have validated the data, check for errors. Return them if found.
#         if json_data.errors:
#             return self._request_invalid(json_data)
#         return self._request_valid(json_data)
#
#     def _request_invalid(self, json_data):
#         """Handle the response for a bad request from the user."""
#         response_dict = {
#             'errors': json_data.errors
#         }
#         return flask.jsonify(**response_dict), 400  # BAD REQUEST
#
#     def _request_valid(self, json_data):
#         """Handle the response for a good request from the user."""
#         try:
#             response_data = RealtimeFlaskPollRequestWorker(json_data.data,
#                                                            RealtimeGroupManagerRequestSchema,
#                                                            current_app).do_work()
#             resp_dict = {
#                 'result': response_data,
#             }
#             code = 200
#         except Exception as e:
#             current_app.logger.error("Failed to perform realtime request:\n{}".format(traceback.format_exc()))
#             resp_dict = {
#                 'error_message': str(e)
#             }
#             code = 500
#         return flask.jsonify(**resp_dict), code
# api.add_url_rule('/example', view_func=RealtimePollingAPI.as_view('example_api'))
