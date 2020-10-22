import numpy as np


def find_rot_center_loc_t1(s1, d1, theta1, s2, d2, theta2, s3, d3, theta3):
    """
    Find the location of the center of rotation with respect to the tip of the splitting
    edge of CC1
    :param s1: width of the beam in um
    :param d1: value of t1_x in um
    :param theta1: angle in degree
    :param s2: width of the beam in um
    :param d2: value of t1_x in um
    :param theta2: angle in degree
    :param s3: width of the beam in um
    :param d3: value of t1_x in um
    :param theta3: angle in degree
    :return:
    """
    r = -(d2 - d1) + (s2 - s1)
    s = -(d3 - d2) + (s3 - s2)

    # Construct the coefficient matrix
    matrix = np.zeros((2, 2))
    matrix[0, 0] = np.sin(np.deg2rad(theta2)) - np.sin(np.deg2rad(theta1))
    matrix[1, 0] = np.sin(np.deg2rad(theta3)) - np.sin(np.deg2rad(theta2))

    matrix[0, 1] = np.cos(np.deg2rad(theta2)) - np.cos(np.deg2rad(theta1))
    matrix[1, 1] = np.cos(np.deg2rad(theta3)) - np.cos(np.deg2rad(theta2))

    # Get the location values
    rot_center_loc = np.dot(np.linalg.inv(matrix), np.array([r, s]))

    return rot_center_loc


def find_rot_center_loc_t6(s1, d1, theta1, s2, d2, theta2, s3, d3, theta3):
    """
    Find the location of the center of rotation with respect to the tip of the splitting
    edge of CC6
    :param s1: width of the beam in um
    :param d1: value of t1_x in um
    :param theta1: angle in degree
    :param s2: width of the beam in um
    :param d2: value of t1_x in um
    :param theta2: angle in degree
    :param s3: width of the beam in um
    :param d3: value of t1_x in um
    :param theta3: angle in degree
    :return:
    """
    r = (d2 - d1) - (s2 - s1)
    s = (d3 - d2) - (s3 - s2)

    # Construct the coefficient matrix
    matrix = np.zeros((2, 2))
    matrix[0, 0] = np.sin(np.deg2rad(theta2)) - np.sin(np.deg2rad(theta1))
    matrix[1, 0] = np.sin(np.deg2rad(theta3)) - np.sin(np.deg2rad(theta2))

    matrix[0, 1] = - (np.cos(np.deg2rad(theta2)) - np.cos(np.deg2rad(theta1)))
    matrix[1, 1] = - (np.cos(np.deg2rad(theta3)) - np.cos(np.deg2rad(theta2)))

    # Get the location values
    rot_center_loc = np.dot(np.linalg.inv(matrix), np.array([r, s]))

    return rot_center_loc


def get_delta_t1_x(theta_old, theta_new, rotation_center):
    """
    Get the change of t1_x such that during the energy scan, the split ratio does not change.

    :param theta_old:
    :param theta_new:
    :param rotation_center:
    :return:
    """
    delta_sine = np.sin(np.deg2rad(theta_new)) - np.sin(np.deg2rad(theta_old))
    delta_cosine = np.cos(np.deg2rad(theta_new)) - np.cos(np.deg2rad(theta_old))

    delta_t1_x = - (rotation_center[0] * delta_sine +
                    rotation_center[1] * delta_cosine)

    return delta_t1_x


def get_delta_t6_x(theta_old, theta_new, rotation_center):
    """
    Get the change of t1_x such that during the energy scan, the split ratio does not change.

    :param theta_old:
    :param theta_new:
    :param rotation_center:
    :return:
    """
    delta_sine = np.sin(np.deg2rad(theta_new)) - np.sin(np.deg2rad(theta_old))
    delta_cosine = np.cos(np.deg2rad(theta_new)) - np.cos(np.deg2rad(theta_old))

    delta_t6_x = rotation_center[0] * delta_sine - rotation_center[1] * delta_cosine
    return delta_t6_x
