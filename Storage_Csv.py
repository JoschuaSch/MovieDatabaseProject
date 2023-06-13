import csv
from IStorage import IStorage


class StorageCsv(IStorage):
    def __init__(self, storage_file):
        self.storage_file = storage_file
        self.fieldnames = self._get_fieldnames()

    def _get_fieldnames(self):
        """Retrieves the fieldnames from the CSV file."""
        with open(self.storage_file) as f:
            reader = csv.reader(f)
            try:
                return next(reader)
            except StopIteration:
                return None

    def list_movies(self):
        """Lists all the movies from the CSV file as a dictionary."""
        try:
            with open(self.storage_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                movies = {}
                for row in reader:
                    movies[row['title']] = {
                        'title': row['title'],
                        'year': int(row['year']),
                        'rating': float(row['rating']),
                        'poster_url': row.get('poster_url', ''),
                        'imdb_url': row.get('imdb_url', ''),
                        'notes': row.get('notes', '')
                    }
                return movies
        except FileNotFoundError:
            return {}

    def add_movie(self, title, year, rating, poster, imdb_url):
        """Adds a new movie to the CSV file with the provided details."""
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
        """Deletes the movie with the given title from the CSV file."""
        movies = self.list_movies()
        if title in movies:
            del movies[title]
            self._save_movies(movies)
        else:
            raise RuntimeError(f"Movie with title '{title}' does not exist.")

    def update_movie(self, title, new_note=None):
        """Updates the notes of the movie with the given title in the CSV file."""
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
        """Saves the movies dictionary to the CSV file."""
        with open(self.storage_file, 'w', newline='', encoding='utf-8') as file:
            fieldnames = ['title', 'year', 'rating', 'poster_url', 'imdb_url', 'notes']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for movie in movies.values():
                writer.writerow({
                    'title': movie['title'],
                    'year': movie['year'],
                    'rating': movie['rating'],
                    'poster_url': movie['poster_url'],
                    'imdb_url': movie['imdb_url'],
                    'notes': movie.get('notes', '')
                })

    def __contains__(self, title):
        """Checks if the movie with the given title exists in the CSV file."""
        movies = self.list_movies()
        return title in movies
