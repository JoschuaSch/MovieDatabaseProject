import random
import requests
from config import API_KEY


class MovieApp:
    def __init__(self, storage):
        """Initializes a MovieApp object with the provided storage."""
        self.storage = storage
        self.OMDB_API_KEY = API_KEY

    def search_movie_from_omdb(self, title):
        """Searches for a movie on OMDB API based on the title and returns the movie data if found.
        Uses the API_KEY from the config.py"""
        response = requests.get(f"http://www.omdbapi.com/?apikey={self.OMDB_API_KEY}&t={title}")
        if response.status_code == 200:
            data = response.json()
            if data['Response'] == 'True':
                return data
            else:
                print("Movie not found.")
        else:
            print("Error while connecting to the OMDb API.")
        return None

    def _command_list_movies(self):
        """
        Gets and Prints a list of the movies stored in the database.
        """
        movies = self.storage.list_movies()
        if not movies:
            print("No movies found in the database.")
        else:
            for movie, data in movies.items():
                print(f"{movie} ({data['year']}) - Rating: {data['rating']}")

    def _command_add_movie(self):
        """
        Adds a new movie to the database from OMDB.
        """
        title = input("Enter the new movie name: ")
        movies = self.storage.list_movies()
        if any(movie_title.lower() == title.lower() for movie_title in movies):
            print("The movie already exists in the database.")
            return
        movie_data = self.search_movie_from_omdb(title)
        if movie_data and title.lower() == movie_data['Title'].lower():
            year = movie_data.get("Year")
            rating = movie_data.get("imdbRating")
            poster = movie_data.get("Poster")
            imdb_id = movie_data.get("imdbID")
            imdb_url = f"https://www.imdb.com/title/{imdb_id}/"
            if not year or not rating or not poster or not imdb_id:
                print("The movie data from the OMDb API is missing some necessary information.")
                return
            try:
                year = int(year)
                rating = float(rating)
            except ValueError:
                print("Couldn't convert Year or imdbRating to numeric types.")
                return
            print("\n************")
            print("Movie Found:")
            print(f"Title: {movie_data['Title']}")
            print(f"Year: {year}")
            print(f"Rating: {rating}")
            print(f"Poster: {poster}")
            print(f"IMDb URL: {imdb_url}")
            print("************\n")
            confirmation = input(f"\nDo you want to add {movie_data['Title']} ({year}) ? (y/n): ")
            if confirmation.lower() != "y":
                print("Movie addition canceled.")
                return
            try:
                self.storage.add_movie(movie_data['Title'], year, rating, poster, imdb_url)
                print(f"The movie {movie_data['Title']} ({year}) was added successfully.")
            except RuntimeError as e:
                print(str(e))

    def _command_delete_movie(self):
        """
        Deletes a movie from our database. The user is prompted for the name to delete and if he
        really wants to delete it.
        """
        title = input("Enter the movie name to delete: ").lower()
        movies = self.storage.list_movies()
        matches = [(movie, properties['year']) for movie, properties in movies.items() if title in movie.lower()]
        if not matches:
            print(f"No movies found with the name '{title}'.")
        else:
            if len(matches) == 1:
                selected_movie = matches[0]
            else:
                print("Multiple movies found with the given name:")
                for i, match in enumerate(matches, start=1):
                    print(f"{i}. {match[0]} ({match[1]})")
                choice = input("Enter the number of the movie to delete (0 to cancel): ")
                if choice.isdigit() and 0 < int(choice) <= len(matches):
                    selected_movie = matches[int(choice) - 1]
                else:
                    if choice != "0":
                        print("Invalid choice.")
                    print("Deletion cancelled.")
                    return
            confirm = input(f"Are you sure you want to delete '{selected_movie[0]}' ({selected_movie[1]})? (y/n): ")
            if confirm.lower() == "y":
                self.storage.delete_movie(selected_movie[0])
                print(f"Movie '{selected_movie[0]}' ({selected_movie[1]}) deleted successfully.")
            else:
                print("Deletion cancelled.")

    def _command_update_movie(self):
        """
        Updates a movie note. The user is prompted for the name and new note.
        """
        title = input("Enter the movie name: ").lower()
        movies = self.storage.list_movies()
        matches = [(movie, properties['year']) for movie, properties in movies.items() if title in movie.lower()]
        if not matches:
            print(f"No movies found with the name '{title}'.")
            add_movie = input("Would you like to add this movie instead? (y/n): ")
            if add_movie.lower() == "y":
                self._command_add_movie()
        else:
            if len(matches) == 1:
                selected_movie = matches[0]
            else:
                print("Multiple movies found with the given name:")
                for i, match in enumerate(matches, start=1):
                    print(f"{i}. {match[0]} ({match[1]})")
                choice = input("Enter the number of the movie to update (0 to cancel): ")
                if choice.isdigit() and 0 < int(choice) <= len(matches):
                    selected_movie = matches[int(choice) - 1]
                else:
                    if choice != "0":
                        print("Invalid choice.")
                    print("Update cancelled.")
                    return
            confirm = input(f"Are you sure you want to update '{selected_movie[0]}' ({selected_movie[1]})? (y/n): ")
            if confirm.lower() == "y":
                current_notes = movies[selected_movie[0]]['notes']
                print(f"Current notes: {current_notes}")
                new_notes = input("Enter new movie notes: ")
                self.storage.update_movie(selected_movie[0], new_notes)
                print(f"Movie '{selected_movie[0]}' ({selected_movie[1]}) updated successfully.")
            else:
                print("Update cancelled.")

    @staticmethod
    def _calculate_median(ratings):
        """
        Calculates the median rating of the movies.
        """
        if not ratings:
            return 0.0
        ratings = sorted(ratings)
        length = len(ratings)
        if length % 2 == 0:
            median = (ratings[length // 2 - 1] + ratings[length // 2]) / 2
        else:
            median = ratings[length // 2]
        return median

    @staticmethod
    def _calculate_average(movies):
        """
        Calculates the average rating of the movies.
        """
        ratings = [properties['rating'] for properties in movies.values()]
        if not ratings:
            return 0.0
        return sum(ratings) / len(ratings)

    @staticmethod
    def _get_highest_rated_movie(movies):
        """
        Get´s the highest rated movie from the database.
        """
        if movies:
            return max(movies.items(), key=lambda movie: movie[1]['rating'])[0]
        return None

    @staticmethod
    def _get_lowest_rated_movie(movies):
        """
        Get´s the lowest rated movie from the database.
        """
        if movies:
            return min(movies.items(), key=lambda movie: movie[1]['rating'])[0]
        return None

    def _command_stats_of_movies(self):
        """Displays statistics of the movies including average, median, highest and lowest rated movies."""
        json_movies = self.storage.list_movies()
        csv_movies = self.storage.list_movies()
        movies = {**json_movies, **csv_movies}
        if not movies:
            print("No movies found in the database.")
        else:
            ratings = sorted([properties['rating'] for properties in movies.values()])
            median_rating = MovieApp._calculate_median(ratings)
            average_rating = MovieApp._calculate_average(movies)
            rounded_average_rating = round(average_rating, 3)
            print(f"\nAverage rating: {rounded_average_rating}")
            print(f"Median rating: {median_rating}")
            highest_rated = MovieApp._get_highest_rated_movie(movies)
            if highest_rated:
                print(f"Best movie: {highest_rated} with a rating of {movies[highest_rated]['rating']}")
            else:
                print("No movies found in the database.")
            lowest_rated = MovieApp._get_lowest_rated_movie(movies)
            if lowest_rated:
                print(f"Worst movie: {lowest_rated} with a rating of {movies[lowest_rated]['rating']}")
            else:
                print("No movies found in the database.")

    def _command_random_movie(self):
        """Selects a random movie from the database and displays it along with its rating."""
        movies = self.storage.list_movies()
        if not movies:
            print("No movies found in the database.")
        else:
            randomized_movie = random.choice(list(movies.keys()))
            rating = movies[randomized_movie]["rating"]
            print(f"Your movie for tonight: {randomized_movie} (rated {rating})")

    def _command_search_movie(self):
        """Searches for a movie based on the user query and displays it along with its rating and year."""
        user_query = input("Enter part of the movie name to search it: ")
        movies = self.storage.list_movies()
        found = False
        for movie, properties in movies.items():
            if user_query.lower() in movie.lower():
                print(f"{movie}, Rating: {properties['rating']}, Year: {properties['year']}")
                found = True
        if not found:
            print("No movies found with your given search query.")

    def _command_movies_sorted_by_rating(self):
        """Sorts the movies by their rating in descending order and displays the sorted list."""
        json_movies = self.storage.list_movies()
        csv_movies = self.storage.list_movies()
        movies = {**json_movies, **csv_movies}
        if not movies:
            print("No movies found in the database.")
        else:
            sorted_movies = sorted(movies.items(), key=lambda item: item[1]['rating'], reverse=True)
            print(f"\nMovies sorted by rating:")
            for movie, properties in sorted_movies:
                print(f"{movie}: {properties['rating']}")

    def _command_generate_website(self):
        """
        Generate a movie list website based on the movies stored in the movies. files.
        """
        movies = self.storage.list_movies()
        if not movies:
            print("No movies found in the database.")
            return
        movie_grid = ""
        for movie, properties in movies.items():
            note = properties.get("notes", "")
            note_html = f"<div class='movie-note'>{note}</div>" if note else ""
            poster_url = properties.get("poster_url", "https://via.placeholder.com/150")
            imdb_url = properties.get("imdb_url", "#")
            movie_rating = properties.get("rating", "N/A")
            movie_year = properties.get("year", "N/A")
            movie_grid += (
                f'<li><div class="movie">'
                f'<a href="{imdb_url}" target="_blank">'
                f'<img src="{poster_url}" alt="{movie} Poster" class="movie-poster">'
                f'</a><div class="movie-details">'
                f'<div class="movie-title">{movie} ({movie_year})</div>'
                f'<div class="movie-rating">Rating: {movie_rating}</div>{note_html}'
                f'</div></div></li>'
            )
        with open("index_template.html", "r") as file:
            template = file.read()
        template = template.replace("__TEMPLATE_TITLE__", "My Favorite Movies")
        template = template.replace("__TEMPLATE_MOVIE_GRID__", movie_grid)
        with open("index.html", "w") as file:
            file.write(template)
        print("Website generated!")

    def run(self):
        """
        Runs the movie app, displaying the main menu and allowing for input.
        """
        print("\n********** My Movies Database **********")
        try:
            while True:
                print("\nMenu:")
                print("0. Exit")
                print("1. List of the movies")
                print("2. Add a movie")
                print("3. Delete a movie")
                print("4. Update a movie")
                print("5. Stats of the movies")
                print("6. Random movie")
                print("7. Search a movie")
                print("8. Movies sorted by their rating")
                print("9. Generate website")
                try:
                    choice_of_the_user = int(input("Enter a choice (0-9): "))
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    continue
                if choice_of_the_user == 0:
                    print("Goodbye!")
                    break
                elif choice_of_the_user == 1:
                    self._command_list_movies()
                elif choice_of_the_user == 2:
                    self._command_add_movie()
                elif choice_of_the_user == 3:
                    self._command_delete_movie()
                elif choice_of_the_user == 4:
                    self._command_update_movie()
                elif choice_of_the_user == 5:
                    self._command_stats_of_movies()
                elif choice_of_the_user == 6:
                    self._command_random_movie()
                elif choice_of_the_user == 7:
                    self._command_search_movie()
                elif choice_of_the_user == 8:
                    self._command_movies_sorted_by_rating()
                elif choice_of_the_user == 9:
                    try:
                        self._command_generate_website()
                    except IOError:
                        print(
                            "An error occurred trying to generate the website. Make sure the template exists/readable.")
                else:
                    print("Invalid choice. Enter a number between 0 and 9.")
                input("\nPress enter to continue: ")
        except Exception as e:
            print("An unexpected error occurred:")
            print(str(e))
