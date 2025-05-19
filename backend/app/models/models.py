from datetime import datetime
from ..models.database import db
from werkzeug.security import generate_password_hash, check_password_hash

class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, nullable=False)  # 会话 ID
    user = db.Column(db.String(10), nullable=False)   # 发送者（"我" 或 "AI"）
    message = db.Column(db.Text, nullable=False)      # 消息内容
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 创建时间

    def to_dict(self):
        return {
            'id': self.id,
            'group_id': self.group_id,
            'user': self.user,
            'message': self.message,
            'created_at': self.created_at.isoformat()
        }

class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False, default="新的会话")
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<Group {self.id}>'

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    nickname = db.Column(db.String(64), nullable=False)
    avatar = db.Column(db.String(255), nullable=True, default='/static/img/avatar.png')
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'user_id': self.id,
            'username': self.username,
            'nickname': self.nickname,
            'avatar': self.avatar,
        }
