from app import db
from sqlalchemy.dialects.postgresql import JSON


class Dataset(db.Model):
    __tablename__ = 'dataset'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    url = db.Column(db.String())

    def __init__(self, name, url):
        self.name = name
        self.url = url

    def __repr__(self):
        return '<Dataset id {}>'.format(self.id)


class AudioFile(db.Model):
    __tablename__ = 'audiofile'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    sample_rate = db.Column(db.Integer)
    dataset_id = db.Column(db.Integer, db.ForeignKey('dataset.id'))
    label_id = db.Column(db.Integer, db.ForeignKey('label.id'))
    text = db.Column(JSON)

    def __init__(self, name, sample_rate, dataset_id, label_id, text={}):
        self.name = name
        self.sample_rate = sample_rate
        self.dataset_id = dataset_id
        self.label_id = label_id
        self.text = text

    def __repr__(self):
        return '<AudioFile id {}>'.format(self.id)


class Label(db.Model):
    __tablename__ = 'label'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Label id {}>'.format(self.id)

