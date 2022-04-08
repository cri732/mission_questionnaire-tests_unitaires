# Import de json pour charger les fichiers de questionnaires générés avec script import
import json
import sys


class Question:
    def __init__(self, titre, choix, bonne_reponse):
        self.titre = titre
        self.choix = choix
        self.bonne_reponse = bonne_reponse

    def from_json_data(data):
        # Définir les choix de réponses
        choix = [i[0] for i in data["choix"]]
        # Définir la bonne réponse
        bonne_reponse = [i[0] for i in data["choix"] if i[1] == True]
        # Gestion erreur s'il y a plusieurs bonnes réponses ou s'il n'y en a aucune
        if len(bonne_reponse) != 1:
            return None
        question = Question(data["titre"], choix, bonne_reponse[0])
        return question

    def poser(self, num_question, nb_questions):
        print(f"QUESTION {num_question} / {nb_questions}")
        print("  " + self.titre)
        for i in range(len(self.choix)):
            print("  ", i+1, "-", self.choix[i])

        print()
        resultat_response_correcte = False
        reponse_int = Question.demander_reponse_numerique_utlisateur(1, len(self.choix))
        if self.choix[reponse_int-1].lower() == self.bonne_reponse.lower():
            print("Bonne réponse")
            resultat_response_correcte = True
        else:
            print("Mauvaise réponse")
            print(f"La bonne réponse était: {self.bonne_reponse}")
            
        print()
        return resultat_response_correcte

    def demander_reponse_numerique_utlisateur(min, max):
        reponse_str = input("Votre réponse (entre " + str(min) + " et " + str(max) + ") :")
        try:
            reponse_int = int(reponse_str)
            if min <= reponse_int <= max:
                return reponse_int

            print("ERREUR : Vous devez rentrer un nombre entre", min, "et", max)
        except:
            print("ERREUR : Veuillez rentrer uniquement des chiffres")
        return Question.demander_reponse_numerique_utlisateur(min, max)


class Questionnaire:
    def __init__(self, questions, categorie, titre, difficulte):
        self.questions = questions
        self.categorie = categorie
        self.titre = titre
        self.difficulte = difficulte

    def from_json_data(data):
        # Récupérer les questions
        questionnaire_data_questions = data["questions"]
        # Mise en forme des questions : peut générer None (voir from_data_json class Question)
        questions = [Question.from_json_data(i) for i in questionnaire_data_questions]
        # Suppression des questions None
        questions = [i for i in questions if i]
        return Questionnaire(questions, data["categorie"], data["titre"], data["difficulte"])

    def from_json_file(filename):
        try:
            # Charger un fichier json
            with open(filename, "r", encoding="utf-8") as f:
                questionnaire_data = json.load(f)
        except:
            print("Erreur lors de l'ouverture ou la lecture du fichier")
            return None
        # Créer le questionnaire
        return Questionnaire.from_json_data(questionnaire_data)

    def lancer(self):
        score = 0
        nb_questions = len(self.questions)
        # Afficher infos questionnaire
        print("----------")
        print(f"QUESTIONNAIRE: {self.titre}")
        print(f"    Catégorie: {self.categorie}")
        print(f"    Difficulté: {self.difficulte}")
        print(f"    Nombre de questions: {nb_questions}")
        print("----------")
        for i in range(nb_questions):
            question = self.questions[i]
            if question.poser(i + 1, nb_questions):
                score += 1
        print("Score final :", score, "sur", nb_questions)
        return score


# -------------------- PHASE PROD : TOUS LES QUESTIONNAIRES --------------------
# Exécuter cette partie de code que si le nom du fichier lancé est le même que le nom dans le main
if __name__ == "__main__":
    # Questionnaire.from_json_file("cinema_alien_debutant.json").lancer()
    if len(sys.argv) < 2:
        print("ERREUR: Vous devez spécifié le nom du fichier json à charger")
        exit(0)
    json_filename = sys.argv[1]
    questionnaire = Questionnaire.from_json_file(json_filename)
    if questionnaire:
        questionnaire.lancer()


# -------------------- PHASE TESTS : UN SEUL QUESTIONNAIRE --------------------
# # Tester première question
# # Charger un fichier json
# with open('animaux_leschats_debutant.json', "r", encoding="utf-8") as f:
#     questionnaire_data = json.load(f)
# # Récupérer les questions
# questionnaire_data_questions = questionnaire_data["questions"]
# # Mise en forme de la question
# question = Question.from_json_data(questionnaire_data_questions[0])
# # Poser une seule question
# question.poser()

# Tester lancement questionnaire : Ancienne méthode
# # Charger un fichier json
# with open('animaux_leschats_debutant.json', "r", encoding="utf-8") as f:
#     questionnaire_data = json.load(f)
# # Créer et lancer le questionnaire
# Questionnaire.from_json_data(questionnaire_data).lancer()
# print()