from gitlabui import app


def main():
    app.run(debug=True, use_debugger=True, use_reloader=True, passthrough_errors=True, host='0.0.0.0')
