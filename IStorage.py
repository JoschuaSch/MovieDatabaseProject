from abc import ABC, abstractmethod


class IStorage(ABC):
    """
    Interface for storage operations.
    """

    @abstractmethod
    def list_movies(self):
        """
        Should return a list of movies.
        """
        pass

    @abstractmethod
    def add_movie(self, title, year, rating, poster, imdb_url):
        """
        Should add a movie with given parameters.
        """
        pass

    @abstractmethod
    def delete_movie(self, title):
        """
        Should delete a movie with given title.
        """
        pass

    @abstractmethod
    def update_movie(self, title, notes):
        """
        Should update a movie with given title and notes.
        """
        pass
