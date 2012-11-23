from django.db import models
from django.utils.translation import ugettext_lazy as _


class Question(models.Model):
    question = models.CharField(
        max_length=256,
        default=u"Jaki to utwor?",
        verbose_name=_(u"question"))
    answer = models.CharField(
        max_length=256,
        verbose_name=_(u"answer"))
    sound = models.FileField(
        upload_to='sounds',
        verbose_name=_(u"sound"))

    class Meta:
        verbose_name = _(u"question")
        verbose_name_plural = _(u"questions")
        ordering = []

    def __unicode__(self):
        return "{0} - {1}".format(self.question, self.answer)


class Participant(models.Model):

    user = models.ForeignKey(
        to='auth.User',
        blank=True,
        null=True,
        verbose_name=_(u"user"))

    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_(u"timestamp"))

    ip = models.IPAddressField(
        verbose_name=_(u"ip"))

    queue = models.CommaSeparatedIntegerField(
        max_length=512,
        verbose_name=_(u"queue"))

    class Meta:
        verbose_name = _(u"participant")
        verbose_name_plural = _(u"participants")

    def __unicode__(self):
        return ""


class Answer(models.Model):

    participant = models.ForeignKey(
        to=Participant,
        related_name='answers',
        verbose_name=_(u"participant"))

    question = models.ForeignKey(
        to=Question,
        related_name='answers',
        verbose_name=_(u"question"))

    answer = models.CharField(
        max_length=256,
        verbose_name=_(u"user_answer"))

    valid = models.BooleanField(
        verbose_name=_(u"valid"))

    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_(u"timestamp"))

    class Meta:
        verbose_name = _(u"answer")
        verbose_name_plural = _(u"answers")

    def __unicode__(self):
        return ""
