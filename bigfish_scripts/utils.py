# -*- coding: utf-8 -*-
# Author: Arthur Imbert <arthur.imbert.pro@gmail.com>
# License: BSD 3 clause

"""Routine functions."""

import os
import time
import datetime
import sys
import inspect
import shutil
import bigfish.stack as stack


def check_directories(path_directories):
    # check directories exist
    stack.check_parameter(path_directories=list)
    for path_directory in path_directories:
        if not os.path.isdir(path_directory):
            raise ValueError("Directory does not exist: {0}"
                             .format(path_directory))

    return


def initialize_script(log_directory, experiment_name=None):
    # check parameters
    stack.check_parameter(log_directory=str)
    stack.check_parameter(experiment_name=(str, type(None)))

    # get filename of the script that call this function
    try:
        previous_filename = inspect.getframeinfo(sys._getframe(1))[0]
    except ValueError:
        previous_filename = None

    # get date of execution
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d %H:%M:%S")
    year = date.split("-")[0]
    month = date.split("-")[1]
    day = date.split("-")[2].split(" ")[0]
    hour = date.split(":")[0].split(" ")[1]
    minute = date.split(":")[1]
    second = date.split(":")[2]

    # format log name
    log_date = year + month + day + hour + minute + second
    if previous_filename is not None:
        operation = os.path.basename(previous_filename)
        operation = operation.split(".")[0]
        if experiment_name is not None:
            log_name = "{0}_{1}_{2}".format(
                log_date, operation, experiment_name)
        else:
            log_name = "{0}_{1}".format(log_date, operation)
    else:
        if experiment_name is not None:
            log_name = "{0}_{1}".format(log_date, experiment_name)
        else:
            log_name = "{0}".format(log_date)

    # initialize logging in a specific log directory
    path_log_directory = os.path.join(log_directory, log_name)
    os.mkdir(path_log_directory)
    path_log_file = os.path.join(path_log_directory, "log")
    sys.stdout = Logger(path_log_file)

    # copy python script in the log directory
    if previous_filename is not None:
        path_output = os.path.join(path_log_directory,
                                   os.path.basename(previous_filename))
        shutil.copyfile(previous_filename, path_output)

    # print information about launched script
    if previous_filename is not None:
        print("Running {0} file..."
              .format(os.path.basename(previous_filename)))
        print()
    start_time = time.time()
    if experiment_name is not None:
        print("Experiment name: {0}".format(experiment_name))
    print("Log directory: {0}".format(log_directory))
    print("Log name: {0}".format(log_name))
    print("Date: {0}".format(date), "\n")

    return start_time


def end_script(start_time):
    # check parameters
    stack.check_parameter(start_time=(int, float))

    # time the script
    end_time = time.time()
    duration = int(round((end_time - start_time) / 60))
    print("Duration: {0} minutes".format(duration), "\n")

    return


class Logger(object):
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log = open(filename, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        # this flush method is needed for python 3 compatibility.
        # this handles the flush command by doing nothing.
        # you might want to specify some extra behavior here.
        pass

