from django.db import models

from django.contrib.auth.models import User


from django.utils.text import slugify
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=200)
    profile_pic = models.ImageField(null=True, blank=True, upload_to="images", default="/user.png")
    bio = models.TextField(null=True, blank=True)
    twitter = models.CharField(max_length=200,null=True, blank=True)

    class Meta:
        ordering = ('-user',)

    def __str__(self):
        name = str(self.first_name)
        if self.last_name:
            name += ' ' + str(self.last_name)
        return name

class Tag(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ('-name',)

    def __str__(self):
        return self.name

class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()

    class Meta:
        ordering = ('-title',)
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return '/%s/' % self.slug

class Post(models.Model):
    ACTIVE = 'active'
    DRAFT = 'draft'

    CHOICES_STATUS = (
        (ACTIVE, 'Active'),
        (DRAFT, 'Draft')
    )

    category = models.ForeignKey(Category, null=True, related_name='posts', blank=True, on_delete=models.CASCADE)
    headline = models.CharField(max_length=200)
    sub_headline = models.CharField(max_length=200, null=True, blank=True)
    intro = models.TextField(null=True, blank=True, max_length=100)
    slug = models.SlugField(null=True, blank=True)
    thumbnail = models.ImageField(null=True, blank=True, upload_to="images", default="/images/placeholder.png")
    body = RichTextUploadingField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, blank=True)
    status = models.CharField(max_length=10, choices=CHOICES_STATUS, default=ACTIVE)


    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.headline

    def get_absolute_url(self):
        return '/%s/%s/' % (self.category.slug, self.slug)


    def save(self, *args, **kwargs):

        if self.slug == None:
            slug = slugify(self.headline)

            has_slug = Post.objects.filter(slug=slug).exists()
            count = 1
            while has_slug:
                count += 1
                slug = slugify(self.headline) + '-' + str(count)
                has_slug = Post.objects.filter(slug=slug).exists()

            self.slug = slug

        super().save(*args, **kwargs)


class PostComment(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        ordering =('-author', 'post')

    def __str__(self):
        return self.body

    @property
    def created_dynamic(self):
        now = timezone.now()
        return now
