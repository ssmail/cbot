# !/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'hongkefeng'

from time import localtime, strftime


class SimpleLog:
    """
        Python build-in log library can not support our requirements
        this log library can show different color according log level
        on console output

        if you don't set log file name, default log file will be "app.log" at
        current work directory

        if you don't want to show log info on console, just init a SimpleLog object as
        debug=False
    """

    def __init__(self, log_file="test.log", debug=True):
        self.log_file = log_file
        self.debug = debug

    def write_log(self, date_time, prefix, content):
        """
        :param: date_time show log date_time :
        :param:prefix: the log level
        :param:content: the log detail content
        :return: None
        """
        self.show_log(colors[prefix] + date_time + " " + prefix,
                      content + u"\033[0m")
        with open(self.log_file, "a") as f:
            f.write(date_time + " " + prefix + " " + content + u"\n")

    def info(self, content):
        """
        :param content: log content
        :return: None
        """
        self.write_log(self.now(), Level.info, content)

    def line_info(self, content, length=30, character="="):
        """
        :param content: log content
        :param length: the string length
        :param character: the line string char

        :Usage:
            line_info('content', )

        :Demo Output:
            2017-10-11 20:20:01 INFO ============= content  ==============
        :return: None
        """
        content = length * character + content + length * character
        self.write_log(self.now(), Level.info, content)

    def warning(self, content):
        """
        :param content: log content
        :return: None
        """
        self.write_log(self.now(), Level.warning, content)

    def line_error(self, content, line_str="-", line_length=30):
        content = line_length * line_str + content + line_length * line_str
        self.write_log(self.now(), Level.error, content)

    def error(self, content):
        """
        :param content: log content
        :return: None
        """
        self.write_log(self.now(), Level.error, content)

    def critical(self, content):
        """
        :param content: log content
        :return: None
        """
        self.write_log(self.now(), Level.critical, content)

    def line_critical(self, content, length=30, character="="):
        """
        :param content: log content
        :param length: the string length
        :param character: the line string char

        :Usage:
            line_info('content', )

        :Demo Output:
            2017-10-11 20:20:01 CRITICAL ============= content  ==============
        :return: None
        """
        content = length * character + content + length * character
        self.write_log(self.now(), Level.critical, content)

    @staticmethod
    def now():
        """
        :return: a string of current date time as a friendly format
        """
        return strftime(u"%Y-%m-%d %H:%M:%S", localtime())

    def show_log(self, prefix, content):
        """
        :param prefix: log level
        :param content: log content
        :return:
        """
        if self.debug:
            print(prefix + u"    " + content)


class Level:
    def __init__(self):
        pass

    info = "INFO    "
    warning = "WARNING "
    error = "ERROR   "
    critical = "CRITICAL"


colors = {
    Level.info: u"\033[94m",
    Level.warning: u"\033[93m",
    Level.error: u"\033[91m",
    Level.critical: u"\033[91m\033[4m",
}


def main():
    log = SimpleLog()
    log.info("this is a test log")
    log.warning("this is error log")
    log.error("this is error log")
    log.critical("this is error log")

    log.line_error("this is error log")
    log.line_info("this is error log")


if __name__ == "__main__":
    main()
