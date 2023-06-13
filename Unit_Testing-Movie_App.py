import pytest
from unittest.mock import patch
from Movie_App import MovieApp


class MockResponse:
    def __init__(self, status_code=200, json_data=None):
        self.status_code = status_code
        self.json_data = json_data or {}

    def json(self):
        return self.json_data


class MockDB:
    def __init__(self, data=None):
        self.data = data or {}

    def get_data(self):
        return self.data


@pytest.fixture
def app():
    return MovieApp(MockDB())


def test_search_movie_from_omdb_success(app):
    """
    For testing add your API-KEY here as well as in the Movie_App.py
    """
    with patch('requests.get', return_value=MockResponse(200, {'Response': 'True', 'movie': 'Some Movie'})) as mock_get:
        data = app.search_movie_from_omdb('Some Movie')
        assert data == {'Response': 'True', 'movie': 'Some Movie'}
        mock_get.assert_called_once_with('http://www.omdbapi.com/?apikey=YOUR-API-KEY&t=Some Movie')


def test_search_movie_from_omdb_not_found(app):
    with patch('requests.get', return_value=MockResponse(404, {})):
        data = app.search_movie_from_omdb('Non Existent Movie')
        assert data is None


def test_search_movie_from_omdb_server_error(app):
    with patch('requests.get', return_value=MockResponse(500, {})):
        data = app.search_movie_from_omdb('Some Movie')
        assert data is None


def test_calculate_average_positive_numbers(app):
    movies = {'Movie1': {'rating': 1}, 'Movie2': {'rating': 2}, 'Movie3': {'rating': 3}, 'Movie4': {'rating': 4},
              'Movie5': {'rating': 5}}
    assert app._calculate_average(movies) == 3


def test_calculate_average_zero(app):
    movies = {'Movie1': {'rating': 0}, 'Movie2': {'rating': 0}, 'Movie3': {'rating': 0}, 'Movie4': {'rating': 0},
              'Movie5': {'rating': 0}}
    assert app._calculate_average(movies) == 0


def test_calculate_average_negative_numbers(app):
    movies = {'Movie1': {'rating': -1}, 'Movie2': {'rating': -2}, 'Movie3': {'rating': -3}, 'Movie4': {'rating': -4},
              'Movie5': {'rating': -5}}
    assert app._calculate_average(movies) == -3


def test_calculate_median_odd_length(app):
    assert app._calculate_median([1, 2, 3, 4, 5]) == 3


def test_calculate_median_even_length(app):
    assert app._calculate_median([1, 2, 3, 4]) == 2.5


def test_calculate_median_single_number(app):
    assert app._calculate_median([50]) == 50
