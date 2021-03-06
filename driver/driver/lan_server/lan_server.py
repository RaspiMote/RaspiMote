# RaspiMote
# https://github.com/RaspiMote
# Copyright (C) 2021 RaspiMote (@A-delta & @Firmin-Launay)

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

"""
Build a web server to receive RaspiMote's requests and Driver's configuration.
"""
from command_processor import process
import threading
from flask_cors import CORS
from flask import Flask, request, send_file
from json import load, loads, dumps
from os import path, getenv
from time import time
from sys import platform
from subprocess import run

from defs import *

from built_in_fcn import actions

app = Flask(__name__)
CORS(app)

if platform == "linux":
    config_file_path = f"{getenv('HOME')}/.config/RaspiMote"
elif platform == "win32":
    config_file_path = f"{getenv('APPDATA')}\\RaspiMote"
elif platform == "darwin": # EXPERIMENTAL
    config_file_path = f"{getenv('HOME')}/Library/Application Support/RaspiMote"

file = load(open(path.join(config_file_path, "pi_ip.raspimote")))
pi_ip = file["ip"]
connection_code = file["code"]
trigger_actions_file_path = path.join(config_file_path, "trigger_actions.raspimote")


@app.route('/action', methods = ['POST'])
def action():

    ip = request.remote_addr
    if pi_ip != ip:
        return '<h1>Not authorized.</h1><h2>IPs do not match.</h2>', 403
    else:
        json = request.json
        code = json["code"]

        if code != connection_code:
            return '<h1>Not authorized.</h1><h2>Codes do not match.</h2>', 403
        else:
            if json["request"]["type"] != "ping":
                processor = threading.Thread(name='Processor', target=process, args=[json])
                processor.start()

            return "True"



#### Configuration ####

#@app.route('/config/add_action', methods = ['POST'])   <- NEED TO BE ADDED
@app.route('/config', methods = ['POST'])
def add_action():
    if request.remote_addr == "127.0.0.1":
        conf_req = loads(list(request.form.to_dict().keys())[0])
        print(f"Adding action : {conf_req}")

        write_action(trigger_actions_file_path, conf_req)

        return "Configuration modified successfully."
    else:
        return '<h1>Not authorized.</h1><h2>Only <code>localhost</code> can configure RaspiMote.</h2>', 403


@app.route('/config/remove_action', methods = ['POST'])
def remove_action():
    if request.remote_addr == "127.0.0.1":
        conf_req = loads(list(request.form.to_dict().keys())[0])
        print(f"Removing action : {conf_req}")

    else:
        return '<h1>Not authorized.</h1><h2>Only <code>localhost</code> can configure RaspiMote.</h2>', 403


@app.route('/config/get_actions', methods = ['POST'])
def get_actions():
    if request.remote_addr == "127.0.0.1":
        actions = get_actions_file(trigger_actions_file_path)
        print(f"Saved actions : {actions}")
        return dumps(actions)
    else:
        return '<h1>Not authorized.</h1><h2>Only <code>localhost</code> can configure RaspiMote.</h2>', 403

#### End Configuration ####


@app.route('/')
def config_ui():
    if request.remote_addr == "127.0.0.1":
        return send_file("ui/ui_model.html")
    else:
        return '<h1>Not authorized.</h1><h2>Only <code>localhost</code> can configure RaspiMote.</h2>', 403

@app.route('/style.css')
def config_css():
    if request.remote_addr == "127.0.0.1":
        return send_file("ui/style.css")
    else:
        return '<h1>Not authorized.</h1><h2>Only <code>localhost</code> can configure RaspiMote.</h2>', 403

@app.route('/initElements.js')
def config_js1():
    if request.remote_addr == "127.0.0.1":
        return send_file("ui/js/initElements.js", mimetype="text/javascript")
    else:
        return '<h1>Not authorized.</h1><h2>Only <code>localhost</code> can configure RaspiMote.</h2>', 403

@app.route('/showHide.js')
def config_js2():
    if request.remote_addr == "127.0.0.1":
        return send_file("ui/js/showHide.js", mimetype="text/javascript")
    else:
        return '<h1>Not authorized.</h1><h2>Only <code>localhost</code> can configure RaspiMote.</h2>', 403

@app.route('/showHideButton.js')
def config_js3():
    if request.remote_addr == "127.0.0.1":
        return send_file("ui/js/showHideButton.js", mimetype="text/javascript")
    else:
        return '<h1>Not authorized.</h1><h2>Only <code>localhost</code> can configure RaspiMote.</h2>', 403

@app.route('/showHideADC.js')
def config_js4():
    if request.remote_addr == "127.0.0.1":
        return send_file("ui/js/showHideADC.js", mimetype="text/javascript")
    else:
        return '<h1>Not authorized.</h1><h2>Only <code>localhost</code> can configure RaspiMote.</h2>', 403

@app.route('/showHideKeyboard.js')
def config_js5():
    if request.remote_addr == "127.0.0.1":
        return send_file("ui/js/showHideKeyboard.js", mimetype="text/javascript")
    else:
        return '<h1>Not authorized.</h1><h2>Only <code>localhost</code> can configure RaspiMote.</h2>', 403


@app.route('/showHideGamepad.js')
def config_js6():
    if request.remote_addr == "127.0.0.1":
        return send_file("ui/js/showHideGamepad.js", mimetype="text/javascript")
    else:
        return '<h1>Not authorized.</h1><h2>Only <code>localhost</code> can configure RaspiMote.</h2>', 403

@app.route('/saveButton.js')
def config_js7():
    if request.remote_addr == "127.0.0.1":
        return send_file("ui/js/saveButton.js", mimetype="text/javascript")
    else:
        return '<h1>Not authorized.</h1><h2>Only <code>localhost</code> can configure RaspiMote.</h2>', 403

@app.route('/saveADC.js')
def config_js8():
    if request.remote_addr == "127.0.0.1":
        return send_file("ui/js/saveADC.js", mimetype="text/javascript")
    else:
        return '<h1>Not authorized.</h1><h2>Only <code>localhost</code> can configure RaspiMote.</h2>', 403

@app.route('/saveKeyboard.js')
def config_js9():
    if request.remote_addr == "127.0.0.1":
        return send_file("ui/js/saveKeyboard.js", mimetype="text/javascript")
    else:
        return '<h1>Not authorized.</h1><h2>Only <code>localhost</code> can configure RaspiMote.</h2>', 403

@app.route('/saveGamepad.js')
def config_js10():
    if request.remote_addr == "127.0.0.1":
        return send_file("ui/js/saveGamepad.js", mimetype="text/javascript")
    else:
        return '<h1>Not authorized.</h1><h2>Only <code>localhost</code> can configure RaspiMote.</h2>', 403

@app.route('/jquery.js')
def jquery():
    if request.remote_addr == "127.0.0.1":
        return send_file("ui/js/jquery-3.6.0.min.js", mimetype="text/javascript")
    else:
        return '<h1>Not authorized.</h1><h2>Only <code>localhost</code> can configure RaspiMote.</h2>', 403

@app.route('/sweetalert.js')
def sweetalert():
    if request.remote_addr == "127.0.0.1":
        return send_file("ui/js/sweetalert2.all.min.js", mimetype="text/javascript")
    else:
        return '<h1>Not authorized.</h1><h2>Only <code>localhost</code> can configure RaspiMote.</h2>', 403

@app.route('/sweetalert.css')
def sweetalert_css():
    if request.remote_addr == "127.0.0.1":
        return send_file("ui/js/sweetalert2.borderless.min.css")
    else:
        return '<h1>Not authorized.</h1><h2>Only <code>localhost</code> can configure RaspiMote.</h2>', 403


@app.route('/RaspiMote_logo.ico')
def config_rsp_ico():
    if request.remote_addr == "127.0.0.1":
        return send_file("ui/RaspiMote_logo.ico")
    else:
        return '<h1>Not authorized.</h1><h2>Only <code>localhost</code> can configure RaspiMote.</h2>', 403

@app.route('/RaspiMote_logo_500px.png')
def config_rsp_png():
    if request.remote_addr == "127.0.0.1":
        return send_file("ui/RaspiMote_logo_500px.png")
    else:
        return '<h1>Not authorized.</h1><h2>Only <code>localhost</code> can configure RaspiMote.</h2>', 403

@app.route('/loading.gif')
def gif_loading():
    if request.remote_addr == "127.0.0.1":
        return send_file("ui/loading.gif")
    else:
        return '<h1>Not authorized.</h1><h2>Only <code>localhost</code> can configure RaspiMote.</h2>', 403

@app.route('/xbox_one.png')
def xbox_one_controller():
    if request.remote_addr == "127.0.0.1":
        return send_file("ui/xbox_one.png")
    else:
        return '<h1>Not authorized.</h1><h2>Only <code>localhost</code> can configure RaspiMote.</h2>', 403

@app.route('/get_inventory', methods = ['POST'])
def config_get_inventory():
    if request.remote_addr == "127.0.0.1":
        try:
            with open (path.join(config_file_path, "inventory.raspimote"), "r") as inventory:
                return inventory.read()
        except FileNotFoundError:
            return "INVENTORY_NOT_FOUND", 500
    else:
        return '<h1>Not authorized.</h1><h2>Only <code>localhost</code> can configure RaspiMote.</h2>', 403


@app.route('/open_editor', methods = ['POST'])
def open_editor():
    if request.remote_addr == "127.0.0.1":
        if platform == "win32":
            try:
                run(["C:\\Program Files\\RaspiMote\\py\\pythonw.exe", "C:\\Program Files\\RaspiMote\\py\\Lib\\idlelib\\idle.py", f"{config_file_path}\\custom_fcn\\custom_fcn.py"])
                return "True"
            except:
                pass
            try:
                run(["code", f"{config_file_path}\\custom_fcn\\custom_fcn.py"])
                return "True"
            except:
                pass
            try:
                run(["notepad", f"{config_file_path}\\custom_fcn\\custom_fcn.py"])
                return "True"
            except:
                pass
            return "False", 500
        elif platform == "linux":
            try:
                run(["idle3", f"{config_file_path}/custom_fcn/custom_fcn.py"])
                return "True"
            except:
                pass
            try:
                run(["code", f"{config_file_path}/custom_fcn/custom_fcn.py"])
                return "True"
            except:
                pass
            try:
                run(["gedit", f"{config_file_path}/custom_fcn/custom_fcn.py"])
            except:
                pass
            try:
                run(["leafpad", f"{config_file_path}/custom_fcn/custom_fcn.py"])
            except:
                pass
            return "False", 500
    else:
        return '<h1>Not authorized.</h1><h2>Only <code>localhost</code> can open an editor.</h2>', 403

@app.route('/test')
def test():
    return 'UP !'
