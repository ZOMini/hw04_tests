from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post

User = get_user_model()


class MyFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_a = User.objects.create_user(username='user_a')
        cls.group = Group.objects.create(
            slug='test-slug',
            title='Тестовая группа',
            description='Тестовое описание',)
        cls.post = Post.objects.create(author=cls.user_a,
                                       text='Тестовый текст',
                                       group=cls.group)

    def setUp(self):
        self.q_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user_a)

    def test_form_create(self):
        posts_count = Post.objects.count()
        form_data = {'text': 'Тестовый текст2'}
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse('posts:profile',
                                               kwargs={'username': 'user_a'}))
        self.assertEqual(posts_count + 1, Post.objects.count())
        self.assertTrue(Post.objects.filter(text='Тестовый текст2').exists())
        self.assertEqual(response.status_code, 200)

    def test_form_edit_post(self):
        """Test edit post"""
        posts_count = Post.objects.count()
        form_data = {'text': 'текст4'}
        response = self.authorized_client.post(
            reverse('posts:post_edit',
                    kwargs={'post_id': f'{self.post.id}'}),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response,
                             reverse('posts:post_detail',
                                     kwargs={'post_id':
                                             self.post.id}))
        self.assertEqual(posts_count, Post.objects.count())
        self.assertTrue(Post.objects.filter(text='текст4').exists())
        self.assertEqual(response.status_code, 200)

    # def test_form_signup(self):
        # """Тест signup"""
        # form_data = {'first_name': 'w23w',
        #              'last_name': 'weetyt3',
        #              'username': 'u2u34',
        #              'email': 'q32423@q5.ru',
        #              'password': 'asqw1m2439A',
        #              'password2': 'asqw1m2439A'}
        # self.q_client.post(reverse('users:signup'), data=form_data,
        #                    follow=True)
        # u_count = User.objects.count()
        # print(f'количество {u_count}')
        # self.assertTrue(User.objects.filter(username='u2u34').exists())
        # u_2 = User.objects.get(username='u2u34')
        # self.assertRedirects(response, reverse('posts:index'))
        # self.assertEqual(form_data['username'],
        #                  u_2.username)
