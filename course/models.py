from django.db import models
from django.contrib.auth import get_user_model

LANGUAGE = [
    ('fa', 'فارسی'),
    ('en', 'English'),
]


class CategoryModel(models.Model):

    class Meta:
        verbose_name = 'موضوع'
        verbose_name_plural = 'موضوعات'

    title = models.CharField(max_length=100, blank=True)
    short_description = models.TextField(
        blank=True, null=True, max_length=1000)
    image = models.ImageField(
        upload_to="course_category/", blank=True, null=True
    )

    def __str__(self):
        return str(self.title)


class LessonModel(models.Model):
    title = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # Todo: modify when update field.
    modify_at = models.DateTimeField(auto_now=True)
    short_description = models.TextField(
        blank=True, null=True, max_length=1000)


class SectionModel(models.Model):
    title = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    short_description = models.TextField(
        blank=True, null=True, max_length=1000)
    lessons = models.ManyToManyField(
        to=LessonModel, related_name="section_of_lesson")


class CourseModel(models.Model):

    class Meta:
        verbose_name = 'دوره'
        verbose_name_plural = 'دوره‌ها'

    title = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    short_description = models.TextField(
        blank=True, null=True, max_length=1000)
    category = models.ForeignKey(
        to=CategoryModel, blank=True, null=True, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to="course/", blank=True, null=True
    )
    language = models.CharField(
        choices=LANGUAGE, max_length=2, blank=True, null=True)
    price = models.BigIntegerField(null=True, blank=True)
    discount_price = models.BigIntegerField(
        null=True, blank=True
    )
    sections = models.ManyToManyField(
        to=SectionModel, related_name="course_of_section")

    def __str__(self):
        return str(self.title)


class CourseReviewModel(models.Model):
    class Meta:
        verbose_name = 'نقد دوره‌'
        verbose_name_plural = 'نقد‌های دوره'

    course = models.ForeignKey(to=CourseModel, on_delete=models.CASCADE)
    author = models.ForeignKey(
        get_user_model(), related_name="course_review", on_delete=models.CASCADE
    )
    subject = models.CharField(max_length=50, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes_count = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)

    def get_total_likes(self):
        return self.review_likes.users.count()

    def get_total_dis_likes(self):
        return self.review_dis_likes.users.count()

    def __str__(self):
        return str(self.description)[:30]


class CourseReviewLikeModel(models.Model):
    class Value(models.IntegerChoices):
        UP = 1
        DOWN = -1

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    review = models.ForeignKey(CourseReviewModel, on_delete=models.CASCADE)
    value = models.IntegerField(choices=Value.choices)

    def create(self, *args, **kwargs):
        self.review.likes_count += 1
        self.review.likes += self.value
        super(CourseReviewLikeModel, self).save(*args, **kwargs)

    def update(self, *args, **kwargs):
        super(CourseReviewModel, self).update(*args, **kwargs)


class CourseLikeModel(models.Model):
    course = models.OneToOneField(
        CourseModel, related_name="course_likes", on_delete=models.CASCADE
    )
    users = models.ManyToManyField(
        get_user_model(), related_name="user_course_likes"
    )

    def __str__(self):
        return self.course.title

    @classmethod
    def like(cls, course, user):
        course.likes += 1
        course.save()
        course_like = cls.objects.get(course=course)
        course_like.users.set([user])
        return course_like

    @classmethod
    def undo_like(cls, course, user):
        course.likes -= 1
        course.save()
        course_like = cls.objects.get(course=course).users.remove(user)
        return course_like
