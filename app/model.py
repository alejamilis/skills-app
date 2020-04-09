from app import db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), index=True, unique=True)
    name = db.Column(db.String(256))
    last_name = db.Column(db.String(256))
    profile_id = db.Column(db.Integer, db.ForeignKey("profiles.id"))
    profile = db.relationship("Profile")

    def __repr__(self):
        return f"<User {self.username}>"


class Profile(db.Model):
    __tablename__ = "profiles"
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(256))
    description = db.Column(db.Text)
    skills = db.relationship("Skill")

    def __repr__(self):
        return f"<Profile {self.role}>"


class Skill(db.Model):
    __tablename__ = "skills"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    score = db.Column(db.Integer)
    profile_id = db.Column(db.Integer, db.ForeignKey("profiles.id"))

    def __repr__(self):
        return f"<Skill {self.name} with score {self.score}>"
