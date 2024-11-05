import graphene
from pymongo import MongoClient

# Connexion au serveur MongoDB
client = MongoClient('mongodb+srv://hubertvecchioli:XXXX@cluster0.XXXX.mongodb.net/')
db = client['sample_mflix']  # Assuming 'sample_mflix' is the database
collection = db['embedded_movies']

# Define a GraphQL ObjectType for Movies
class Movie(graphene.ObjectType):
    title = graphene.String()
    year = graphene.Int()
    rated = graphene.String()
    genres = graphene.List(graphene.String)
    directors = graphene.List(graphene.String)
    cast = graphene.List(graphene.String)
    plot = graphene.String()
    runtime = graphene.Int()
    languages = graphene.List(graphene.String)

# Query to fetch a multiple movie by title
class Query(graphene.ObjectType):
    movies = graphene.List(Movie, title=graphene.String(), year=graphene.Int())

    def resolve_movies(self, info, title=None, year=None):
        query = {}
        if title:
            query["title"] = title
        if year:
            query["year"] = year

        movies_cursor = collection.find(query)

        movies_list = []
        for movie in movies_cursor:
            movies_list.append(
                Movie(
                    title=movie.get("title"),
                    year=movie.get("year"),
                    rated=movie.get("rated"),
                    genres=movie.get("genres"),
                    directors=movie.get("directors"),
                    cast=movie.get("cast"),
                    plot=movie.get("plot"),
                    runtime=movie.get("runtime"),
                    languages=movie.get("languages"),
                )
            )
        return movies_list
    
schema = graphene.Schema(query=Query)

# Un exemple de query qui devrait me retourner 'The Perils of Pauline'
query_string = '''
{
    movies(year: 1914) {
        title
        year
        rated
        cast
        runtime
        languages
    }
}
'''

result = schema.execute(query_string)
print(result.data)


class CreateMovie(graphene.Mutation):
	class Arguments:
		title = graphene.String()
		year = graphene.Int()
		rated = graphene.String()
		genres = graphene.List(graphene.String)
		directors = graphene.List(graphene.String)
		cast = graphene.List(graphene.String)
		plot = graphene.String()
		runtime = graphene.Int()
		languages = graphene.List(graphene.String)

	# Création du schéma
	movie = graphene.Field(lambda: Movie)

	def mutate(self, info, title, year, plot):
		new_movie = {"title": title, "year": year, "plot": plot}
		collection.insert_one(new_movie)
		return CreateMovie(movie=Movie(title=title, year=year, plot=plot))

class Mutation(graphene.ObjectType):
	create_movie = CreateMovie.Field()

# Schéma GraphQL avec mutation
schema = graphene.Schema(query=Query, mutation=Mutation)

# Exemple de mutation pour ajouter un utilisateur
mutation = '''
mutation {
  createMovie(title: "Dave", year: 1914, plot: "dave@plot.com") {
    movie {
      title
      year
      plot
    }
  }
}
'''

result = schema.execute(mutation)
if result.errors:
    print(f"Errors: {result.errors}")
else:
    print(result.data)