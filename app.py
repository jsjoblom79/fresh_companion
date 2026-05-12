import webview
from data.dataApi import DataApi

api = DataApi()



if __name__ == '__main__':
    window = webview.create_window('Fresh Companion Followup','index.html', js_api=api, width=1160, frameless=True, easy_drag=True)
    webview.start(debug=True)