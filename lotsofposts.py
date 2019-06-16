from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database2_setup import Cause, Base, EffectAnswer, User

engine = create_engine('sqlite:///causeandeffectwithusers.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

user1 = User(name="Vlad", email="cvb.chivu@gmail.com")
session.add(user1)
session.commit()


platform1 = Cause(user_id=1, name="The Environment problem")

session.add(platform1)
session.commit()

effectanswer1 = EffectAnswer(user_id=1, name="silly", solution="drive less",
                             importance="high", area="global", cause=platform1)

session.add(effectanswer1)
session.commit()

effectanswer2 = EffectAnswer(user_id=1, name="gauge", solution="plant more"
                             "trees", importance="high", area="global",
                             cause=platform1)

session.add(effectanswer2)
session.commit()


platform2 = Cause(user_id=1, name="kids with no help")

session.add(platform2)
session.commit()

effectanswer1 = EffectAnswer(user_id=1, name="bob", solution="train more"
                             "teachers", importance="high", area="global",
                             cause=platform2)

session.add(effectanswer1)
session.commit()

effectanswer2 = EffectAnswer(user_id=1, name="jessie", solution="bring more"
                             "involved people", importance="high",
                             area="global", cause=platform2)

session.add(effectanswer2)
session.commit()

platform3 = Cause(user_id=1, name="Unpaved roads")

session.add(platform3)
session.commit()

effectanswer1 = EffectAnswer(user_id=1, name="roxanne", solution="bring more"
                             "funds", importance="medium", area="local",
                             cause=platform3)

session.add(effectanswer1)
session.commit()


print("added menu items!")
