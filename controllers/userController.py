from database import SessionLocal
from info_classes import UserInfo, MessageInfo, ServerInfo, MessageType
from models import User, Server, Message, ServerMember

db = SessionLocal()

# 1. Create a plain UserInfo object (as you already do)
user_data = UserInfo(userName="jerry", password="hashed_pw", profileImage="img.png", isAdmin=False)

# 2. Convert it into a DB model and save it
user = User(
    username=user_data.userName,
    password=user_data.password,
    profile_image=user_data.profileImage,
    is_admin=user_data.isAdmin
)
db.add(user)
db.commit()
db.refresh(user)  # now user.user_id is populated

db.close()


def to_db(self):
    from models import User
    return User(
        username=self.userName,
        password=self.password,
        profile_image=self.profileImage,
        is_admin=self.isAdmin
    )

user_data = UserInfo(userName="jerry", password="hashed_pw", profileImage="img.png", isAdmin=False)
db.add(user_data.to_db())
db.commit()

