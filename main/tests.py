from django.test import TestCase
from main.models import *
from django.contrib.auth.models import User
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

        favorite_test = FAVORITE.objects.create(user=test_user, beer=beer_test)

        profile_test = PROFILE.objects.create(user=test_user,
                                              email='joekawa@yahoo.com',
                                              city='Omaha',
                                              state='NE')

        vote = VOTE.objects.create(user=test_user, vote_choice='U',
                                   content_object=beer_test,
                                   object_id=beer_test.pk)


        # *Save the model to the database
        favorite_test.save()

        beer_test.save()
        brewery_test.save()
        profile_test.save()
        vote.save()

        tag_test = TAG.objects.create(beer=beer_test, tag='first tag',
                                      created_by=test_user
                                      )
        tag_test.save()

        # *Retrieve the saved model from the database
        beer_save_test = BEER.objects.get(pk=beer_test.pk)
        brewery_save_test = BREWERY.objects.get(pk=brewery_test.pk)

        favorite_save_test = FAVORITE.objects.get(pk=favorite_test.pk)
        tag_save_test = TAG.objects.get(pk=tag_test.pk)
        profile_save_test = PROFILE.objects.get(pk=profile_test.pk)
        vote_save_test = VOTE.objects.get(object_id=beer_test.pk)

        # *Check that the saved model has the correct values
        self.assertEqual(beer_save_test.name, 'test beer')
        self.assertEqual(brewery_save_test.name, 'test brewery')
        self.assertEqual(favorite_save_test.user.username, 'test_user')
        self.assertEqual(tag_save_test.tag, 'first tag')
        self.assertEqual(profile_save_test.city, 'Omaha')
        self.assertEqual(vote_save_test.content_object, beer_test)

