import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data.data_models import Tasks, Notes, TimeTracking
from fresh_companion_repo import FreshCompanionRepo

with open('../config/config.json', 'r') as file:
    config = json.load(file)


class DataApi:
    def __init__(self):
        self.engine = create_engine(config['database']['connection_string'])
        self.Session = sessionmaker(bind=self.engine)
        self.db = self.Session()

        self.repo = FreshCompanionRepo(self.db)
