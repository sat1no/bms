from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
Moduly = Table('Moduly', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR(length=100)),
    Column('value1', INTEGER),
)

Urzadzenia = Table('Urzadzenia', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('nazwa', VARCHAR(length=100)),
    Column('rejestr', INTEGER, nullable=False),
    Column('sterowanie', VARCHAR(length=100)),
    Column('wartosc', INTEGER),
    Column('r', INTEGER),
    Column('g', INTEGER),
    Column('b', INTEGER),
    Column('modul_id', INTEGER),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['Moduly'].drop()
    pre_meta.tables['Urzadzenia'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['Moduly'].create()
    pre_meta.tables['Urzadzenia'].create()
