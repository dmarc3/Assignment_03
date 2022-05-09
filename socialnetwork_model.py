import os
import peewee as pw
from loguru import logger

file = 'users.db'
if os.path.exists(file):
    os.remove(file)

db = pw.SqliteDatabase(file)


class BaseModel(pw.Model):
    logger.info('allows database to be defined changed in one place')

    class Meta:
        database = db


class Users(BaseModel):
    """
    This class defines Users, which maintains details of someone for whom we want to add to the social media.
    """

    user_id = pw.CharField(primary_key=True, max_length=30)
    user_email = pw.CharField()
    user_name = pw.CharField(max_length=30)
    user_last_name = pw.CharField(max_length=100)

    def show(self):
        """ display an instance """
        print(self.user_id, self.email, self.user_name, self.user_last_name)


def main():
    """add and print some records """
    db.connect()
    db.execute_sql('PRAGMA foreign_keys=ON;')
    db.create_tables([
        Users
    ])

    people = [
        ('kwong', 'k@gmail.com', 'Kathleen', 'Wong'),
        ('pwong', 'p@gmail.com', 'Peter', 'Wong'),
    ]

    for person in people:
        try:
            with db.transaction():
                new_person = Users.create(
                    user_id=person[0],
                    email=person[1],
                    user_name=person[2],
                    user_last_name=person[3],)
                new_person.save()

        except Exception as e:
            logger.info(f'Error creating person = {person[0]}')
            logger.info(e)
            logger.info('See how the database protects our data')

    try:
        with db.transaction():
            new_person = Users.delete(
                user_id='kwong')
            new_person.save()

    except Exception as e:
        logger.info(f'Error creating person = kwong')
        logger.info(e)
        logger.info('See how the database protects our data')

    for person in Users:
        person.show()


if __name__ == '__main__':
    main()