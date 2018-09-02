from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_config import Base, Starships, User

engine = create_engine('sqlite:///fleet.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine


DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy user
User1 = User(name="I Robot", email="",
             image='')
session.add(User1)
session.commit()


# Create starting starships
starship1 = Starships(user_id=1, name="USS Enterprise", description="""Fisrt
                      ship on the series, commanded by Pyke and Kirk.
                      Has Spock.""",
                      category="NCC-1701")

session.add(starship1)
session.commit()


starship2 = Starships(user_id=1, name="USS Voyager", description="""Primary
                      setting of Star Trek: Voyager : (TV Series) . Commanded
                      by Captain Kathryn Janeway.
                      Commanded by Captain Chakotay in
                      the "Enemy of My Enemy" book series, then commanded by
                      Captain Afsarah Eden in the novel Unworthy,
                      then by Captain Chakotay as final commander in the novels
                      Full Circle and Children of the Storm.""",
                      category="NCC-74656")

session.add(starship2)
session.commit()


starship3 = Starships(user_id=1, name="USS Defiant", description="""The ship is
                      lost in an interdimensional rift in "The Tholian Web".
                      Later, it is revealed she was taken by Mirror Universe
                      Tholians, captured by the crew of ISS Enterprise (NX-01),
                      and then used in the service of the Terran Empire in
                      "In a Mirror, Darkly".The Defiant is mentioned,
                      but not seen (except for a wireframe graphic) in
                      Star Trek Discovery, Season One.""",
                      category="NCC-1764")

session.add(starship3)
session.commit()


starship4 = Starships(user_id=1, name="ISS Enterprise", description="""Mirror
                      Universe version of Enterprise.""", category="NCC-1701")

session.add(starship4)
session.commit()


starship5 = Starships(user_id=1, name="USS Discovery", description="""The USS
                      Discovery  was a 23rd century Federation Crossfield-class
                      starship operated by Starfleet, under the command of
                      Captain Gabriel Lorca and, later, acting captain Saru""",
                      category="NCC-1031")

session.add(starship5)
session.commit()


starship6 = Starships(user_id=1, name="ISS Discovery", description="""Terran
                      Crossfield-class starship that was in service to
                      Starfleet in the mid-23rd century. The vessel was under
                      the command of Captain Sylvia Tilly, who rose to the
                      position after killing the previous captain.""",
                      category="NCC-1031")

session.add(starship6)
session.commit()


print "Launched Ships!"
