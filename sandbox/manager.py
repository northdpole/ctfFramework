import argparse
import logging
import logging.config
import os

from sandbox.Sandbox import Sandbox
from sandbox.dockerDriver import  DockerDriver


def main():

    setup_logging()
    parser = argparse.ArgumentParser()
    parser.add_argument("-d","--daemon", help="run in the background as a daemon, all other arguments will be ignored", action="store_true")
    parser.add_argument("-c","--challenge", help="the path of the document root of the challenge you wish to launch")
    parser.add_argument("--install_depenencies", help="install docker and vagrant if not already installed (needs sudo, will exit after completion)")

    args = parser.parse_args()
    print args

    if args.install_dependencies:
        # try to execute ansible, if fail try to execute setup.py
        return

    if args.daemon:
        daemonize()
        return

    if args.challenge:
        box = Sandbox(args.challenge)
        box.launch()

    return


def daemonize():
    containerdaemon = DockerDriver()
    child_pid = os.fork()
    if child_pid == 0:
        containerdaemon.auto_container_killer()
    else:
        containerdaemon.create_socket()

    pass



def setup_logging():
    """
    This function defines a standard template which can be used to create
    additional logging classes in the future. Give a valid name and the
    filename to which the logs should be saved.
    :rtype:             ->       object
        :param  name:       ->       Name given to the logging process
        :param filename:    ->       Filename to which logs should be saved
        :return:            ->       A logger object that can be used to log
    """
    logging.config.fileConfig('logging.conf')
    return logging.getLogger('root')

if __name__ == '__main__':
    main()
