import csv
import os

from dotenv import load_dotenv

load_dotenv()


def get_movies(app):
    elements = []
    headers = []
    # Make sure this path is actually pointing to the file you updated!
    csv_path = os.path.join(
        app.root_path, "movie_agent_package/static", os.getenv("FILE_NAME")
    )

    try:
        with open(csv_path, "r", encoding="utf-8-sig") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=";")

            # --- DEBUGGING START ---
            # Print the headers Python found.
            print("CSV Headers found:", reader.fieldnames)
            # --- DEBUGGING END ---

            # Robust fix: Strip whitespace from headers just in case
            # (e.g., "Movie Title " becomes "Movie Title")
            if reader.fieldnames:
                reader.fieldnames = [name.strip() for name in reader.fieldnames]
                headers = reader.fieldnames

            for row in reader:
                elements.append(row)

    except FileNotFoundError:
        print(f"Error: File not found at {csv_path}")
        pass
    except Exception as e:
        print(f"An error occurred: {e}")

    return elements, headers
