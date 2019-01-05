import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, CategoryItem

# Tell application which database engine we want to use. We will use SQLite3
# Create sqlite3 database file
#engine = create_engine('sqlite:///database.db')
engine = create_engine('postgresql://catalog:grader@localhost/catalog')

# Bind engine to Base class, creating connection between our class definitions
# and their corrisponding tables
Base.metadata.bind = engine

# Create a sessionmaker object which is a line of communication between our
# code and the database engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create dummy data to populate our app with starter data

# Create inital users:
user = User(
    name='Johnny Noname',
    email='thewickk@thewickk.com',
    picture='some_pic.jpg'
)

session.add(user)
session.commit()

user = User(
    name='Jane Doe',
    email='jandoe@aol.com',
    picture='another_selfie.png'
)

session.add(user)
session.commit()

# Baseball Category and Items:
category = Category(
    name='Baseball',
    user_id=1
)

session.add(category)
session.commit()

item = CategoryItem(
    name='Baseball Glove',
    description='A leather mitt for shagging fly balls!',
    creation_date=datetime.datetime.now(),
    category=category
    # user = user
)

session.add(item)
session.commit()

item = CategoryItem(
    name='Baseball Cleats',
    description='Metal spikes for extra traction',
    creation_date=datetime.datetime.now(),
    category=category
    # user = user
)

session.add(item)
session.commit()

item = CategoryItem(
    name='Baseball Bat',
    description='Louisville Slugger for smashing home runs',
    creation_date=datetime.datetime.now(),
    category=category
    # user = user
)

session.add(item)
session.commit()

# Surfing Category and Items
category = Category(
    name='Surfing',
    user_id=1
)

session.add(category)
session.commit()

item = CategoryItem(
    name='Surfboard',
    description='The lateste technology for the best performance!',
    creation_date=datetime.datetime.now(),
    category=category
    # user = user
)

session.add(item)
session.commit()

item = CategoryItem(
    name='Wetsuit',
    description='Helps keep you warm in cold water weather',
    creation_date=datetime.datetime.now(),
    category=category
    # user = user
)

session.add(item)
session.commit()

# Camping Category and Items
category = Category(
    name='Camping',
    user_id=2
)

session.add(category)
session.commit()

item = CategoryItem(
    name='Tent',
    description='Portable shelter',
    creation_date=datetime.datetime.now(),
    category=category
    # user = user
)

session.add(item)
session.commit()

item = CategoryItem(
    name='Compass',
    description='Find your direction in any weather',
    creation_date=datetime.datetime.now(),
    category=category
    # user = user
)

session.add(item)
session.commit()

# Golfing Category and Items
category = Category(
    name='Golf',
    user_id=2
)

session.add(category)
session.commit()

item = CategoryItem(
    name='Golf Club',
    description='Used for hitting golf balls',
    creation_date=datetime.datetime.now(),
    category=category
    # user = user
)

session.add(item)
session.commit()

item = CategoryItem(
    name='Golf Bag',
    description='Used to carry golfing equipment',
    creation_date=datetime.datetime.now(),
    category=category
    # user = user
)

session.add(item)
session.commit()
