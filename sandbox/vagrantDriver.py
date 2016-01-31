import json
import os
import re

import shutil

import time
from vagrant import Vagrant

import SandboxDriver
from sandbox.cmd import helper


class VagrantDriver(SandboxDriver):
    """Class to deal with Vagrant Boxes.
    """

    @staticmethod
    def status():
        """
        Return the status of this vm instance
        :return: the output of vagrant status in machine readable format
        """
        return Vagrant.status()

    def add_box(self, box_name):
        """Function to add a vagrant box if not exists.
        Args:
            box_name (str): the name of box, ex ubuntu/trusty64
        """
        Vagrant.box_add(box_name)

    def __init__(self, (box_name, box_id)):
        """ init the challenge based on box_name in the directory named box_id
        Args:
            box_name (str): the name of box, ex ubuntu/trusty64
            box_id (str): the id of box

        """
        # Add a base box if not exists
        self.vagrantAddBox(box_name)

        # Create a challenge directory
        if not os.path.exists("./data"):
            os.makedirs("./data")

            tmp_curr_dir = "./data"
            if not os.path.exists(tmp_curr_dir + "/boxes"):
                os.makedirs(tmp_curr_dir + "/boxes")
                tmp_curr_dir += "/boxes"

                challenge_id_base = box_name.replace('/', '_')
                i = 1
                challenge_id = challenge_id_base + str(i)
                while os.path.exists(tmp_curr_dir + "/" + challenge_id):
                    i += 1
                    challenge_id = challenge_id_base + str(i)

                self.boxId = challenge_id
                os.makedirs(tmp_curr_dir + "/" + challenge_id)
                tmp_curr_dir += "/" + challenge_id

        os.chdir(SandboxDriver.HACKADEMIC_TMP_CHAL_DIR + box_id)
        Vagrant.init(box_name)
        self.setup()

    def setup(self, config_file, challenge_path):
        """
        Copy the challenge files described in the config file in the correct directory in challenge_path
        :param config_file: the challenge.xml challenge config file
        :param challenge_path:  the target path in the Hackademic tmp directory where the challenge will be launched
        :return:
        """
        shutil.copyfile(config_file, challenge_path + "/challenge.xml")
        # create the files directory and copy the files, to that directory
        # In same manner as provided in xml
        os.makedirs(challenge_path + "/files")
        directoriesCopies = []

        # Copy the files
        for _file in config_file.files:
            if helper.getRootFolder(_file.src) not in directoriesCopies:
                # Copy that folder to this folder
                directory = helper.getRootFolder(_file.src)
                helper.copy(
                        challenge_path + "/" + directory, challenge_path + "/files/" + directory)
                directoriesCopies.append(directory)

            # Copy the scripts
            for _script in config_file.scripts:
                if helper.getRootFolder(_script) not in directoriesCopies:
                    # Copy that folder to this folder
                    directory = helper.getRootFolder(_script)
                    helper.copy(
                            challenge_path + "/" + directory, challenge_path + "/files/" + directory)
                    directoriesCopies.append(directory)

                # Copy the manifest file
                if not config_file.puppetManifest == '':
                    os.makedirs(challenge_path + "/manifests")
                    shutil.copyfile(
                            challenge_path + "/" + config_file.puppetManifest, challenge_path + "/manifests/default.pp")

                if not config_file.modules == None:
                    helper.copy(
                            challenge_path + "/" + config_file.modules, challenge_path + "/modules")

                # Modify the vagrantFile according to xml data
                self.create_file(challenge_path)

                # Create a .status file
                status = {}
                status['basebox'] = config_file.baseBox
                status['active'] = 0
                with open(challenge_path + '/.status', 'w') as o_file:
                    o_file.write(json.dumps(status))

                self.out['data'] = config_file
                self.out['message'] = 'success'

    def launch(self):
        self.up()

    def up(self):
        """Function to start a vagrant box in current dir.

        Starts the VM

        Args:
            challenge_id (str): the challengeId retrived during create command
        """
        Vagrant.up()

    def stop(self, challenge_id):
        """Function to stop a vagrant box in current dir.

        Stops the VM

        Args:
           challenge_id (str): the challengeId retrived during create command
        """
        _challengeID = challenge_id
        if not os.path.exists("./data/challenges/" + _challengeID):
            self.out['error'] = True
            self.out['message'] = 'unable to stop %s, as it doesn\'t exist' % _challengeID
        else:
            challenge_path = "./data/challenges/" + _challengeID
            # get the box ID
            with open(challenge_path + '/.status', 'r') as cStatus:
                try:
                    boxId = json.loads(cStatus.readline())['boxId']
                    cStatus.close()
                    # Update basebox status
                    with open("./data/boxes/" + boxId + "/.status", 'r+') as bStatus:
                        baseboxStatus = json.loads(bStatus.readline())
                        baseboxStatus['active'] -= 1
                        bStatus.seek(0)
                        bStatus.write(json.dumps(baseboxStatus))
                        bStatus.truncate()
                except Exception:
                    print("Couldn't destroy challenge")
                Vagrant.destroy(challenge_id)

                # delete the challenegeID Dir
                shutil.rmtree(challenge_path)
                self.out['message'] = _challengeID + ' deleted successfully'
                self.out['data'] = {}
                self.out['data']['challenegeId'] = _challengeID

    def create_file(self, path):
        """Function to create a vagrant file from template.

        creates the vagrant file for a challenge based on template
        and data loaded from challenge.xml

        Args:
            path (str): path of the challenge directory
        """

        with open("./data/.VagrantFile", 'r') as f:
            data = f.read()

        data = data.replace('~basebox~', self.xmlData.baseBox)

        # Replace files with files
        m = re.search('\~files\~\\n(.*)\\n.*\~files\~', data)
        fileConfig = m.group(1)
        fileConfigScript = ''
        for _file in self.xmlData.files:
            if _file.src[0] == '/':
                prefix = 'files'
            else:
                prefix = 'files/'
            fileConfigScript += fileConfig.replace(
                    '~src~', prefix + _file.src).replace('~dest~', _file.dest) + "\n"
        data = data.replace(m.group(0), fileConfigScript)

        # Replace scripts with scripts
        m = re.search('\~shell\~\\n(.*)\\n.*\~shell\~', data)
        scriptConfig = m.group(1)
        scriptConfigScript = ''
        for _script in self.xmlData.scripts:
            if (_script[0] == '/'):
                prefix = 'files'
            else:
                prefix = 'files/'
            scriptConfigScript += scriptConfig.replace(
                    '~src~', prefix + _script) + "\n  "
        data = data.replace(m.group(0), scriptConfigScript)

        with open(path + "/Vagrantfile", 'w') as f:
            f.write(data)

    def modify_file(self, path, hostname):
        """Function to modify a vagrant file when Start command is sent.

        This further modifies the Vagrant file with host and private IP information.

        Args:
            path (str): the path of challenge dir
            hostname (str): the hostname for the VM

        """
        print "domain Name = %s ; " % self.domain
        with open(path, 'r') as f:
            data = f.read()

        data = data.replace(
                '~hostname~', hostname.replace('_', '.') + '.' + self.domain)
        data = data.replace('~private_ips~', self.privateIP)
        with open(path, 'w') as f:
            f.write(data)

    def install(self, box_id, config_file):
        """
        Overly complex challenge initial install method it exists to be refactored and have functionality stripped to
        the driver or installer <-- TODO: create challenge isntaller
        :parameter box_id the unique id of the box
        :parameter config_file the challenge's config file already parse as xml
        """
        if not os.path.exists("./data"):
            self.out['error'] = True
            self.out[
                'message'] = 'data directory does not exist. challenge cannot be created'
        else:
            challenge_path = "./data"
            if not os.path.exists(challenge_path + "/boxes"):
                self.out['error'] = True
                self.out[
                    'message'] = 'box for boxId %s not found' % box_id
            elif not os.path.exists(challenge_path + "/boxes/" + box_id):
                self.out['error'] = True
                self.out[
                    'message'] = 'box for boxId %s not found' % box_id
            else:
                if not os.path.exists(challenge_path + "/challenges"):
                    os.makedirs(challenge_path + "/challenges")

                _challengeID = box_id + helper.getRandStr(5)
                while os.path.exists(challenge_path + "/challenges/" + _challengeID):
                    _challengeID = box_id + helper.getRandStr(5)

                # Copy all files to this challenge directory
                helper.copy(
                        challenge_path + "/boxes/" + box_id,
                        challenge_path + "/challenges/" + _challengeID)

                # load the xml in this directory to memory
                challenge_path += "/challenges/" + _challengeID
                config_file = challenge_path + "/challenge.xml"
                xml_data = config_file

                # verify the content
                # check for flags
                err = False
                file_not_found = []

                for flags in xml_data.flags:
                    if not os.path.exists(challenge_path + "/files/" + flags):
                        err = True
                        file_not_found.append(flags)

                # check for files
                for files in xml_data.files:
                    if not os.path.exists(challenge_path + "/files/" + files.src):
                        print "[%s] file not found %s" % (time.time(),
                                                          challenge_path + "/files/" + files.src)

                        err = True
                        file_not_found.append(files.src)

                # check for scripts
                for script in xml_data.scripts:
                    if not os.path.exists(challenge_path + "/files/" + script):
                        print "[%s] script not found %s" % (time.time(),
                                                            challenge_path + "/files/" + script)
                        err = True
                        file_not_found.append(script)

                # check for manifests
                if not os.path.exists(challenge_path + "/manifests/default.pp"):
                    err = True
                    file_not_found.append(xml_data.puppetManifest)

                # local variable to store flag information
                flag_info = []

                if err:
                    self.out['err'] = True
                    self.out[
                        'message'] = 'following files were not found: \n'
                    for _file in file_not_found:
                        self.out['message'] += _file + '\n'
                else:
                    # modify the flag files
                    for flag in xml_data.flags:
                        _new_flag = helper.randomizeFlaginFile(
                                challenge_path + "/files/" + flag)
                        flag_info.append({"/files/" + flag: _new_flag})

                    # Subdomain thingy
                    print "modifying the vagrant file for network info"
                    self.modify_file(
                            challenge_path + "/Vagrantfile", _challengeID)

                    # start the box
                    print "starting vagrant box"
                    self.up(_challengeID)

                    # Update basebox status
                    with open("./data/boxes/" + box_id + "/.status", 'r+') as bStatus:
                        baseboxStatus = json.loads(bStatus.readline())
                        baseboxStatus['active'] += 1
                        bStatus.seek(0)
                        bStatus.write(json.dumps(baseboxStatus))
                        bStatus.truncate()
                        bStatus.close()

                        with open(challenge_path + "/.status", 'w') as cStatus:
                            status = {
                                'status': 'active',
                                'basebox': baseboxStatus['basebox'],
                                'boxId': box_id
                            }
                            cStatus.write(json.dumps(status))

                self.out['data'] = {}
                self.out['data']['challengeId'] = _challengeID
                self.out['data']['flags'] = flag_info
                self.out['message'] = 'success'
