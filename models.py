import peewee

db = peewee.SqliteDatabase("f1.db")


class Pilots(peewee.Model):
    class Meta:
        database = db

    abbreviation = peewee.CharField(unique=True, max_length=3)
    name = peewee.CharField()
    team = peewee.CharField()


class Qualifications(peewee.Model):
    class Meta:
        database = db
        indexes = (
            (("start_lap", "end_lap"), True),
        )

    start_lap = peewee.DateTimeField()
    end_lap = peewee.DateTimeField()
    grand_prix = peewee.CharField()
    season = peewee.SmallIntegerField()
    pilot = peewee.ForeignKeyField(Pilots)


def init_db():
    # db.drop_tables([Pilots, Qualifications], safe=True)
    db.create_tables([Pilots, Qualifications], safe=True)


if __name__ == "__main__":
    init_db()
