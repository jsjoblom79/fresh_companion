import webview
from data.dataApi import DataApi

api = DataApi()



if __name__ == '__main__':
    webview.create_window('Fresh Companion Followup','index.html')
    webview.start(debug=True)