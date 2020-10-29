import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import wave

from app import app, db
from models import *


app.config.from_object(os.environ['APP_SETTINGS'])

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def load_dataset(dataset_dirpath, dataset_name, dataset_url):
    ds = Dataset(name=dataset_name, url=dataset_url)
    db.session.add(ds)
    db.session.commit()
    sub_dirs = [x for x in os.walk(dataset_dirpath)][1:]
    #labels = [sd.split('/')[1]for sd[0] in sub_dirs]
    for sd in sub_dirs:
        # create label
        label_name = sd[0].split('/')[1]
        label = Label(name=label_name)
        db.session.add(label)
        files = sd[2]
        for f in files:
            # get name
            fname = label_name + '/' + f
            # get sample rate
            with wave.open(dataset_dirpath + '/' + fname, 'rb') as ff:
                sr = f.getframerate()
            # now add file to DB
            print('adding {} to db'.format(fname))
            db.session.add(AudioFile(name=fname,
                                     sample_rate=sr, dataset_id=ds.id,
                                     label_id=label.id))
            db.session.commit()

    with wave.open(file, 'rb') as f:
        framerate = f.getframerate()


if __name__ == '__main__':
    manager.run()
