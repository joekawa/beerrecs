from django.test import TestCase
from main.models import *
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import SignUpForm


# Create your tests here.


class ModelTest(TestCase):
    def test_create_and_save_model(self):

        # *Create test user
        test_user = User.objects.create(username='test_user',
                                        password='Password')
        test_user.save()

        # *Create a new instance of MyModel
        beer_test = BEER.objects.create(name='test beer',
                                        description='beer in test script')
        brewery_test = BREWERY.objects.create(name='test brewery',
                                              description='brewery in ' +
                                              'test script')

        profile_test = PROFILE.objects.create(user=test_user,
                                              email='joekawa@yahoo.com',
                                              city='Omaha',
                                              state='NE')

        vote = ACTIVITY.objects.create(user=test_user, activity='U',
                                       content_object=beer_test,
                                       object_id=beer_test.pk)
        favorite = ACTIVITY.objects.create(user=test_user, activity='F',
                                           content_object=beer_test,
                                           object_id=beer_test.pk)

        # * Save the model to the database
        beer_test.save()
        brewery_test.save()
        profile_test.save()
        vote.save()
        favorite.save()

        tag_test = TAG.objects.create(beer=beer_test, tag='first tag',
                                      created_by=test_user
                                      )
        tag_test.save()

        # *Retrieve the saved model from the database
        beer_save_test = BEER.objects.get(pk=beer_test.pk)
        brewery_save_test = BREWERY.objects.get(pk=brewery_test.pk)

        tag_save_test = TAG.objects.get(pk=tag_test.pk)
        profile_save_test = PROFILE.objects.get(pk=profile_test.pk)
        vote_save_test = ACTIVITY.objects.get(object_id=beer_test.pk,
                                              activity='U')
        favorite_save_test = ACTIVITY.objects.get(object_id=beer_test.pk,
                                                  activity='F')

        # *Check that the saved model has the correct values
        self.assertEqual(beer_save_test.name, 'test beer')
        self.assertEqual(brewery_save_test.name, 'test brewery')
        self.assertEqual(favorite_save_test.user.username, 'test_user')
        self.assertEqual(tag_save_test.tag, 'first tag')
        self.assertEqual(profile_save_test.city, 'Omaha')
        self.assertEqual(vote_save_test.content_object, beer_test)
        self.assertEqual(favorite_save_test.content_object, beer_test)
        self.assertEqual(vote_save_test.activity, 'U')
        self.assertEqual(favorite_save_test.activity, 'F')


class TestViews(TestCase):
    def test_home_view(self):
        response = self.client.get(reverse('main:home'))
        self.assertEqual(response.status_code, 200)

    def test_search_view(self):
        response = self.client.get(reverse('main:search'))
        self.assertEqual(response.status_code, 200)

    def test_all_beers_view(self):
        response = self.client.get(reverse('main:all_beers'))
        self.assertEqual(response.status_code, 200)

    def test_my_beers_view(self):
        response = self.client.get(reverse('main:my_beers'))
        self.assertEqual(response.status_code, 200)

    def test_beer_view(self):
        beer = BEER.objects.create(name='ttest', description='test')
        response = self.client.get(reverse('main:beer',
                                           kwargs={'id': beer.pk}))
        self.assertEqual(response.status_code, 200)

    def test_brewery_view(self):
        brewery = BREWERY.objects.create(name='test', description='test')
        response = self.client.get(reverse('main:brewery',
                                           kwargs={'id': brewery.pk}))
        self.assertEqual(response.status_code, 200)

    def test_favorites_view(self):
        user = User.objects.create(username='test', password='Password')
        response = self.client.get(reverse('main:favorites',
                                           kwargs={'user_id': user.pk}))
        self.assertEqual(response.status_code, 200)


class SignUpFormTest(TestCase):
    def setUp(self):
        self.url = reverse('main:signup')

    def test_signup_form_valid(self):
        data = {
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'city': 'Testville',
            'state': 'CA',
            'zip_code': '12345'
        }
        form = SignUpForm(data=data)
        self.assertTrue(form.is_valid())

    def test_signup_form_invalid(self):
        data = {
            'username': '',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'city': 'Testville',
            'state': 'CA',
            'zip_code': '12345'
        }
        form = SignUpForm(data=data)
        self.assertFalse(form.is_valid())

    def test_signup_view_post(self):
        data = {
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'city': 'Testville',
            'state': 'CA',
            'zip_code': '12345'
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username=data['username']).exists())

    def test_signup_view_invalid_post(self):
        data = {
            'username': '',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'email': 'testuser@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'city': 'Testville',
            'state': 'CA',
            'zip_code': '12345'
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username=data['username']).exists())
