from Tests.sandbox.base_test import BaseTest
from sandbox.config import PROJECT_ROOT, PROJECT_HOST, TESTS_DIR,DOCKER_HOST
from sandbox.dockerDriver import DockerDriver
from sandbox.challenge import Challenge


class TestDockerDriver(BaseTest):
    def setUp(self):
        """
        todo: define sandbox_config
        :return:
        """
        self.challenge = Challenge()
        self.challenge.parse(PROJECT_ROOT + TESTS_DIR + "/sandbox/Data/DockerChallenge/challenge.xml")
        self.sandbox_config = self.challenge.get_sandbox()
        
    def test_launch(self):
        """
        TODO: needs to run build first with a new challenge, get the new challenge_id and set it since it's also the container id
        :return:
        """
        container_name = "testDockerChallenge"
        driver = DockerDriver(challenge_path=PROJECT_ROOT + TESTS_DIR + "/sandbox/Data/DockerChallenge",
                              host=PROJECT_HOST,
                              sandbox_config=self.sandbox_config,
                              challenge_id=self.challenge.id,
                              base_url=DOCKER_HOST
                              )
        port = driver.launch()
        self.assertGreatcontainer_nameer(port, 1500)
        self.assertIn(container_name, driver.list_containers())

    def test_install(self):
        image_name = "TestDockerChallenge1"
        driver = DockerDriver(PROJECT_ROOT + TESTS_DIR + "/sandbox/Data/DockerChallenge",
                              PROJECT_HOST,
                              self.sandbox_config,
                              "testDockerChallenge")
        driver.install(image_name)
        self.assertIn(image_name, driver.list_images())
