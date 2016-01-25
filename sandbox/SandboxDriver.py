
HACKADEMIC_TMP_CHAL_DIR = "./data/tmp/"

class SandboxDriver(object):
    """
    Interface to define the methods that any Sandbox Driver type class must implement
    """
    def launch(self):
        raise NotImplementedError("The class inheriting from SandboxDriver hansn't implemented launch")

