import duckdb

# Connect to DuckDB
conn = duckdb.connect(database=":memory:")

def load_data(csv_file_path):
    """Load the movie dataset into DuckDB only if the table doesn't already exist."""
    # Check if the 'movies' table exists
    table_exists = conn.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'movies'").fetchone()[0]
    
    if table_exists == 0:
        # Table doesn't exist, so load the data
        conn.execute(f"CREATE TABLE movies AS SELECT * FROM read_csv_auto('{csv_file_path}')")
        print("Data loaded successfully into DuckDB!")
    else:
        print("Table 'movies' already exists. Skipping data load.")

def get_top_rated_movies(limit=10):
    """Retrieve the top-rated movies."""
    query = f"""
    SELECT Series_Title, IMDB_Rating
    FROM movies
    ORDER BY IMDB_Rating DESC
    LIMIT {limit}
    """
    return conn.execute(query).fetchdf()

def get_movies_by_genre(genre):
    """Retrieve movies by a given genre."""
    query = f"""
    SELECT Series_Title, Genre, IMDB_Rating
    FROM movies
    WHERE Genre LIKE '%{genre}%'
    """
    return conn.execute(query).fetchdf()

def get_average_rating_by_genre():
    """Retrieve the average IMDb rating by genre."""
    query = """
    SELECT Genre, AVG(IMDB_Rating) AS Avg_Rating 
    FROM movies 
    GROUP BY Genre 
    ORDER BY Avg_Rating DESC
    """
    return conn.execute(query).fetchdf()

def get_movies_with_high_votes(min_votes):
    """Retrieve movies with a high number of votes."""
    query = f"""
    SELECT Series_Title, IMDB_Rating, No_of_Votes
    FROM movies
    WHERE No_of_Votes >= {min_votes}
    """
    return conn.execute(query).fetchdf()
