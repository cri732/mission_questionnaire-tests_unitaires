import os
from turtle import width
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


# Tests sur la class Questionnaire
class TestsQuestionnaire(unittest.TestCase):
    def setUp(self):
        print("setUp")

    def tearDown(self):
        print("tearDown")

    # Tester le lancement du questionnaire
    def test_questionnaire_lancer(self):
        filename = os.path.join("test_data", "cinema_alien_debutant.json")
        q = questionnaire.Questionnaire.from_json_file(filename)
        # S'assurer que le questionnaire ne renvoie pas none
        self.assertIsNotNone(q)
        # S'assurer que le questionnaire renvoie le bon nombre de questions
        self.assertEqual(len(q.questions), 10)
        # S'assurer que le questionnaire renvoie le bon titre
        self.assertEqual(q.titre, "Alien")
        # S'assurer que le questionnaire renvoie la bonne catégorie
        self.assertEqual(q.categorie, "Cinéma")
        # S'assurer que le questionnaire renvoie la bonne difficulté
        self.assertEqual(q.difficulte, "débutant")
        # S'assurer que le questionnaire renvoie le bon score
        with patch("builtins.input", return_value="1"):
            self.assertEqual(q.lancer(), 2)


unittest.main()