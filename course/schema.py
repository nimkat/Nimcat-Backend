import graphene
from django.contrib.auth import get_user_model
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id


from .models import (
    CourseLikeModel,
    CourseModel,
    CourseCategoryModel,
    CourseReviewModel,
    CourseReviewLikeModel,
    CourseLessonModel,
    CourseSectionModel,
)
from .types import (
    CourseCategoryType,
    CourseLessonType,
    CourseLikeType,
    CourseReviewLikeType,
    CourseReviewType,
    CourseSectionType,
    CourseType,
)

from user.models import BoughtCoursesModel


class Query(graphene.AbstractType):
    course = relay.Node.Field(CourseType)
    all_courses = DjangoFilterConnectionField(CourseType)

    course_category = relay.Node.Field(CourseCategoryType)
    all_course_categories = DjangoFilterConnectionField(CourseCategoryType)

    course_likes = relay.Node.Field(CourseLikeType)
    all_course_likes = DjangoFilterConnectionField(CourseLikeType)

    my_courses = relay.Node.Field(CourseType)
    all_my_courses = DjangoFilterConnectionField(CourseType)

    course_review = relay.Node.Field(CourseReviewType)
    all_course_review = DjangoFilterConnectionField(CourseReviewType)

    def resolve_trip(self, info):
        return CourseModel.objects.filter(published=True)

    def resolve_all_trip(root, info, **kwargs):
        return CourseModel.objects.filter(published=True)

    def resolve_all_trip_review(self, info):
        return CourseReviewModel.objects.all()

    def resolve_categories(self, info):
        return CourseCategoryModel.objects.all()

    def resolve_my_courses(self, info):
        user = info.context.user
        bought_courses = BoughtCoursesModel.objects.filter(
            user=user).values("course")
        courses = CourseModel.objects.filter(pk__in=bought_courses).order_by(
            "-created_at"
        )
        return courses


class CreateCourseReview(relay.ClientIDMutation):
    class Input:
        course_id = graphene.ID(required=True)
        subject = graphene.String()
        description = graphene.String(required=True)

    review = graphene.Field(CourseReviewType)
    success = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, course_id, subject, description):
        user = info.context.user
        course = CourseModel.objects.get(pk=from_global_id(course_id)[1])
        review = CourseReviewModel.objects.create(
            user=user, subject=subject, description=description
        )
        course.reviews.add(review)
        return CreateCourseReview(review=review, success=True)


class UpdateCourseReview(graphene.Mutation):
    """update course review mutation."""

    review = graphene.Field(CourseReviewType)
    success = graphene.Boolean()

    class Input:
        course_review_id = graphene.ID()
        subject = graphene.String(required=True)
        description = graphene.String(required=True)

    def mutate(self, info, course_review_id, **kwargs):
        course_review = CourseReviewModel.objects.get(
            pk=(from_global_id(trip_review_id)[1])
        )
        for key, value in kwargs.items():
            setattr(course_review, key, value)
        course_review.save()
        return UpdateCourseReview(review=course_review, success=True)


class DeleteCourseReview(graphene.Mutation):
    """delete course review mutation."""

    deleted = graphene.Boolean()

    class Arguments:
        course_review_id = graphene.ID(required=True)

    @classmethod
    def mutate(cls, root, info, course_review_id):
        course_review = CourseReviewModel.objects.get(
            pk=from_global_id(course_review_id)[1])
        course_review.delete()
        return cls(deleted=True)


class CreateCourseLike(graphene.Mutation):
    class Arguments:
        course_id = graphene.ID(required=True)

    success = graphene.Boolean()
    like = graphene.Boolean()

    @staticmethod
    def mutate(root, info, courseid):
        user = info.context.user
        course_like = CourseLikeModel.objects.filter(
            course=from_global_id(trip_id)[1])
        course = CourseModel.objects.get(pk=from_global_id(trip_id)[1])
        if not course_like:
            CourseLikeModel.like(course=course, user=user)
            like = True
        else:
            trip_like = CourseLikeModel.objects.get(course=course)
            like_user = get_user_model().objects.filter(
                user_course_likes__id=course_like.id
            )
            if like_user:
                course_like.undo_like(course, user)
                like = False
            else:
                course_like.like(course, user)
                like = True
        success = True
        return CreateCourseLike(success=success, like=like)


class Mutation(graphene.ObjectType):
    create_course_like = CreateCourseLike.Field()
    create_course_review = CreateCourseReview.Field()

    update_course_review = UpdateCourseReview.Field()

    delete_course_review = DeleteCourseReview.Field()
