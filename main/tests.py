from django.test import TestCase
from main.models import *
from django.contrib.auth.models import User
from django.urls import reverse
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
