from user.models import BoughtCoursesModel
from graphene import relay
from graphene.types.generic import GenericScalar
from graphene_django import DjangoObjectType

from .models import (
    CourseLikeModel,
    CourseModel,
    CourseCategoryModel,
    CourseReviewModel,
    CourseReviewLikeModel,
    CourseLessonModel,
    CourseSectionModel,
)

from common.util.Video import get_secure_video_link

from graphql_relay import from_global_id
from django.utils.translation import gettext as _


class CourseType(DjangoObjectType):

    def resolve_image(self, info):
        """Resolve product image absolute path"""
        if self.image:
            self.image = info.context.build_absolute_uri(self.image.url)
        return self.image

    def resolve_video(self, info):
        """Resolve vodeo url secure path"""
        if self.video:
            self.video = get_secure_video_link(info.context, self.video)
        return self.video

    class Meta:
        model = CourseModel
        interfaces = (relay.Node,)
        filter_fields = {'category': ['exact'],
                         'category__title': ['exact'], }
        fields = "__all__"
        description = "Course list"  # way to add description


class SecureCourseType(DjangoObjectType):

    def resolve_image(self, info):
        """Resolve product image absolute path"""
        if self.image:
            self.image = info.context.build_absolute_uri(self.image.url)
        return self.image

    def resolve_video(self, info):
        """Resolve vodeo url secure path"""
        if self.video:
            self.video = get_secure_video_link(info.context, self.video)
        return self.video

    class Meta:
        model = CourseModel
        interfaces = (relay.Node,)
        filter_fields = {'category': ['exact'],
                         'category__title': ['exact'], }
        fields = "__all__"
        description = "Course list"  # way to add description

    @classmethod
    def get_node(cls, info, **kwargs):
        id = kwargs.get["id"]
        user = info.context.user
        if user.is_authenticated:
            print(id)
            course_id = from_global_id(id)[1]
            bought_courses = BoughtCoursesModel.objects.filter(
                user=user).values("course")
            print(bought_courses)
        return _("Not Authenticated")


class CourseCategoryType(DjangoObjectType):

    def resolve_image(self, info):
        """Resolve product image absolute path"""
        if self.image:
            self.image = info.context.build_absolute_uri(self.image.url)
        return self.image

    class Meta:
        model = CourseCategoryModel
        filter_fields = ['title']
        interfaces = (relay.Node,)
        fields = "__all__"


class CourseSectionType(DjangoObjectType):
    def resolve_video(self, info):
        """Resolve vodeo url secure path"""
        if self.video:
            self.video = get_secure_video_link(info.context, self.video)
        return self.video

    class Meta:
        model = CourseSectionModel
        filter_fields = "__all__"
        interfaces = (relay.Node,)
        fields = "__all__"


class CourseLessonType(DjangoObjectType):
    def resolve_video(self, info):
        """Resolve vodeo url sequre path"""
        if self.video:
            self.video = get_secure_video_link(info.context, self.video)
        return self.video

    class Meta:
        model = CourseLessonModel
        filter_fields = "__all__"
        interfaces = (relay.Node,)
        fields = "__all__"


class CourseReviewLikeType(DjangoObjectType):
    class Meta:
        model = CourseReviewLikeModel
        filter_fields = "__all__"
        interfaces = (relay.Node,)
        fields = "__all__"


class CourseReviewType(DjangoObjectType):
    class Meta:
        model = CourseReviewModel
        filter_fields = "__all__"
        interfaces = (relay.Node,)
        fields = "__all__"


class CourseLikeType(DjangoObjectType):
    class Meta:
        model = CourseLikeModel
        filter_fields = "__all__"
        interfaces = (relay.Node,)
        fields = "__all__"
