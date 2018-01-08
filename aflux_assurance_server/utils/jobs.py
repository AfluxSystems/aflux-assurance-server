"""
This is where you should be performing all of the heavy-lifting for your app. NOT in views.py
"""
import os
import uuid
import yaml
import errno
import shutil
import pickle
import traceback
import itertools
from operator import itemgetter



# You should subclass this base class so that you follow a DRY development model.
class AbstractFlaskWorker:
    """
    Class to handle the newer configuration of the flask application.
    """
    def __init__(self, flask_app, *args, **kwargs):
        super().__init__()
        self.app = flask_app
        self._verify_config(self.app)

    def do_work(self):
        """Abstract method to override"""
        raise NotImplementedError()

    def _verify_config(self, flask_app):
        flask_app.logger.debug("Verifying worker configuration")
        try:
            self._verify_flask_settings(flask_app)
        except ValueError:
            flask_app.logger.critical(traceback.format_exc())
            raise

    @staticmethod
    def _verify_flask_settings(flask_app):
        flask_app.logger.debug("Verifying flask settings")
        errors = []
        # if 'SNAP_DRIVER_REFRESH_SYSTEM_INTERVAL' not in flask_app.config:
        #     message = "SNAP_DRIVER_REFRESH_SYSTEM_INTERVAL not found in settings"
        #     errors.append(message)
        # if 'SNAP_DRIVER_NO_DELETE' in flask_app.config:
        #     if not isinstance(flask_app.config['SNAP_DRIVER_NO_DELETE'], bool):
        #         message = "SNAP_DRIVER_NO_DELETE is not a boolean"
        #         errors.append(message)
        # else:
        #     message = "SNAP_DRIVER_NO_DELETE not found in settings"
        #     errors.append(message)
        # if not os.path.exists(flask_app.config['SNAP_GROUP_MANAGERS_FILE']):
        #     message = "'{}' does not point to an existing or accessible file".format(flask_app.config['SNAP_GROUP_MANAGERS_FILE'])
        #     errors.append(message)
        # if 'TSDB_SETTINGS' in flask_app.config:
        #     if isinstance(flask_app.config['TSDB_SETTINGS'], dict):
        #         if 'BASE_URL' not in flask_app.config['TSDB_SETTINGS']:
        #             message = "BASE_URL not found in TSDB_SETTINGS"
        #             errors.append(message)
        #     else:
        #         message = "TSDB_SETTINGS is not a dictionary"
        #         errors.append(message)
        # else:
        #     message = "TSDB_SETTINGS not found in settings"
        #     errors.append(message)
        # if 'SNAP_DJANGO_SETTINGS' in flask_app.config:
        #     if isinstance(flask_app.config['SNAP_DJANGO_SETTINGS'], dict):
        #         if 'BASE_URL' not in flask_app.config['SNAP_DJANGO_SETTINGS']:
        #             message = "BASE_URL not found in SNAP_DJANGO_SETTINGS"
        #             errors.append(message)
        #         if 'USERNAME' not in flask_app.config['SNAP_DJANGO_SETTINGS']:
        #             message = "USERNAME not found in SNAP_DJANGO_SETTINGS"
        #             errors.append(message)
        #         if 'PASSWORD' not in flask_app.config['SNAP_DJANGO_SETTINGS']:
        #             message = "PASSWORD not found in SNAP_DJANGO_SETTINGS"
        #             errors.append(message)
        #     else:
        #         message = "SNAP_DJANGO_SETTINGS is not a dictionary"
        #         errors.append(message)
        # else:
        #     message = "SNAP_DJANGO_SETTINGS not found in settings"
        #     errors.append(message)
        if len(errors) > 0:
            raise ValueError(("The following configuration errors were "
                               "found while initializing the aflux-assurance-server:\n{}"
                              ).format("\n".join(errors)))

    @staticmethod
    def _load_yaml_file(flask_app, filepath):
        """locate vars file, load it."""
        flask_app.logger.debug("Loading YAML file: {}".format(filepath))
        try:
            assert os.path.exists(filepath) and os.path.isfile(filepath)
            with open(filepath, 'r') as stream:
                raw_config = yaml.load(stream)
            return raw_config
        except AssertionError:
            flask_app.logger.critical("YAML file '{}' does not exist or is not a file:\n{}".format(
                filepath,
                traceback.format_exc()
            ))
            raise
        except (OSError, IOError):
            flask_app.logger.critical("Failed to open YAML file '{}':\n{}".format(
                filepath,
                traceback.format_exc()
            ))
            raise
        except yaml.YAMLError:
            flask_app.logger.critical("Failed to parse YAML file '{}':\n{}".format(
                filepath,
                traceback.format_exc()
            ))
            raise

    @staticmethod
    def group_by(data, sort_key):
        """Extracted method to group dicts by a key."""
        data.sort(key=itemgetter(sort_key))
        data_by_key = {}
        for item, group in itertools.groupby(data, key=lambda x: x[sort_key]):
            data_by_key[item] = list(group)
        return data_by_key

    @staticmethod
    def create_dir(target):
        """Create directory locally, ignore error if
        it already exists."""
        if not os.path.exists(target):
            try:
                os.makedirs(target)
            except OSError as exception:
                if exception.errno != errno.EEXIST:
                    raise
        return True

    @staticmethod
    def get_home_directory():
        """Return this instance's module path."""
        return os.path.expanduser('~')

    def get_run_directory(self):
        """Return the location of local/var/run."""
        var_run_path = os.path.join(
            self.get_home_directory(),
            'local', 'var', 'run', __name__.split('.')[0]
        )
        self.create_dir(var_run_path)
        return var_run_path

    @staticmethod
    def delete_item(item):
        """Delete local item, whether it is a directory or a file."""
        if os.path.exists(item):
            if os.path.isdir(item):
                shutil.rmtree(item)
            else:
                try:
                    os.remove(item)
                except OSError as exception:
                    if exception.errno != errno.ENOENT:
                        raise
        return True

    @staticmethod
    def get_new_filename(extension=None):
        """Generate a new file name."""
        file_extention = extension if extension is not None else 'pickle'
        return "{}.{}".format(uuid.uuid1(), file_extention)

    def pickle_data(self, data, target=None):
        """
        Pickle data to a file. If target is None,
        the filename will be a uuid in picikle_staging.
        """
        pickle_path = target
        if pickle_path is None:
            pickle_path = os.path.join(
                self.get_run_directory(),
                self.get_new_filename()
            )
        with open(pickle_path, 'wb') as f:
            pickle.dump(data, f)
        return pickle_path

    @staticmethod
    def load_pickle(pickle_file, flask_app):
        """Unpack pickle file and return its data."""
        try:
            with open(pickle_file, 'rb') as f:
                data = pickle.load(f)
        except (OSError, IOError):
            message = "Exception when opening pickle file '{}':\n{}".format(pickle_file, traceback.format_exc())
            flask_app.logger.error(message)
            raise
        except pickle.UnpicklingError:
            message = "Exception when unpickling pickle file '{}':\n{}".format(pickle_file, traceback.format_exc())
            flask_app.logger.error(message)
            raise
        return data


class ExampleWorker(AbstractFlaskWorker):
    pass