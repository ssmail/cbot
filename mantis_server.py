# -*- coding: utf-8 -*-
# !/usr/bin/env python
# author = Chris Hong


from mantis import mantis_server

if __name__ == '__main__':
    mantis_server.run(host="127.0.0.1", port=5000, debug=True)
