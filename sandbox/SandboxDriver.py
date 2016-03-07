
HACKADEMIC_TMP_CHAL_DIR = "./data/tmp/"

class SandboxDriver(object):
    """
    Interface to define the methods that any Sandbox Driver type class must implement
    """

    """
    Read
    Launch the challenge, randomize stuff if needed map ports/subdomain if needed and generally do whatever needs to be done
    on a case to case basis.
    Finally setup a -phone-home- channel to communicate logs/user_activity and such
    """
    def launch(self):
        raise NotImplementedError("The class inheriting from SandboxDriver hansn't implemented launch")

    """
    Create
    Called when the challenge is first received, the method downloads dependencies,
    builds and does whatever is necessary to make launching the challenge as instant as possible later.
    """
    def install(self):
        raise NotImplementedError("The class inheriting from SandboxDriver hasn't implemented install")

    """
    Delete
    Remove the challenge and cleanup
    """
    def remove(self):
        raise NotImplementedError("The class inheriting from SandboxDriver hasn't implemented remove")

    """
    Update
    Essentially remove and then install
    """
    def provision(self):
        raise NotImplementedError("The class inheriting from SandboxDriver hasn't implemented provision")
