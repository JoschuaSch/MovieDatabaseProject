import pytest
from Storage_Csv import StorageCsv

storage_file = 'test_movies.csv'


def setup_function(function):
    with open('test_movies.csv', 'w') as f:
        f.write("title,year,rating,poster_url,imdb_url\n")


def test_add_movie():
    storage = StorageCsv(storage_file)
    storage.add_movie("Test Movie", 2000, 8.0, "poster_url", "imdb_url")
    movies = storage.list_movies()
    assert "Test Movie" in movies


def test_add_existing_movie():
    storage = StorageCsv(storage_file)
    storage.add_movie("Test Movie", 2000, 8.0, "poster_url", "imdb_url")
    with pytest.raises(RuntimeError):
        storage.add_movie("Test Movie", 2000, 8.0, "poster_url", "imdb_url")


def test_delete_movie():
    storage = StorageCsv(storage_file)
    storage.add_movie("Test Movie", 2000, 8.0, "poster_url", "imdb_url")
    storage.delete_movie("Test Movie")
    movies = storage.list_movies()
    assert "Test Movie" not in movies


def test_delete_non_existent_movie():
    storage = StorageCsv(storage_file)
    with pytest.raises(RuntimeError):
        storage.delete_movie("Non Existent Movie")


def test_update_movie():
    storage = StorageCsv(storage_file)
    storage.add_movie("Test Movie", 2000, 8.0, "poster_url", "imdb_url")
    storage.update_movie("Test Movie", "New Note")
    movies = storage.list_movies()
    assert movies["Test Movie"]["notes"] == "New Note"


def test_update_non_existent_movie():
    storage = StorageCsv(storage_file)
    with pytest.raises(RuntimeError):
        storage.update_movie("Non Existent Movie", new_note="This is a new note")


def test_contains():
    storage = StorageCsv(storage_file)
    storage.add_movie("Test Movie", 2000, 8.0, "poster_url", "imdb_url")
    assert "Test Movie" in storage
    assert "Non Existent Movie" not in storage
