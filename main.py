import os
import argparse

from Movie_App import MovieApp
from Storage_Csv import StorageCsv
from Storage_Json import StorageJson


def main():
    """
        Movie App

        Main File of the Movie App. It allows users to manage our collection of movies
        stored in either a JSON or CSV file. The script accepts a command-line argument specifying
        the movie storage we use. The file can have a .json or .csv extension.

        How to use it:
            python3 main.py movies.json
            python3 main.py movies.csv
        """

    parser = argparse.ArgumentParser(description='Movie App')
    parser.add_argument('filename', help='Path to the .json or .csv file to be used for movie storage')
    args = parser.parse_args()

    filename = args.filename
    script_dir = os.path.dirname(__file__)
    full_path = os.path.join(script_dir, filename)

    if full_path.endswith('.json'):
        storage = StorageJson(full_path)
    elif full_path.endswith('.csv'):
        storage = StorageCsv(full_path)
    else:
        print('Invalid file extension. Please use a .json or .csv file.')
        return

    app = MovieApp(storage)
    app.run()


if __name__ == "__main__":
    main()

# If you want to use it manually(Keep the indentation in mind)
# from WebsiteMovie.Movie_App import MovieApp
# from WebsiteMovie.Storage_Csv import StorageCsv
# from WebsiteMovie.Storage_Json import StorageJson


# def main():
# storage = StorageCsv('movies.csv')
# storage = StorageJson('movies.json')

# app = MovieApp(storage)
# app.run()


# if __name__ == "__main__":
# main()
