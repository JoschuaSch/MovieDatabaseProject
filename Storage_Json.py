import json
from IStorage import IStorage


class StorageJson(IStorage):
    def __init__(self, storage_file):
        self.storage_file = storage_file

    def list_movies(self):
        """Lists all the movies from the JSON file as a dictionary."""
        try:
            with open(self.storage_file, 'r') as file:
                movies = json.load(file)
                return movies
        except FileNotFoundError:
            return {}

    def add_movie(self, title, year, rating, poster, imdb_url):
        """Adds a new movie to the JSON file with the provided details."""
        movies = self.list_movies()
        if title in movies:
            raise RuntimeError(f"Movie with title '{title}' already exists.")
        movie = {
            'title': title,
            'year': year,
            'rating': rating,
            'poster_url': poster,
            'imdb_url': imdb_url,
            'notes': ''
        }
        movies[title] = movie
        self._save_movies(movies)

    def delete_movie(self, title):
        """Deletes the movie with the given title from the JSON file."""
        movies = self.list_movies()
        if title not in movies:
            raise RuntimeError(f"No movie with title '{title}' found.")
        del movies[title]
        self._save_movies(movies)

    def update_movie(self, title, new_note=None):
        """Updates the notes of the movie with the given title in the JSON file."""
        movies = self.list_movies()
        if title not in movies:
            raise RuntimeError(f"No movie with title '{title}' found.")
        if new_note is None:
            update_decision = input("Do you want to update the note? (y/n): ")
            if update_decision.lower() != "y":
                print("Update cancelled.")
                return
            new_note = input("Enter the new note: ")
        movies[title]['notes'] = new_note
        self._save_movies(movies)

    def _save_movies(self, movies):
        """Saves the movies dictionary to the JSON file."""
        with open(self.storage_file, 'w') as file:
            json.dump(movies, file, indent=4)

    def __contains__(self, title):
        """Checks if the movie with the given title exists in the JSON file."""
        movies = self.list_movies()
        return title in movies
