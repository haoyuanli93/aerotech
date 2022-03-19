"""
This module holds the class for interacting with an Aerotech XYZ.
Author R.Cole
"""
import socket
import datetime
import time

"""
I have modified the original class to be compatible with my current situation
1. One x axis is used.
2. The port connection is not stable. Therefore reconnect each time after the operation.

Author Haoyuan Li. 2020-10-21
"""

EOS_CHAR = '\n'  # End of string character
ACK_CHAR = '%'  # indicate success.
NAK_CHAR = '!'  # command error.
FAULT_CHAR = '#'  # task error.
TIMEOUT_CHAR = '$'

# Specify the location to save the log files
address = "/reg/d/psdm/xpp/xpplv1818/results/haoyuan/aerotech_logs"


class Ensemble:
    """Class providing control over a single Aerotech XYZ stage."""

    def __init__(self, ip, port):
        """
        Parameters
        ----------
        ip : str
            The ip of the Ensemble, e.g. 'localhost'
        port : int
            The port, default 8000
        """
        self._ip = ip
        self._port = port
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def move_relative(self, x_pos):
        """Move x axis to the specified position

        Parameters
        ----------
        x_pos : double
            The x position required
        """
        # Establish the connection
        self._socket.connect((self._ip, self._port))

        # Move
        command = "MOVEINC X%f XF10.0" % x_pos
        self._run(command)
        logging.info('Command written: %s', command)

        # Close
        self._socket.close()

    def connect(self):
        """Open the connection."""
        try:
            self._socket.connect((self._ip, self._port))
            logging.info('Connected')
        except ConnectionRefusedError:
            logging.error("Unble to connect.")

    def _close(self):
        """Close the connection."""
        self._socket.close()
        logging.info("Connection closed")

    def _run(self, command):
        """This method writes a command and returns the response,
        checking for an error code.

        Parameters
        ----------
        command : str
            The command to be sent, e.g. HOME X

        Returns
        ----------
        response : str
            The response to a command
        """
        if EOS_CHAR not in command:
            command = ''.join((command, EOS_CHAR))

        self._socket.send(command.encode())
        read = self._socket.recv(4096).decode().strip()
        code, response = read[0], read[1:]
        if code != ACK_CHAR:
            logging.error("Error from write_read().")
        return response

    def _home(self):
        """This method homes the stage."""
        self._run('HOME X')
        logging.info('Homed')

    def _move(self, x_pos):
        """Move x axis to the specified position

        Parameters
        ----------
        x_pos : double
            The x position required
        """
        command = "MOVEABS X%f XF10.0" % x_pos
        self._run(command)
        logging.info('Command written: %s', command)

    def _get_positions(self):
        """Method to get the latest positions.

        Returns
        ----------
        positions : float
            The X positions.
        """
        x_pos = float(self._run('PFBK X'))
        return x_pos
