import shutil
import tempfile
import time

from django import forms
from django.conf import settings
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Comment, Follow, Group, Post, User
from yatube.settings import HTML_S, YATUBE_CONST


class AllViewsTests(TestCase):

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username="StasBasov")
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.group = Group.objects.create(
            title="Заголовок",
            slug="test_slug",
        )
        self.author = User.objects.create(
            username="test_name",
        )
        self.post = Post.objects.create(
            author=self.author,
            text="Текст, написанный для проверки",
            group=self.group,
        )

    def test_pages_uses_correct_template(self):
        templates_pages_names = {
            reverse("posts:index"): "posts/index.html",
            reverse(
                "posts:group_list", kwargs={"slug": self.group.slug}
            ): "posts/group_list.html",
            reverse(
                "posts:profile", kwargs={"username": self.author.username}
            ): "posts/profile.html",
            reverse(
                "posts:post_detail", kwargs={"post_id": self.post.id}
            ): "posts/post_detail.html",
            reverse(
                "posts:post_edit", kwargs={"post_id": self.post.id}
            ): "posts/create_post.html",
            reverse("posts:post_create"): "posts/create_post.html",
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)





