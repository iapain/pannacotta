from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import permalink
from django.contrib.auth.models import User
from django.conf import settings
 
import datetime
from apps.accounts.models import Account
 
 
class Category(models.Model):
    """Category model."""
    title = models.CharField(_('title'), max_length=100)
    slug = models.SlugField(_('slug'), unique=True)
    user = models.ForeignKey(User)
    account = models.ForeignKey(Account)
 
    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        db_table = 'blog_categories'
        ordering = ('title',)

 
    def __unicode__(self):
        return u'%s' % self.title
 
    @permalink
    def get_absolute_url(self):
        return ('blog_category_detail', None, {'slug': self.slug})
 
 
class Post(models.Model):
    """Post model."""
    STATUS_CHOICES = (
        (1, _('Draft')),
        (2, _('Public')),
    )
    title = models.CharField(_('title'), max_length=200)
    slug = models.SlugField(_('slug'), unique_for_date='publish')
    user = models.ForeignKey(User)
    account = models.ForeignKey(Account)
    body = models.TextField(_('body'), )
    tease = models.TextField(_('tease'), blank=True, help_text=_('Concise text suggested. Does not appear in RSS feed.'))
    status = models.IntegerField(_('status'), choices=STATUS_CHOICES, default=2)
    allow_comments = models.BooleanField(_('allow comments'), default=True)
    publish = models.DateTimeField(_('publish'), default=datetime.datetime.now)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)
    categories = models.ManyToManyField(Category, blank=True)
    tags = models.CharField(_('tags'), max_length=200)
 
    class Meta:
        verbose_name = _('post')
        verbose_name_plural = _('posts')
        db_table = 'blog_posts'
        ordering = ('-publish',)
        get_latest_by = 'publish'
 
    def __unicode__(self):
        return u'%s' % self.title
 
    @permalink
    def get_absolute_url(self):
        return ('blog_detail', None, {
            'year': self.publish.year,
            'month': self.publish.strftime('%b').lower(),
            'day': self.publish.day,
            'slug': self.slug
        })
 
    def get_previous_post(self):
        return self.get_previous_by_publish(status__gte=2)
 
    def get_next_post(self):
        return self.get_next_by_publish(status__gte=2)
 