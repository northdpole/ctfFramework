import inspect
import xml.etree.ElementTree as ElementTree
import xmltodict
from pprint import pprint
import matplotlib.colors.Colormap as colomaps




class Challenge(object):
    """
    Holds all the necessary info to properly launch a challenge
    """
    id = category = flags = title = type = author = description = sandbox = None

    def __init__(self):
        pass

    # TODO: Add config validation
    def parse(self, config_path):
        """
        :parameter config_path -- path to the configuration file describing the challenge
        :return: void
        """
        file = open(config_path, 'r')

        config = dict(xmltodict.parse(file, xml_attribs=True))['challenge']
        file.close()
        self.author = config['author']
        self.sandbox = config['sandbox']
        self.description = config['description']
        self.title = config['title']

    def set_author(self, child):
        self.author = child.text

    def set_title(self, child):
        self.title = child.text

    def set_type(self, child):
        self.type = child.text

    def get_sandbox(self):
        return self.sandbox
