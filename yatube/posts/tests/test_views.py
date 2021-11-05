import time

from django import forms
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Group, Post

User = get_user_model()


class AllViewsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_a = User.objects.create_user(username='user_a')
        cls.author_p = User.objects.create_user(username='author_p')
        cls.group = Group.objects.create(
            slug='test-slug',
            title='Тестовая группа',
            description='Тестовое описание',)
        cls.post = Post.objects.create(
            author=cls.author_p,
            text='Тестовый текст',
            group=cls.group,)
        time.sleep(0.01)  # Иначе сортирует не верно.
        Post.objects.create(author=cls.author_p,
                            text='text_2',
                            )
        for i in range(13):
            time.sleep(0.01)
            Post.objects.create(author=cls.user_a,
                                text=f'text{i}',
                                group=cls.group)

    def setUp(self):
        self.a_c_author = Client()
        self.a_c_author.force_login(self.author_p)

    def test_pages_uses_correct_template(self):
        templates_pages_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_list', kwargs={'slug': 'test-slug'}):
            'posts/group_list.html',
            reverse('posts:profile', kwargs={'username': 'user_a'}):
            'posts/profile.html',
            reverse('posts:post_detail', kwargs={'post_id': '1'}):
            'posts/post_detail.html',
            reverse('posts:post_edit', kwargs={'post_id': '1'}):
            'posts/create_post.html',
            reverse('posts:post_create'): 'posts/create_post.html',
            # reverse('posts:create_post') в теории/м.б. в тестах!!!
            reverse('about:author'): 'about/author.html',
            reverse('about:tech'): 'about/tech.html',
            reverse('users:signup'): 'users/signup.html',
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.a_c_author.get(reverse_name)
                self.assertTemplateUsed(response, template)

    # Проверяем пэджинатор.

    def test_index_first_page(self):
        # индекс 1-я стр, 10
        response = self.a_c_author.get(reverse('posts:index'))
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_index_second_page(self):
        # индек 2-я стр, 5 постов
        response = self.a_c_author.get(reverse('posts:index') + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 5)

    def test_group_posts_first_page(self):
        # гроуп 1-я = 10
        response = self.a_c_author.get(reverse('posts:group_list',
                                               kwargs={'slug': 'test-slug'}))
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_group_posts_second_page(self):
        # 2-я стр. группы = 4 поста
        response = self.a_c_author.get(reverse(
            'posts:group_list',
            kwargs={'slug': 'test-slug'}) + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 4)

    def test_profile_first_page(self):
        # профайл 1-я 10
        response = self.a_c_author.get(reverse(
            'posts:profile', kwargs={'username': 'user_a'}))
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_profile_second_page(self):
        # профайл 2-я 3
        response = self.a_c_author.get(reverse(
            'posts:profile', kwargs={'username': 'user_a'}) + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 3)

    # Проверяем контекст страниц.
    def test_index_pages(self):
        response = self.a_c_author.get(reverse('posts:index'))
        obj = response.context['page_obj'][1]
        self.assertEqual(obj.author, self.user_a)
        self.assertEqual(obj.text, 'text11')

    def test_post_create_page(self):
        response = self.a_c_author.get(reverse('posts:post_create'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.models.ModelChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_post_detail_pages(self):
        response = self.a_c_author.get(reverse('posts:post_detail',
                                               kwargs={'post_id': '1'}))
        self.assertEqual(response.context.get('post').text, 'Тестовый текст')
        self.assertEqual(response.context.get('post').author,
                         self.author_p)
        self.assertEqual(response.context.get('post').group,
                         self.group)

    def test_group_posts_pages(self):
        response = self.a_c_author.get(reverse('posts:group_list',
                                               kwargs={'slug': 'test-slug'}))
        obj = response.context['page_obj'][0]
        self.assertEqual(obj.text, 'text12')
        self.assertEqual(obj.author, self.user_a)
        self.assertEqual(obj.group, self.group)

    def test_profile_pages(self):
        response = self.a_c_author.get(reverse('posts:profile',
                                               kwargs={'username':
                                                       'author_p'}))
        user = User.objects.get(username='author_p')
        obj = response.context['page_obj'][0]
        self.assertEqual(obj.text, 'text_2')
        self.assertEqual(obj.author, user)

    # Проверяем последний созданный пост с группой.

    def test_last_post_in_group(self):
        """ В группах 1-й пост должен быть последним из созданных.
         И в своей ли он группе."""
        response = self.a_c_author.get(
            reverse(
                'posts:group_list', kwargs={'slug': 'test-slug'}
            )
        )
        self.assertEqual(response.context['page_obj'][0].id, 15)
        self.assertEqual(response.context['page_obj'][0].group, self.group)

    def test_last_post_in_index(self):
        """ В индексе 1-й пост должен быть последним из созданных.
         Группа в норме."""
        response = self.a_c_author.get(reverse('posts:index'))
        self.assertEqual(response.context['page_obj'][0].id, 15)
        self.assertEqual(response.context['page_obj'][0].group, self.group)

    def test_last_post_in_profile(self):
        """ В профайле 1-й пост должен быть последним из созданных.
         Группа в норме."""
        response = self.a_c_author.get(reverse('posts:profile',
                                               kwargs={'username':
                                                       'user_a'}))
        self.assertEqual(response.context['page_obj'][0].id, 15)
        self.assertEqual(response.context['page_obj'][0].group, self.group)

    def test_post_in_2_group(self):
        """ Проверяем не отображается ли пост, принадлежащий
         "2"-й группе, в "1"-й."""
        g2 = Group.objects.create(slug='test-slug2', title='Тестовая группа2',
                                  description='Тестовое описание2',)
        Post.objects.create(author=self.author_p, text='text_16', group=g2)
        response = self.a_c_author.get(
            reverse(
                'posts:group_list', kwargs={'slug': 'test-slug'}
            )
        )
        self.assertEqual(response.context['page_obj'][0].id, 15)
        """ Так-как 15-й пост остался 1-м в группе "1", значит 16-й пост,
         из группы "2", не отображается в "1"-й группе - Ок."""
