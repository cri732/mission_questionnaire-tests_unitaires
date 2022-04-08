import requests
import json
import unicodedata

# LIENS NON JSON + MAUVAIS LIEN les chats
# open_quizz_db_data = (
#     ("Animaux", "Les chats", "https://www.kiwimeeeeee.com/oqdb/files/1050828847/OpenQuizzDB_050/openquizzdb_50.json"),
#     ("Arts", "Musée du Louvre", "https://www.kiwime.com/oqdb/files/1086624389/OpenQuizzDB_086/openquizzdb_86.json"),
#     ("Bande dessinnée", "Tintin", "https://www.kiwime.com/oqdb/files/2124627384/OpenQuizzDB_124/openquizzdb_124.json"),
#     ("Cinéma", "Alien", "https://www.kiwime.com/oqdb/files/3241454997/OpenQuizzDB_241/openquizzdb_241.json"),
#     ("Cinéma", "Star wars", "https://www.kiwime.com/oqdb/files/1090993427/OpenQuizzDB_090/openquizzdb_90.json"),
# )

# LIENS OK LE 20/03/2022
open_quizz_db_data = (
    ("Animaux", "Les chats", "https://www.kiwime.com/oqdb/files/1050288832/OpenQuizzDB_050/openquizzdb_50.json"),
    ("Arts", "Musée du Louvre", "https://www.kiwime.com/oqdb/files/1086665427/OpenQuizzDB_086/openquizzdb_86.json"),
    ("Bande dessinnée", "Tintin", "https://www.kiwime.com/oqdb/files/2124627594/OpenQuizzDB_124/openquizzdb_124.json"),
    ("Cinéma", "Alien", "https://www.kiwime.com/oqdb/files/3241985774/OpenQuizzDB_241/openquizzdb_241.json"),
    ("Cinéma", "Star wars", "https://www.kiwime.com/oqdb/files/1090683544/OpenQuizzDB_090/openquizzdb_90.json"),
)


def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')


def get_quizz_filename(categorie, titre, difficulte):
    return strip_accents(categorie).lower().replace(" ", "") + "_" + strip_accents(titre).lower().replace(" ", "") + "_" + strip_accents(difficulte).lower().replace(" ", "") + ".json"


def generate_json_file(categorie, titre, url):
    out_questionnaire_data = {"categorie": categorie, "titre": titre, "questions": []}
    out_questions_data = []
    # Gestion si mauvaise url
    try:
        response = requests.get(url)
    except:
        print(f"Erreur avec le lien: {url}")
    else:
        # Gestion si lien n'est pas fichier json
        try:
            data = json.loads(response.text)
            all_quizz = data["quizz"]["fr"]
            for quizz_title, quizz_data in all_quizz.items():
                out_filename = get_quizz_filename(categorie, titre, quizz_title)
                print(out_filename)
                out_questionnaire_data["difficulte"] = quizz_title
                for question in quizz_data:
                    question_dict = {}
                    question_dict["titre"] = question["question"]
                    question_dict["choix"] = []
                    for ch in question["propositions"]:
                        question_dict["choix"].append((ch, ch==question["réponse"]))
                    out_questions_data.append(question_dict)
                out_questionnaire_data["questions"] = out_questions_data
                out_json = json.dumps(out_questionnaire_data)

                file = open(out_filename, "w")
                file.write(out_json)
                file.close()
                print("end")
        except:
            print(f"Erreur dans la désérialisation du lien: {url} - Questionnaire {titre} non généré")


# Exécuter cette partie de code que si le nom du fichier lancé est le même que le nom dans le main
if __name__ == "__main__":
    for quizz_data in open_quizz_db_data:
        generate_json_file(quizz_data[0], quizz_data[1], quizz_data[2])

