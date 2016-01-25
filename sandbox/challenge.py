import xml.etree.ElementTree as ElementTree


class Challenge(object):
    """
    Holds all the necessary info to properly launch a challenge
    """
    flags,title, type, author, set_description = None

    # TODO: Add config validation
    def parse(self, config):
        """
        :parameter config -- path to the configuration file describing the challenge
        :return: void
        """
        root = ElementTree.parse(config).getroot()
        for child in root:
            self.challenge_config_items[child.tag]()
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

    def set_type(self,child):
        self.type = child.text

    challenge_config_items = {
        'flags'       : set_flags,
        'title'       : set_title,
        'author'      : set_author,
        'description' : set_description,
    }