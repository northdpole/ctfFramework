import logging
import random
import string

from sandbox.challenge import Challenge
from sandbox.dockerDriver import DockerDriver
from sandbox.vagrantDriver import VagrantDriver


class Sandbox(object):

    def __init__(self, pathname):
        """
        Parse the challenge.xml config file and initialize the correct driver for the challenge
        (for now Docker or Vagrant).
        :parameter challenge the relative to project root path of the challenge base dir
        :return sandboxId
        :throw malformed challenge exception
        """
        self.path = pathname
        self.challengeConfig = self.parse_challenge_xml()
        self.driver = ''

        logging.debug("Initializing sandbox for challenge %s", pathname)
        pass

    def launch(self):
        logging.debug("Launching challenge %s", self.path)
        instance_id = self.generate_box_id()
        if 'box' ==  self.challengeConfig.type:
            self.driver = VagrantDriver(self.challengeConfig.name, instance_id)
        elif 'container' == self.challengeConfig.type:
            self.driver = DockerDriver()
        elif 'web' == self.challengeConfig.type:
            # do nothing, pure web challenges should be handled by the web interface(or if this file ever becomes
            # the core of challenge launching then just launch the challenge controller
            raise NotImplementedError

        self.driver.launch()
        pass

    def generate_box_id(self):
        """
        Generate a random 8 character unique-ish string to serve as the instance id
        :return a random 8 character string
        """
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))

    """
    Parse the challenge.yml file and instantiate a new challenge object
    NON USABLE YET
    ""
    def parse_challenge_yml(self):
        with open(self.challenge,'r') as doc:
            config = yaml.load(doc)
            challenge = Challenge()
        return challenge.parse(self.challenge)
    """

    def parse_challenge_xml(self):
        challenge = Challenge()
        return challenge.parse(self.path)




