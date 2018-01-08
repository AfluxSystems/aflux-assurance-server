import os
import json
import uuid
import traceback
import flask
import pathlib
from werkzeug.utils import secure_filename
from flask import current_app, request
from flask.views import MethodView
from aflux_assurance_server.api.v1 import api
from aflux_assurance_server.utils.jobs import ExampleWorker  # Import your jobs
#from aflux_assurance_server.api.v1.schemas import RealtimeDeviceSchema  # Import your schemas


@api.route('/')
def index():
    current_app.logger.info("I just used current_app!")
    return "Hello, World!"


class CheckEmploymentStatus(MethodView):
    def get(self):
        employers = request.args.getlist('empl')
        return flask.jsonify(self.get_employer_status(employers=employers))

    def get_employer_status(self, employers):
        statuses = self.read_employer_file()
        if employers:
            return {
                employer: statuses[employer.lower()]
                for employer in employers if employer.lower() in statuses
            }
        return statuses

    def read_employer_file(self):
        with open(current_app.config['EMPLOYMENT_FILE'], 'r') as f:
            status = json.load(f)
        return status


api.add_url_rule('/estatus', view_func=CheckEmploymentStatus.as_view('employment_status'))


class BackupFiles(MethodView):
    def post(self, employer, system):
        files = request.files.getlist('file')
        return self.backup_files(files=files, employer=employer, system=system)

    def backup_files(self, files, employer, system):
        uploaded = []
        errors = []
        for file in files:
            filepath, success = self.save_file(file=file, employer=employer, system=system)
            uploaded.append(filepath) if success else errors.append(filepath)
        return flask.jsonify(
            {
                'uploaded': uploaded,
                'errors': errors
            }
        )

    def save_file(self, file, employer, system):
        success = False
        filename = 'unknown-{}.file'.format(uuid.uuid4())
        save_path = os.path.join(
            current_app.config['UPLOAD_FOLDER'],
            employer.lower(),
            system.lower()
        )
        self.ensure_backup_path(save_path)
        try:
            filename = secure_filename(file.filename) or filename
            file.save(os.path.join(save_path, filename))
            success = True
        except:
            current_app.logger.error(
                "Failed to upload file: {}\n{}".format(
                    os.path.join(save_path, filename),
                    traceback.format_exc()
                )
            )
        return os.path.join(save_path, filename), success

    @staticmethod
    def ensure_backup_path(save_path):
        pathlib.Path(save_path).mkdir(parents=True, exist_ok=True)


backups_view = BackupFiles.as_view('backup')
api.add_url_rule(
    '/backup/<string:employer>/<string:system>',
     view_func=backups_view,
    methods=['POST', ],
)




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
