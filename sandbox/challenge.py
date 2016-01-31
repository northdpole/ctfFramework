import inspect
import xml.etree.ElementTree as ElementTree
import xmltodict


class Challenge(object):
    """
    Holds all the necessary info to properly launch a challenge
    """
    category = flags = title = type = author = description = sandbox = None

    def __init__(self):
        self.challenge_config_items = {
            'flags': self.set_flags,
            'title': self.set_title,
            'author': self.set_author,
            'description': self.set_description,
            'category': self.set_category,
            'sandbox': self.set_sandbox,
        }

    def set_sandbox(self, child):
        print type(child)
        print inspect.getmembers(child)
        self.sandbox = xmltodict.parse(child.text())

    def set_description(self, child):
        self.description = child.text

    def set_category(self, child):
        self.category = child.text

    # TODO: Add config validation
    def parse(self, config):
        """
        :parameter config -- path to the configuration file describing the challenge
        :return: void
        """
        
        root = ElementTree.parse(config).getroot()
        for child in root:
            self.challenge_config_items[child.tag](child)
        pass

    def set_author(self, child):
        self.author = child.text

    def set_flags(self, child):
        self.flags = []
        if len(child) > 0:
            for grandchild in child:
                self.flags.append(grandchild.text)

    def author(self, child):
        self.author = child.text

    def set_title(self, child):
        self.title = child.text

    def set_type(self, child):
        self.type = child.text

    def get_sandbox(self):
        return self.sandbox