import pytest
import os
from Storage_Json import StorageJson


storage_file = 'test_movies.json'
storage = StorageJson(storage_file)


def test_add_movie():
    storage.add_movie("Test Movie", 2000, 8.0, "poster_url", "imdb_url")
    movies = storage.list_movies()
    assert "Test Movie" in movies


def test_add_existing_movie():
    with pytest.raises(RuntimeError):
        storage.add_movie("Test Movie", 2000, 8.0, "poster_url", "imdb_url")


def test_delete_movie():
    storage.delete_movie("Test Movie")
    movies = storage.list_movies()
    assert "Test Movie" not in movies


def test_delete_non_existent_movie():
    with pytest.raises(RuntimeError):
        storage.delete_movie("Non Existent Movie")


def test_update_movie():
    storage.add_movie("Test Movie 2", 2001, 7.5, "poster_url_2", "imdb_url_2")
    storage.update_movie("Test Movie 2", "Great movie!")
    movies = storage.list_movies()
    assert movies["Test Movie 2"]["notes"] == "Great movie!"


def test_update_non_existent_movie():
    with pytest.raises(RuntimeError):
        storage.update_movie("Non Existent Movie", "Can't update this movie")


def test_contains():
    assert "Test Movie 2" in storage
    assert "Non Existent Movie" not in storage


def teardown_module(module):
    if os.path.exists(storage_file):
        os.remove(storage_file)
