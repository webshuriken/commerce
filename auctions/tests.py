from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Listing, User, Comment


# MODELS TESTS
class ListingModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_create_valid_listing(self):
        listing = Listing.objects.create(
            title="Valid Title",
            description="Valid Description",
            value=100.00,
            user=self.user
        )
        self.assertEqual(listing.title, "Valid Title")
        self.assertEqual(listing.description, "Valid Description")
        self.assertEqual(listing.value, 100.00)
        self.assertEqual(listing.user, self.user)

    def test_validate_price(self):
        with self.assertRaises(ValidationError):
            Listing.objects.create(
                title="Valid Title",
                description="Valid Description",
                value=-10.00,
                user=self.user
            ).full_clean()

    def test_validate_title_profanity(self):
        with self.assertRaises(ValidationError):
            Listing.objects.create(
                title="Fuck the pain away",
                description="Valid Description",
                value=100.00,
                user=self.user
            ).full_clean()
    
    def test_validate_description_profanity(self):
        with self.assertRaises(ValidationError):
            Listing.objects.create(
                title="Valid title",
                description="sucking on my titis like you wanted me to",
                value=100.00,
                user=self.user
            ).full_clean()
      
    def test_validate_profanity_edge1(self):
      # ege1: using numbers and letter to write swear words
      with self.assertRaises(ValidationError):
          Listing.objects.create(
              title="Valid title",
              description="You can not sneak 5h1t is this text",
              value=100.00,
              user=self.user
          ).full_clean()

    def test_listing_str(self):
        listing = Listing.objects.create(
            title="Valid Title",
            description="Valid Description",
            value=100.00,
            user=self.user
        )
        expected_str = f"ID: {listing.id}: {listing.title}\nDescription: {listing.description}\nValue: {listing.value}\nCreated by: {listing.user}\n"
        self.assertEqual(str(listing), expected_str)

class CommentModelTest(TestCase):

    def setUp(self):
        # Comment model requires a listing and a user
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.listing = Listing.objects.create(
            title="Valid Title",
            description="Valid Description",
            value=100.00,
            user=self.user
        )

    def test_create_valid_comment(self):
        comment = Comment.objects.create(
            comment="This is a valid comment.",
            user=self.user,
            listing=self.listing
        )
        self.assertEqual(comment.comment, "This is a valid comment.")
        self.assertEqual(comment.user, self.user)
        self.assertEqual(comment.listing, self.listing)

    def test_validate_comment_profanity(self):
        with self.assertRaises(ValidationError):
            Comment.objects.create(
                comment="This is a shitty comment.",
                user=self.user,
                listing=self.listing
            ).full_clean()

    def test_validate_comment_profanity_edge_case(self):
        with self.assertRaises(ValidationError):
            Comment.objects.create(
                comment="This is a 5h1tty comment.",
                user=self.user,
                listing=self.listing
            ).full_clean()

    def test_comment_str(self):
        comment = Comment.objects.create(
            comment="This is a valid comment.",
            user=self.user,
            listing=self.listing
        )
        expected_str = f"ID: {comment.id}: {comment.comment} by user {comment.user}\nFor listing: {comment.listing}\n"
        self.assertEqual(str(comment), expected_str)