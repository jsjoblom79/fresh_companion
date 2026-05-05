class FreshCompanionRepo:
    def __init__(self, session):
        self.session = session

    def add(self, item):
        self.session.add(item)
        self.session.commit()
        return item

    def get_by_id(self, model, id):
        return self.session.get(model, id)

    def get_by_model(self, model):
        return self.session.get(model)

    def delete(self, item):
        self.session.delete(item)
        self.session.commit()
        