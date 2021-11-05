# posts/tests/test_urls.py
from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from posts.models import Group, Post

User = get_user_model()


class AllURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_a = User.objects.create_user(username='user_a')
        cls.author_p = User.objects.create_user(username='author_p')
        cls.group = Group.objects.create(
            slug='test-slug',
            title='Тестовая группа',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            id='1',
            author=cls.author_p,
            text='Тестовый текст',
            group=cls.group,
        )
        cls.for_guest_test = {
            '/': 200,
            '/about/tech/': 200,
            '/about/author/': 200,
            '/group/test-slug/': 200,
            '/profile/user_a/': 200,
            '/noexisting_page/': 404,
            '/posts/1/': 200,
            '/create/': 302,
            '/posts/1/edit/': 302,
        }
        cls.url_adress = {
            '/': 'posts/index.html',
            '/group/test-slug/': 'posts/group_list.html',
            '/create/': 'posts/create_post.html',
            '/profile/user_a/': 'posts/profile.html',
            '/posts/1/': 'posts/post_detail.html',
            '/posts/1/edit/': 'posts/create_post.html',
            '/about/author/': 'about/author.html',
            '/about/tech/': 'about/tech.html',
            '/auth/signup/': 'users/signup.html',
            '/auth/login/': 'users/login.html',
        }

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client_author = Client()
        self.authorized_client.force_login(self.user_a)
        self.authorized_client_author.force_login(self.author_p)

    def test_url_quest(self):
        """Страницы доступные гостю."""
        for page_url, resp_code in self.for_guest_test.items():
            with self.subTest(page_url=page_url):
                resp = self.guest_client.get(page_url)
                self.assertEqual(resp.status_code, resp_code, page_url)

    def test_url_authorized(self):
        """Страницы доступные авторизованному."""
        response = self.authorized_client.get('/create/')
        self.assertTemplateUsed(response, 'posts/create_post.html')
        resp = self.guest_client.get('/posts/1/edit/')
        self.assertEqual(resp.status_code, 302, 'posts/create_post.html')

    def test_url_authorized_author(self):
        """Страницы доступные автору."""
        response = self.authorized_client_author.get('/posts/1/edit/')
        self.assertTemplateUsed(response, 'posts/create_post.html')

    def test_url_adress(self):
        """Страницы доступные автору."""
        for adress, template in self.url_adress.items():
            with self.subTest(adress=adress):
                response = self.authorized_client_author.get(adress)
                self.assertTemplateUsed(response, template)
        response = self.authorized_client_author.get('/create/')
        self.assertTemplateUsed(response, 'posts/create_post.html')

    # def test_url_quest_response_redirect(self):
    #     """Страница / доступна любому пользователю."""
    #     response = self.guest_client.get('/task/', follow=True)
    #     self.assertRedirects(
    #         response, '/admin/login/?next=/task/'
    #     )
