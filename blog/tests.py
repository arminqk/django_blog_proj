from django.test import TestCase
from django.contrib.auth.models import User
from django.shortcuts import reverse
from .models import Post



class BlogPostTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='user1')

        cls.post1 = Post.objects.create(
            title='post title',
            text='test text ',
            status=Post.STATUS_CHOICES[0][0],
            author=cls.user,
        )
        cls.post2 = Post.objects.create(
            title='post2',
            text='test2 text',
            status=Post.STATUS_CHOICES[1][0],
            author=cls.user,
        )


#UNIT TEST
    def test_post_model_str(self):
        post = self.post1
        self.assertEqual(str(post) , post.title)

    def test_post_detail(self):
        self.assertEqual(self.post1.title , 'post title')
        self.assertEqual(self.post1.text, 'test text ')


    def test_post_list_url(self):
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code , 200)

    def test_post_list_url_by_name(self):
        response = self.client.get(reverse('posts_list'))
        self.assertEqual(response.status_code, 200)

    def test_post_title_on_blog_list(self):
        response = self.client.get(reverse('posts_list'))
        self.assertContains(response,'post title')

    def test_post_text_on_blog_list(self):
        response = self.client.get(reverse('posts_list'))
        self.assertContains(response , self.post1.text)

    def test_post_details_url_by_name(self):
        response = self.client.get(reverse('posts_detail' , args=[self.post1.id]))
        self.assertEqual(response.status_code, 200)

    def test_post_detail_on_blog_detail_page(self):
        response = self.client.get(reverse('posts_detail', args=[self.post1.id]))
        self.assertContains(response, self.post1.title)
        self.assertContains(response, self.post1.text)

    def test_if_post_id_n_exist(self):
        response = self.client.get(reverse('posts_detail', args=[self.post1.id+100]))
        self.assertEqual(response.status_code, 404)


    def test_draft_post_not_show_in_post_list(self): #TDD
        response = self.client.get(reverse('posts_list'))
        self.assertContains(response, self.post1.title)
        self.assertNotContains(response, self.post2.title)


    def post_create_view(self):
        response = self.client.post(reverse('post_create') , {
            'title' : 'post titleee',
            'text' : 'posttt text',
            'status' : 'pub',
            'author' : self.user.id,
        })
        self.assertEqual(response.status_code , 302)

    def test_post_update_view(self):
        response = self.client.post(reverse('post_update' , args =[self.post2.id]) ,{
            'title': 'post update',
            'text': 'update text',
            'status':'pub',
            'author' : self.post2.author.id
        })
        self.assertEqual(Post.objects.last().title ,'post update')
        self.assertEqual(Post.objects.last().text, 'update text')

    def test_post_delete_view(self):
        response = self.client.post(reverse('post_delete', args=[self.post2.id]))
        self.assertEqual(response.status_code , 302)


