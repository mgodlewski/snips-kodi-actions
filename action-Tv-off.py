#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import ConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

class SnipsConfigParser(ConfigParser.SafeConfigParser):
    def to_dict(self):
        return {section : {option_name : option for option_name, option in self.items(section)} for section in self.sections()}


def read_configuration_file(configuration_file):
    try:
        with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(f)
            return conf_parser.to_dict()
    except (IOError, ConfigParser.Error) as e:
        return dict()

def subscribe_intent_callback(hermes, intentMessage):
    conf = read_configuration_file(CONFIG_INI)
    action_wrapper(hermes, intentMessage, conf)


def action_wrapper(hermes, intentMessage, conf):
    """
    PLAY
    """
    import simplejson
    import requests
    addr_ = conf['global']['ip']
    port_ =conf['global']['port']

    request = "{\"jsonrpc\":\"2.0\",\"method\":\"Addons.ExecuteAddon\",\"params\":{\"addonid\":\"script.json-cec\",\"params\":{\"command\":\"standby\"}},\"id\":1}"
    url = "http://" + addr_ + ":" + port_ + "/jsonrpc?request=" + request
    response = requests.get(url)
    json_data = simplejson.loads(response.text)






if __name__ == "__main__":
    with Hermes("localhost:1883") as h:
        h.subscribe_intent("Ianou:Tv-off", subscribe_intent_callback) \
         .start()