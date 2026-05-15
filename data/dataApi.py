import json
from webview import window
import webview
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from data.data_models import Tasks, Notes, TimeTracking, Base
from data.fresh_companion_repo import FreshCompanionRepo
from datetime import datetime



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


        self.repo = FreshCompanionRepo(self.db)

    def add_task(self, task):
        try:
            new_task = Tasks(**task)
            new_task.followup_date = datetime.fromisoformat(new_task.followup_date.replace('Z', '+00:00'))
            saved_task = self.repo.add(new_task)
            return saved_task.to_dict()
        except Exception as e:
            print(f"Failed to add task: {e}")
            raise

    def get_task(self, task_id):
        try:
            task = self.repo.get_by_id(Tasks,task_id)
            if not task:
                print(f"Task {task_id} not found")
                return None
            return task
        except Exception as e:
            print(f"Failed to get task: {e}")
            raise

    def get_all_tasks(self):
        tasks = self.db.query(Tasks).filter(Tasks.is_completed == False).all()
        return [{
            "id": task.id,
            "title": task.title,
            "description": task.description,
        } for task in tasks]

    def delete_task(self, task_id):
        task = self.get_task(task_id)
        self.repo.delete(task)

    def mark_complete(self, task_id):
        self.repo.complete_task(self.get_task(task_id))



    def get_total_task_count(self):
        tasks = len(self.db.query(Tasks).all())
        completed = len(self.db.query(Tasks).filter(Tasks.is_completed == True).all())
        return {"count": tasks, "completed": completed}

