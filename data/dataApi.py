import json

import webview
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from data.data_models import Tasks, Notes, TimeTracking, Base
from data.fresh_companion_repo import FreshCompanionRepo




class DataApi:
    def __init__(self):
        try:
            with open('config/config.json', 'r') as file:
                config = json.load(file)
        except FileNotFoundError:
            print('Error: config.json file not found.')
            raise
        except json.decoder.JSONDecodeError:
            print("Error: Unable to parse config.json.")
            raise

        try:
            self.engine = create_engine(config['database']['connection_string'])
            self.Session = sessionmaker(bind=self.engine)
            self.db = self.Session()
            Base.metadata.create_all(self.engine)
            # Test the database connection
            self.db.execute(text("SELECT 1"))
        except Exception as e:
            print(f"Database connection failed: {e}")
            raise


        #self.repo = FreshCompanionRepo(self.db)

    def add_task(self, task):
        try:
            return self.repo.add(task)
        except Exception as e:
            print(f"Failed to add task: {e}")
            raise

    def get_task(self, task_id):
        try:
            task = self.repo.get_by_id(task_id)
            if not task:
                print(f"Task {task_id} not found")
                return None
            return task
        except Exception as e:
            print(f"Failed to get task: {e}")
            raise

    def get_all_tasks(self):
        return self.db.query(Tasks).all()

    def close_app(self):
        webview.windows[0].destroy()