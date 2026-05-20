from pymongo import MongoClient
from pprint import pprint
import json

# import de la base de données 
# mongoimport -d sample -c books --authenticationDatabase admin --username datascientest --password dst123 --file /data/db/books.json

if __name__ == "__main__":

    #
    # Connexion à la base de données
    #

    # (a) Pour se connecter à MongoDB via pymongo, ajoutez l'authentification aux lignes de 
    # code suivantes puis lancez-les :
    client = MongoClient(
        host="127.0.0.1",
        port = 27017,
        username = "datascientest",
        password = "dst123"
    )

    # (b) Afficher la liste des bases de données disponibles.
    print(client.list_database_names())

    # (c) Afficher la liste des collections disponibles dans cette base de données.
    print(client['sample'].list_collection_names())
    
    # (d) Afficher un des documents de cette collection.
    books = client['sample']['books']
    pprint(books.find_one())

    # (e) Afficher le nombre de documents dans cette collection.
    print(books.count_documents({})) # books.find().count() est déprécié

    #
    # Exploration de la base
    #

    with open("exam.txt", "w") as f:

        # (a) Afficher le nombre de livres avec plus de 400 pages. Afficher ensuite le nombre de livres ayant plus de 400 pages ET qui sont publiés.
        f.write("(a) Afficher le nombre de livres avec plus de 400 pages. Afficher ensuite le nombre de livres ayant plus de 400 pages ET qui sont publiés.\n")
        f.write('books.count_documents({"pageCount": {"$gt": 400}})\n') # books.find({"pageCount": {"$gt": 400}}).count() est déprécié
        f.write("Il y a %s livres avec plus de 400 pages.\n" % books.count_documents({"pageCount": {"$gt": 400}}))
        f.write('books.count_documents({"pageCount": {"$gt": 400}, "status": "PUBLISH"})\n') # books.find({"pageCount": {"$gt": 400}, "status": "PUBLISH"}).count() est déprécié
        f.write("Il y a %s livres avec plus de 400 pages et qui sont publiés.\n" % books.count_documents({"pageCount": {"$gt": 400}, "status": "PUBLISH"}))
        f.write("\n")

        # (b) Afficher le nombre de livres ayant le mot-clé Android dans leur description (brève ou longue).
        f.write("(b) Afficher le nombre de livres ayant le mot-clé Android dans leur description (brève ou longue).\n")
        f.write('books.count_documents({"$or": [{"longDescription": {"$regex": "Android"}}, {"shortDescription": {"$regex": "Android"}}]})\n')
        f.write("Il y a %s livres avec le mot-clé Android dans leur description (brève ou longue).\n" % books.count_documents({"$or": [{"longDescription": {"$regex": "Android"}}, {"shortDescription": {"$regex": "Android"}}]}))
        f.write("\n")

        # (c) Chaque document possède un attribut categories qui est une liste. Vous devez grouper tous les documents en un à l'aide de l'opérateur $group. Puis, à l'aide de l'opérateur $addToSet, créez 2 sets à partir des catégories contenues dans la liste categories selon leur index 0 ou 1. Pour cibler, les catégories utilisez l'opérateur $arrayElemAt.
        f.write("(c) Chaque document possède un attribut categories qui est une liste. Vous devez grouper tous les documents en un à l'aide de l'opérateur $group. Puis, à l'aide de l'opérateur $addToSet, créez 2 sets à partir des catégories contenues dans la liste categories selon leur index 0 ou 1. Pour cibler, les catégories utilisez l'opérateur $arrayElemAt.\n")
        f.write('agr = books.aggregate([{"$group": {"_id": None, "set_0": {"$addToSet": {"$arrayElemAt": ["$categories", 0]}}, "set_1": {"$addToSet": {"$arrayElemAt": ["$categories", 1]}}}}])\n')
        agr = books.aggregate([{"$group": {"_id": None, "set_0": {"$addToSet": {"$arrayElemAt": ["$categories", 0]}}, "set_1": {"$addToSet": {"$arrayElemAt": ["$categories", 1]}}}}])
        f.write("Résultat de lagregation: \n")
        json.dump(next(agr), f, indent=4, ensure_ascii=False)
        f.write("\n")

        # (d) Afficher le nombre de livres qui contiennent des noms de langages suivants dans leur description longue : Python, Java, C++, Scala. On pourra s'appuyer sur des expressions régulières et une condition or.
        f.write("(d) Afficher le nombre de livres qui contiennent des noms de langages suivants dans leur description longue : Python, Java, C++, Scala. On pourra s'appuyer sur des expressions régulières et une condition or.\n")
        f.write('books.count_documents({"$or": [{"longDescription": {"$regex": "Python"}}, {"longDescription": {"$regex": "Java"}}, {"longDescription": {"$regex": "C++"}}, {"longDescription": {"$regex": "Scala"}}]})\n')
        f.write("Il y a %s livres contenant au moins un des mots Python, Java, C++, Scala dans leur description longue.\n" % books.count_documents({"$or": [{"longDescription": {"$regex": "Python"}}, {"longDescription": {"$regex": "Java"}}, {"longDescription": {"$regex": "C++"}}, {"longDescription": {"$regex": "Scala"}}]}))
        f.write("\n")

        # (e) Afficher diverses informations statistiques sur notre base de données : nombre maximal, minimal, et moyen de pages par catégorie. On utilisera une pipeline d'agrégation, le mot-clé $group, ainsi que les accumulateurs appropriés. N'oubliez pas d'aller voir "$unwind" pour ce problème.
        f.write("(e) Afficher diverses informations statistiques sur notre base de données : nombre maximal, minimal, et moyen de pages par catégorie. On utilisera une pipeline d'agrégation, le mot-clé $group, ainsi que les accumulateurs appropriés. N'oubliez pas d'aller voir \"$unwind\" pour ce problème.\n")
        agr = books.aggregate([{"$unwind": "$categories"}, {"$group": {"_id": "$categories", "max": {"$max": "$pageCount"}, "min": {"$min": "$pageCount"}, "avg": {"$avg": "$pageCount"}}}])
        f.write("Statistiques du nombre de pages par catégorie :\n")
        json.dump(list(agr), f, indent=4, ensure_ascii=False)
        f.write("\n\n")

        # (f) Via une pipeline d'agrégation, créer de nouvelles variables en extrayant des informations depuis l'attribut dates : année, mois, jour. On rajoutera une condition pour filtrer seulement les livres publiés après 2009. N'affichez que les 20 premiers.
        f.write("(f) Via une pipeline d'agrégation, créer de nouvelles variables en extrayant des informations depuis l'attribut dates : année, mois, jour. On rajoutera une condition pour filtrer seulement les livres publiés après 2009. N'affichez que les 20 premiers.\n")
        f.write('books.aggregate([{"$project": {"year": {"$year": "$publishedDate"}, "month": {"$month": "$publishedDate"}, "day": {"$dayOfMonth": "$publishedDate"}}}, {"$match": {"year": {"$gt": 2009}}}, {"$limit": 20}])\n')
        agr = books.aggregate([{"$project": {"year": {"$year": "$publishedDate"}, "month": {"$month": "$publishedDate"}, "day": {"$dayOfMonth": "$publishedDate"}}}, {"$match": {"year": {"$gt": 2009}}}, {"$limit": 20}])
        f.write("Liste des 20 premiers livres publiés après 2009:\n")
        json.dump(list(agr), f, indent=4, ensure_ascii=False)
        f.write("\n\n")
 
        # (g) À partir de la liste des auteurs, créez de nouveaux attributs (author_1, author_2 ... author_n). Observez le comportement de "$arrayElemAt". N'affichez que les 20 premiers dans l'ordre chronologique.
        f.write('(g) À partir de la liste des auteurs, créez de nouveaux attributs (author_1, author_2 ... author_n). Observez le comportement de "$arrayElemAt". N\'affichez que les 20 premiers dans l\'ordre chronologique.\n')
        f.write('[{"$project": {"_id": "title","author_1": {"$arrayElemAt": ["$authors", 0]}, "author_2": {"$arrayElemAt": ["$authors", 1]}, "author_3": {"$arrayElemAt": ["$authors", 2]}, "author_4": {"$arrayElemAt": ["$authors", 3]}}},{"$sort": {"publishedDate": 1}}, {"$limit": 20}]\n')
        agr = books.aggregate([{"$project": {"_id": "title","author_1": {"$arrayElemAt": ["$authors", 0]}, "author_2": {"$arrayElemAt": ["$authors", 1]}, "author_3": {"$arrayElemAt": ["$authors", 2]}, "author_4": {"$arrayElemAt": ["$authors", 3]}}},{"$sort": {"publishedDate": 1}}, {"$limit": 20}])
        f.write("Liste des autheurs pour les 20 premiers livres par ordre de publication:\n")
        json.dump(list(agr), f, indent=4, ensure_ascii=False)
        f.write("\n\n")

        # (h) En s'inspirant de la requête précédente, créer une colonne contenant le nom du premier auteur, puis agréger selon cette colonne pour obtenir le nombre d'articles pour chaque premier auteur. Afficher le nombre de publications pour les 10 premiers auteurs les plus prolifiques. On pourra utiliser un pipeline d'agrégation avec les mots-clés $group, $sort, $limit.
        f.write('(h) En s\'inspirant de la requête précédente, créer une colonne contenant le nom du premier auteur, puis agréger selon cette colonne pour obtenir le nombre d\'articles pour chaque premier auteur. Afficher le nombre de publications pour les 10 premiers auteurs les plus prolifiques. On pourra utiliser un pipeline d\'agrégation avec les mots-clés $group, $sort, $limit.\n')
        f.write('books.aggregate([{"$project": {"first_author": {"$arrayElemAt": ["$authors", 0]}}}, {"$match": {"first_author": {"$ne": None}}}, {"$group": {"_id": "$first_author", "nb_livres": {"$sum": 1}}}, {"$sort": {"nb_livres": -1}}, {"$limit": 10}])\n')
        agr = books.aggregate([{"$project": {"first_author": {"$arrayElemAt": ["$authors", 0]}}}, {"$match": {"first_author": {"$ne": None}}}, {"$group": {"_id": "$first_author", "nb_livres": {"$sum": 1}}}, {"$sort": {"nb_livres": -1}}, {"$limit": 10}])
        f.write("Nombre de publications pour les 10 premiers auteurs les plus prolifiques:\n")
        json.dump(list(agr), f, indent=4, ensure_ascii=False)
        f.write("\n\n")

        # (i) Afficher la distribution du nombre d'auteurs : Commencer par créer une nouvelle colonne avec le nombre d'auteurs (taille de la liste de l'attribut authors), puis agrégez sur cette colonne avec l'accumulateur $count ou $sum.
        f.write("(i) Afficher la distribution du nombre d'auteurs : Commencer par créer une nouvelle colonne avec le nombre d'auteurs (taille de la liste de l'attribut authors), puis agrégez sur cette colonne avec l'accumulateur $count ou $sum.\n")
        f.write('books.aggregate([{"$project": {"nb_auteurs": {"$size": "$authors"}}}, {"$group": {"_id": "$nb_auteurs", "nb_livres": {"$sum": 1}}}])\n')
        agr = books.aggregate([{"$project": {"nb_auteurs": {"$size": "$authors"}}}, {"$group": {"_id": "$nb_auteurs", "nb_livres": {"$sum": 1}}}])
        f.write("Distribution du nombre d'auteurs:\n")
        json.dump(list(agr), f, indent=4, ensure_ascii=False)
        f.write("\n\n")

        # (j) Afficher l'occurrence de chaque auteur selon son index dans l'attribut "authors". Un même auteur peut avoir plusieurs index. N'affichez pas les auteurs vides, sortez par ordre d'occurrence décroissant avec une limite de 20. Utilisez "$unwind" pour séparer les auteurs et "$project" pour supprimer les auteurs absents.
        f.write('(j) Afficher l\'occurrence de chaque auteur selon son index dans l\'attribut "authors". Un même auteur peut avoir plusieurs index. N\'affichez pas les auteurs vides, sortez par ordre d\'occurrence décroissant avec une limite de 20. Utilisez "$unwind" pour séparer les auteurs et "$project" pour supprimer les auteurs absents.')
        f.write('agr = books.aggregate([{"$unwind": {"path": "$authors", "includeArrayIndex": "author_index"}}, {"$project": {"name": "$authors", "index": "$author_index"}}, {"$sort": {"index": -1}}, {"$limit": 20}])\n')
        agr = books.aggregate([{"$unwind": {"path": "$authors", "includeArrayIndex": "author_index"}}, {"$project": {"name": "$authors", "index": "$author_index"}}, {"$sort": {"index": -1}}, {"$limit": 20}])
        json.dump(list(agr), f, indent=4, ensure_ascii=False)
        f.write("\n\n")