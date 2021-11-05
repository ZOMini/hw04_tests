from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый текст',
        )

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        # Проверяем Group
        str_group = self.group
        title_group = self.group.title
        self.assertEqual(title_group, str(str_group))
        # Проверяем Post
        str_post = self.post
        text_post = self.post.text[:15]
        self.assertEqual(text_post, str(str_post))

    def test_verbose_name(self):
        """Test verbose_name"""
        self.post = PostModelTest.post
        verbose_field = {
            'text': 'Текст поста',
            'pub_date': 'Дата поста',
            'author': 'Автор',
            'group': 'Группа',
        }

        for field, value in verbose_field.items():
            with self.subTest(field=field):
                self.assertEqual(
                    self.post._meta.get_field(field).verbose_name, value)

    def test_help_text_in_post_model(self):
        """Test help_text"""
        self.post = PostModelTest.post
        help_field = {
            'text': 'Введите текст поста',
            'group': 'Выберите группу',
        }

        for field, value in help_field.items():
            with self.subTest(field=field):
                self.assertEqual(
                    self.post._meta.get_field(field).help_text, value)
