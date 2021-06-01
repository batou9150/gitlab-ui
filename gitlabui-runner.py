#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gitlabui import app

if __name__ == "__main__":
    app.run(debug=True, use_debugger=True, use_reloader=True, passthrough_errors=True, host='0.0.0.0')
