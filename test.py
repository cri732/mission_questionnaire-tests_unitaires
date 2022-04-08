import unittest
import os
import json

from unittest.mock import patch

import questionnaire
import questionnaire_import

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

    # Tester le lancement du questionnaire avec un format invalide
    def test_questionnaire_format_invalide(self):
        # Manque categorie et difficulte
        filename = os.path.join("test_data", "format_invalide1.json")
        q = questionnaire.Questionnaire.from_json_file(filename)
        # S'assurer que le questionnaire ne renvoie pas none
        self.assertIsNotNone(q)
        # S'assurer que le questionnaire renvoie inconnue pour la catégorie
        self.assertEqual(q.categorie, "Inconnue")
        # S'assurer que le questionnaire renvoie inconnue pour la difficulté
        self.assertEqual(q.difficulte, "Inconnue")
        # S'assurer que le questionnaire contient des questions
        self.assertIsNotNone(q.questions)
        
        # Manque categorie et difficulte et titre
        filename = os.path.join("test_data", "format_invalide2.json")
        q = questionnaire.Questionnaire.from_json_file(filename)
        # S'assurer que le questionnaire renvoie none car titre bloquant
        self.assertIsNone(q)

        # Manque categorie et difficulte et questions
        filename = os.path.join("test_data", "format_invalide3.json")
        q = questionnaire.Questionnaire.from_json_file(filename)
        # S'assurer que le questionnaire renvoie none car titre bloquant
        self.assertIsNone(q)


# Tests sur le code d'import des questionnaires
class TestImportQuestionnaire(unittest.TestCase):
    # Tester l'import au format json
    def test_import_format_json(self):
        questionnaire_import.generate_json_file("Animaux", "Les chats", "https://www.kiwime.com/oqdb/files/1050288832/OpenQuizzDB_050/openquizzdb_50.json")
        filenames = ("animaux_leschats_confirme.json", "animaux_leschats_debutant.json", "animaux_leschats_expert.json")
        for filename in filenames:
            # S'assurer que le fichier existe
            self.assertTrue(os.path.isfile(filename))
            with open(filename, "r", encoding="utf-8") as f:
                json_data = f.read()
            try:
                data = json.loads(json_data)
            except:
                self.fail(f"Problème de désérialisation pour le fichier {filename}")

            # S'assurer que le questionnaire contient un titre
            self.assertIsNotNone(data.get("titre"))
            # S'assurer que le questionnaire contient une catégorie
            self.assertIsNotNone(data.get("categorie"))
            # S'assurer que le questionnaire contient une difficulté
            self.assertIsNotNone(data.get("difficulte"))
            # S'assurer que le questionnaire contient des questions
            self.assertIsNotNone(data.get("questions"))

            for question in data.get("questions"):
                # S'assurer que la question contient un titre
                self.assertIsNotNone(question.get("titre"))
                # S'assurer que la question contient des choix
                self.assertIsNotNone(question.get("choix"))
                for choix in question.get("choix"):
                    # S'assurer qu'il y a bien des champs existants
                    self.assertGreater(len(choix[0]), 0)
                    # S'assurer que l'index 1 de choix soit bien un booléen
                    self.assertTrue(isinstance(choix[1], bool))
                    bonne_reponse = [i[0] for i in question.get("choix") if i[1]]
                    # S'assurer que le nombre de bonne réponse est strictement égal à 1
                    self.assertEqual(len(bonne_reponse), 1)


unittest.main()