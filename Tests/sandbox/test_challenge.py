from Tests.sandbox.base_test import BaseTest
from sandbox.challenge import Challenge
from sandbox.config import *


class TestChallenge(BaseTest):
    example_challenge_xml_path = PROJECT_ROOT + TESTS_DIR + "/sandbox/Data/baseChallenge/challenge.xml"
    challenge = None

    def test_parse(self):
        self.challenge = Challenge();
        self.challenge.parse(self.example_challenge_xml_path)
        self.assertIsNotNone(self.challenge.title)
        self.assertIsNotNone(self.challenge.author)
        self.assertIsNotNone(self.challenge.description)
        self.assertIsNotNone(self.challenge.sandbox)
