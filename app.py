import webview
from data.dataApi import DataApi
from screeninfo import get_monitors

class NavigationApi:
    def __init__(self):
        self.db = DataApi()

    def load_task_detail(self, task_id):
        task = self.db.get_task(task_id)
        window.load_url('assets/task.html')

    def close_app(self):
        webview.windows[0].destroy()

    def navigate_home(self):
        window.load_url('index.html')

api = NavigationApi()



if __name__ == '__main__':
    monitor_width = get_monitors()[0].width
    monitor_height = get_monitors()[0].height

    window = webview.create_window(
        'Fresh Companion Followup',
        'index.html',
        js_api=api,
        width= int (monitor_width / 2),
        height=monitor_height,
        frameless=True,
        easy_drag=True,
        on_top=True
    )
    webview.start(debug=True)