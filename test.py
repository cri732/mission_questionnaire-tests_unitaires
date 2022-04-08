import unittest

from unittest.mock import patch

import questionnaire

# Tests sur la class Question
class TestsQuestion(unittest.TestCase):
    def setUp(self):
        print("setUp")

    def tearDown(self):
        print("tearDown")

    # Tester si la réponse donnée renvoie bonne ou mauvaise réponse
    def test_question_bonne_mauvaise_reponse(self):
        choix = ("choix1", "choix2", "choix3")
        q = questionnaire.Question("titre_question", choix, "choix2")
        # choix2 = bonne réponse : s'assurer que le choix1 renvoie une mauvaise réponse
        with patch("builtins.input", return_value="1"):
            self.assertFalse(q.poser(1, 1))
        # choix2 = bonne réponse : s'assurer que le choix2 renvoie une bonne réponse
        with patch("builtins.input", return_value="2"):
            self.assertTrue(q.poser(1, 1))
        # choix2 = bonne réponse : s'assurer que le choix3 renvoie une mauvaise réponse
        with patch("builtins.input", return_value="3"):
            self.assertFalse(q.poser(1, 1))


unittest.main()