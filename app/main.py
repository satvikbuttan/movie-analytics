import streamlit as st
import pandas as pd
from queries import load_data, get_top_rated_movies, get_movies_by_genre, get_average_rating_by_genre, get_movies_with_high_votes

# Path to the CSV file
csv_file_path = "data/movies.csv"  

# Load data into DuckDB
load_data(csv_file_path)

def main():
    st.title("Movie Analytics with DuckDB")

    # Sidebar for navigation
    st.sidebar.header("Navigation")
    options = ["Download Dataset", "Top Rated Movies", "Movies by Genre", "Average IMDb Ratings by Genre", "Movies with High Votes"]
    selection = st.sidebar.radio("Choose an option", options)

    # Display selected option
    if selection == "Top Rated Movies":
        st.header("Top Rated Movies")
        limit = st.slider("Select the number of top-rated movies to display", min_value=5, max_value=20, value=10)
        top_rated = get_top_rated_movies(limit)
        st.write(top_rated)
        st.write(f"Number of rows: {len(top_rated)}")  # Display number of rows

    elif selection == "Movies by Genre":
        st.header("Movies by Genre")
        genre = st.text_input("Enter the genre (e.g., Action, Drama, Comedy):", "Action")
        movies_by_genre = get_movies_by_genre(genre)
        st.write(movies_by_genre)
        st.write(f"Number of rows: {len(movies_by_genre)}")  # Display number of rows

    elif selection == "Average IMDb Ratings by Genre":
        st.header("Average IMDb Ratings by Genre")
        avg_ratings = get_average_rating_by_genre()
        st.write(avg_ratings)
        st.write(f"Number of rows: {len(avg_ratings)}")  # Display number of rows

    elif selection == "Movies with High Votes":
        st.header("Movies with High Number of Votes")
        min_votes = st.number_input("Enter the minimum number of votes:", min_value=100000, value=1000000)
        high_vote_movies = get_movies_with_high_votes(min_votes)
        st.write(high_vote_movies)
        st.write(f"Number of rows: {len(high_vote_movies)}")  # Display number of rows

    elif selection == "Download Dataset":
        st.header("Download Complete Dataset")
        st.write("Click the button below to download the complete movie dataset (CSV file).")

        # Read the dataset using pandas to provide the file for download
        df = pd.read_csv(csv_file_path)

        # Display the number of rows in the dataset
        st.write(f"Number of rows in the dataset: {len(df)}")

        # Create a download button
        st.download_button(
            label="Download CSV",
            data=df.to_csv(index=False),  # Convert DataFrame to CSV
            file_name="movies_dataset.csv",  # Name of the file to be downloaded
            mime="text/csv"  # MIME type for CSV
        )

if __name__ == "__main__":
    main()
