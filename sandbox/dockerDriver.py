#!/usr/bin/env python2

import json
import random
import socket
from config import PROJECT_ROOT

import logging
from docker import Client
from docker import errors

from sandbox.SandboxDriver import SandboxDriver

__author__ = "AnirudhAnand (a0xnirudh) < anirudh@init-labs.org >"


class DockerDriver(SandboxDriver):
    """The Main Docker daemon class. This wil control the containers """

    def __init__(self, challenge_path, host, sandbox_config, challenge_id, base_url="unix://var/run/docker.sock", ):
        """
        Initialize a new docker instance
        :challenge_path: the path of the challenge relative to the project root
        :param host: the hostname of the machine the challenge runs on, it will be used to setup the url to the container
        :param sandbox_config: the dictionary containing the sandbox section of the config file
        :return:
        """
        self.client = Client(base_url=base_url)
        self.timer = "hour"
        self.host = host
        self.sandbox_config = sandbox_config
        self.challenge_path = challenge_path
        self.id = challenge_id

    def install(self, challenge_title):
        """
        Run a docker build -t <challenge_title> <PROJECT_ROOT+self.sandbox_config.dockerfile_path>
        :param challenge_title: the title of the challenge, that's what the tag of the image
        :raise: TypeError
        """
        dockerfile_path = PROJECT_ROOT + self.challenge_path + self.sandbox_config.dockerfile_path
        with open(dockerfile_path, 'r') as dockerfile:
            try:
                result = [line for line in self.client.build(fileobj=dockerfile, forcerm=True, tag=challenge_title, )]
                logging.info(result)
            except TypeError:
                logging.error(dockerfile_path + " doesn't exist or doesn't point to a docker file")
                raise TypeError

    def launch(self):
        """
        launch challenge build by install and initialized with init
        :raise: APIError when something goes wrong with Docker
        """
        port = self.__generate_port()
        try:
            self.client.start(self.id)

        except errors.APIError as exception:
            logging.error("Runtime Error: \n" + str(exception))
            raise exception

        return port

    def list_containers(self):
        return json.dumps(self.client.containers())

    def kill_container(self):
        self.client.rremove_container(container=self.id, force=True)

    def list_images(self):
        return json.dumps(self.client.images())

    def __generate_port(self):
        """
        Find a port between 1500 and 10000 in the system not used by docker
        :return:
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            port = random.randint(1500, 10000)
            result = sock.connect_ex((self.host, port))
            if result != 0:
                sock.close(result)
                return port

    """ def auto_container_killer(self):
            while True:
                sleep(300)
                container_list = self.client.containers()
                for i in range(0, len(container_list)):
                    temp = container_list[i].get("Status")
                    flag = re.findall(self.timer, temp)
                    if flag:
                        self.kill_container(container_list[i].get("Id"))
    """

    """def create_socket(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            s.bind((self.HOST, self.PORT))
        except socket.error as msg:
            print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            sys.exit(1)
        s.listen(10)
        while True:
            conn, addr = s.accept()
            thread.start_new_thread(self.client_thread, (conn,))

    def client_thread(self, conn):
        while True:
            data = conn.recv(1024)

            if 'launch' in str(data):
                challenge = str(data).split(':')[1]
                containers = self.launch(challenge)
                conn.sendall(containers)

            if data == 'list_containers':
                containers = self.list_containers()
                conn.sendall(containers)

            if 'kill_container' in str(data):
                containerid = str(data).split(':')[1]
                containerid = containerid.strip("\n")
                try:
                    containers = self.kill_container(containerid)
                except (TypeError) as exception:
                    pass
                conn.close()

        conn.close()
"""
