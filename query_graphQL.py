import graphene
from pymongo import MongoClient

# Connexion au serveur MongoDB
client = MongoClient('mongodb+srv://hubertvecchioli:XXXX@cluster0.XXXX.mongodb.net/')
db = client['test_db']
users_collection = db['test']

# Définir un type GraphQL pour User
class User(graphene.ObjectType):
    name = graphene.String()
    age = graphene.Int()
    email = graphene.String()

# Query pour récupérer tous les utilisateurs
class Query(graphene.ObjectType):
    users = graphene.List(User)

    def resolve_users(self, info):
        # Requête MongoDB pour récupérer les utilisateurs
        users = list(users_collection.find())
        return [User(name=user['name'], age=user['age']) for user in users]

# Schéma GraphQL
schema = graphene.Schema(query=Query)

# Exécuter des requêtes GraphQL dans ce script pour tester
query = '''
{
    users {
        name
        age
        email
    }
}
'''

result = schema.execute(query)
print(result.data)