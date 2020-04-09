import graphene

from app import db
from app.graphql.object import SkillInput, User as User, Profile as Profile
from app.model import User as UserModel, Profile as ProfileModel, Skill as SkillModel


class UserMutation(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        name = graphene.String(required=True)
        last_name = graphene.String(required=True)

    user = graphene.Field(lambda: User)

    def mutate(self, info, username, name, last_name):
        user = UserModel(username=username, name=name, last_name=last_name)

        db.session.add(user)
        db.session.commit()

        return UserMutation(user=user)


class ProfileMutation(graphene.Mutation):
    class Arguments:
        role = graphene.String(required=True)
        description = graphene.String(required=True)
        user_id = graphene.Int(required=True)
        skills = graphene.List(SkillInput)
        id = graphene.Int()

    profile = graphene.Field(lambda: Profile)

    def mutate(self, info, role, description, user_id, skills):
        user = UserModel.query.get(user_id)

        profile = ProfileModel(role=role, description=description)
        # Create skills
        skill_list = [SkillModel(name=input_skill.name, score=input_skill.score) for input_skill in skills]
        profile.skills.extend(skill_list)

        db.session.add(profile)

        # Update user
        user.profile = profile

        db.session.commit()

        return ProfileMutation(profile=profile)


class Mutation(graphene.ObjectType):
    mutate_user = UserMutation.Field()
    mutate_profile = ProfileMutation.Field()
