from datetime import datetime
from unittest import TestCase
from wotsong.core.models.BaseEntity import DocumentReference, EntityNotCommited
from wotsong.core.models.Game import Game
from wotsong.core.models import User, SpotifySecrets

class TestUser(TestCase):

    def test_document_reference(self):
        user = User("id")
        reference = user.get_document_reference()
        self.assertIsInstance(reference, DocumentReference)

    def test_path(self):
        user = User("id")
        self.assertEqual(user.path, "users/id") 

    def test_is_anonymous(self):
        user = User("id")

        self.assertTrue(user.is_anonymous)
        user.email = "an@email.com"
        self.assertFalse(user.is_anonymous)

class TestSpotifySecrets(TestCase):

    def test_document_reference(self):
        secrets = SpotifySecrets("access_token", datetime.now(), "refresh_token")
        user = User("id")
        with self.assertRaises(Exception):
            secrets.get_document_reference()

        secrets.set_user(user)
        reference = secrets.get_document_reference()
        self.assertIsInstance(reference, DocumentReference)
        self.assertEqual(secrets.path, "users/id/secrets/spotify_secrets")



class TestGame(TestCase):

    def test_game_code(self):
        game = Game()
        self.assertIsInstance(game.game_code,str)
        self.assertEqual(len(game.game_code), 5, "expect length of game_codee = 5")