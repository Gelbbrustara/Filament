# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
import os
import json
import flask

class PrintManagerPlugin(octoprint.plugin.StartupPlugin,
                         octoprint.plugin.TemplatePlugin,
                         octoprint.plugin.SettingsPlugin,
                         octoprint.plugin.AssetPlugin,
                         octoprint.plugin.BlueprintPlugin):
    
    def __init__(self):
        self.data_folder = self.get_plugin_data_folder()
        self.filament_data_file = os.path.join(self.data_folder, "filament_data.json")
        self.print_data_file = os.path.join(self.data_folder, "print_data.json")
        self._ensure_data_files_exist()

    def _ensure_data_files_exist(self):
        if not os.path.exists(self.filament_data_file):
            with open(self.filament_data_file, 'w') as f:
                json.dump([], f)
        if not os.path.exists(self.print_data_file):
            with open(self.print_data_file, 'w') as f:
                json.dump([], f)

    def get_settings_defaults(self):
        return {}

    def get_template_configs(self):
        return [
            dict(type="navbar", custom_bindings=False),
            dict(type="settings", custom_bindings=False)
        ]

    def get_assets(self):
        return dict(
            js=["js/printmanager.js"],
            css=["css/printmanager.css"]
        )

    @octoprint.plugin.BlueprintPlugin.route("/add_print", methods=["POST"])
    def add_print(self):
        data = flask.request.json
        print_data = self._read_data_file(self.print_data_file)
        print_data.append(data)
        self._write_data_file(self.print_data_file, print_data)
        return flask.jsonify(dict(success=True))

    @octoprint.plugin.BlueprintPlugin.route("/get_prints", methods=["GET"])
    def get_prints(self):
        print_data = self._read_data_file(self.print_data_file)
        return flask.jsonify(print_data)

    @octoprint.plugin.BlueprintPlugin.route("/add_filament", methods=["POST"])
    def add_filament(self):
        data = flask.request.json
        filament_data = self._read_data_file(self.filament_data_file)
        filament_data.append(data)
        self._write_data_file(self.filament_data_file, filament_data)
        return flask.jsonify(dict(success=True))

    @octoprint.plugin.BlueprintPlugin.route("/get_filaments", methods=["GET"])
    def get_filaments(self):
        filament_data = self._read_data_file(self.filament_data_file)
        return flask.jsonify(filament_data)

    def _read_data_file(self, filepath):
        with open(filepath, 'r') as f:
            return json.load(f)

    def _write_data_file(self, filepath, data):
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)

__plugin_name__ = "Print Manager Plugin"
__plugin_version__ = "0.1.0"
__plugin_description__ = "A plugin to manage prints and filament usage"
__plugin_author__ = "Dein Name"
__plugin_pythoncompat__ = ">=2.7,<4"

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = PrintManagerPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {}
