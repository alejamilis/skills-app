import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType
from app.model import User as UserModel, Profile as ProfileModel, Skill as SkillModel


class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        interfaces = (relay.Node,)


class Profile(SQLAlchemyObjectType):
    class Meta:
        model = ProfileModel
        interfaces = (relay.Node,)

    skills = graphene.List(lambda: Skill, name=graphene.String(), score=graphene.Int())

    def resolve_skills(self, info, name=None, score=None):
        query = Skill.get_query(info=info)
        query = query.filter(SkillModel.profile_id == self.id)
        if name:
            query = query.filter(SkillModel.name == name)
        if score:
            query = query.filter(SkillModel.score == score)

        return query.all()


class Skill(SQLAlchemyObjectType):
    class Meta:
        model = SkillModel
        interfaces = (relay.Node,)


class SkillInput(graphene.InputObjectType):
    name = graphene.String()
    score = graphene.Int()
