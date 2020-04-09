import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField

from app.graphql.object import User as User, Profile as Profile, Skill as Skill
from app.model import User as UserModel


class Query(graphene.ObjectType):
    node = relay.Node.Field()

    users = graphene.List(lambda: User, username=graphene.String())

    def resolve_users(self, info, username=None):
        query = User.get_query(info)
        if username:
            query = query.filter(UserModel.username == username)
        return query.all()

    profiles = SQLAlchemyConnectionField(Profile)
    skills = SQLAlchemyConnectionField(Skill)
