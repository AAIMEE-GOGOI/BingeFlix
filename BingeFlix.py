
import streamlit as st
import pickle
import requests
import numpy as np
import pandas as pd
import os


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="BingeFlix",
    page_icon="🍿",
    layout="wide"
)


# ============================================================
# TMDB
# ============================================================

TMDB_API_KEY = os.getenv("TMDB_API_KEY")

TMDB_BASE = "https://api.themoviedb.org/3"
TMDB_IMAGE = "https://image.tmdb.org/t/p/w500"


# ============================================================
# LOAD MODEL
# ============================================================

try:

    with open("movie_dict.pkl", "rb") as f:
        movie_data = pickle.load(f)

    with open("similarity.pkl", "rb") as f:
        similarity = pickle.load(f)

except Exception as e:

    st.error(f"Could not load model files: {e}")
    st.stop()


# ============================================================
# CONVERT MODEL DATA TO DATAFRAME
# ============================================================

def load_movie_dataframe(data):

    # DataFrame
    if isinstance(data, pd.DataFrame):

        return data.copy()


    # Dictionary
    if isinstance(data, dict):

        # Example:
        # {"title": [...], "movie_id": [...], ...}

        if "title" in data:

            try:

                return pd.DataFrame(data)

            except Exception:

                pass


        # Example:
        # {0: {"title": "Avatar", ...}, ...}

        try:

            df = pd.DataFrame.from_dict(
                data,
                orient="index"
            )

            if "title" in df.columns:

                return df.reset_index(drop=True)

        except Exception:

            pass


    # List
    if isinstance(data, list):

        try:

            df = pd.DataFrame(data)

            if "title" in df.columns:

                return df.reset_index(drop=True)

        except Exception:

            pass


    return None


movies = load_movie_dataframe(movie_data)


# ============================================================
# CHECK DATA
# ============================================================

if movies is None or "title" not in movies.columns:

    st.error(
        "movie_dict.pkl does not contain a usable 'title' column."
    )

    st.stop()


movies["title"] = movies["title"].astype(str)

movies = movies.reset_index(drop=True)

movie_titles = movies["title"].tolist()


# ============================================================
# TMDB SEARCH
# ============================================================

@st.cache_data(show_spinner=False)
def tmdb_search(title):

    if not TMDB_API_KEY:

        return None

    try:

        response = requests.get(
            f"{TMDB_BASE}/search/movie",
            params={
                "api_key": TMDB_API_KEY,
                "query": title
            },
            timeout=10
        )

        if response.status_code != 200:

            return None

        results = response.json().get(
            "results",
            []
        )

        if not results:

            return None

        return results[0]

    except Exception:

        return None


# ============================================================
# TMDB GENRES
# ============================================================

@st.cache_data(show_spinner=False)
def tmdb_genres():

    if not TMDB_API_KEY:

        return {}

    try:

        response = requests.get(
            f"{TMDB_BASE}/genre/movie/list",
            params={
                "api_key": TMDB_API_KEY
            },
            timeout=10
        )

        if response.status_code != 200:

            return {}

        genres = response.json().get(
            "genres",
            []
        )

        return {
            g["id"]: g["name"]
            for g in genres
        }

    except Exception:

        return {}


GENRE_MAP = tmdb_genres()


# ============================================================
# MOVIE INFORMATION
# ============================================================

def movie_info(title):

    result = tmdb_search(title)

    if result is None:

        return {
            "title": title,
            "poster": None,
            "rating": None,
            "genres": "Genre unavailable"
        }


    poster_path = result.get("poster_path")

    if poster_path:

        poster = TMDB_IMAGE + poster_path

    else:

        poster = None


    rating = result.get("vote_average")


    genre_ids = result.get(
        "genre_ids",
        []
    )


    genres = [
        GENRE_MAP[g]
        for g in genre_ids
        if g in GENRE_MAP
    ]


    if genres:

        genre_text = " • ".join(genres)

    else:

        genre_text = "Genre unavailable"


    return {
        "title": result.get(
            "title",
            title
        ),
        "poster": poster,
        "rating": rating,
        "genres": genre_text
    }


# ============================================================
# RECOMMENDATION MODEL
# ============================================================

def recommend_movie(selected_movie):

    try:

        # Find movie index
        matches = movies.index[
            movies["title"].str.lower()
            == selected_movie.lower()
        ].tolist()


        if not matches:

            return []


        index = matches[0]


        # Similarity scores
        sim_scores = np.asarray(
            similarity[index]
        ).flatten()


        # Highest similarity first
        similar_indices = sim_scores.argsort()[::-1]


        recommendations = []


        for i in similar_indices:

            # Don't recommend the movie itself
            if i == index:

                continue


            if i >= len(movies):

                continue


            title = movies.iloc[i]["title"]


            if title not in recommendations:

                recommendations.append(title)


            # EXACTLY 5
            if len(recommendations) == 5:

                break


        return recommendations


    except Exception as e:

        st.error(
            f"Recommendation error: {e}"
        )

        return []


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
        radial-gradient(
            circle at top,
            #252525 0%,
            #111111 45%,
            #080808 100%
        );
        color: white;
    }


    .bingeflix-logo {
        text-align: center;
        font-size: 68px;
        font-weight: 900;
        color: #E50914;
        letter-spacing: -4px;
        margin-top: 20px;
        margin-bottom: 0px;
        font-family: Arial, Helvetica, sans-serif;
    }


    .welcome {
        text-align: center;
        font-size: 36px;
        font-weight: 800;
        margin-top: 5px;
    }


    .tagline {
        text-align: center;
        color: #dddddd;
        font-size: 18px;
        margin-bottom: 35px;
    }


    .section-title {
        font-size: 30px;
        font-weight: 800;
        margin-top: 35px;
        margin-bottom: 18px;
    }


    .stButton > button {
        background-color: #E50914;
        color: white;
        border: none;
        border-radius: 6px;
        font-size: 17px;
        font-weight: 700;
        padding: 10px 25px;
    }


    .stButton > button:hover {
        background-color: #b20710;
        color: white;
    }


    div[data-baseweb="select"] > div {
        background-color: #181818;
        border: 1px solid #555;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="bingeflix-logo">BingeFlix</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="welcome">Welcome to BingeFlix 🍿</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="tagline">Your next movie obsession starts here.</div>',
    unsafe_allow_html=True
)


# ============================================================
# DEFAULT 5 MOVIES FROM YOUR DATASET
# ============================================================

st.markdown(
    '<div class="section-title">🔥 Trending Movies</div>',
    unsafe_allow_html=True
)


# Take exactly 5 movies directly from your dataset
default_movies = movie_titles[:5]


# ============================================================
# DISPLAY DEFAULT MOVIES
# ============================================================

default_cols = st.columns(5)


for col, title in zip(
    default_cols,
    default_movies
):

    info = movie_info(title)

    with col:

        # Poster
        if info["poster"]:

            st.image(
                info["poster"],
                use_container_width=True
            )

        else:

            st.markdown(
                "🎬 Poster unavailable"
            )


        # Movie name
        st.markdown(
            f"**{info['title']}**"
        )


        # Rating
        if info["rating"] is not None:

            st.markdown(
                f"⭐ **{info['rating']:.1f}/10**"
            )

        else:

            st.markdown(
                "⭐ Rating unavailable"
            )


        # Genre
        st.caption(
            f"🎭 {info['genres']}"
        )


# ============================================================
# FIND MOVIE
# ============================================================

st.markdown(
    '<div class="section-title">🎬 Find Your Next Movie</div>',
    unsafe_allow_html=True
)

st.write(
    "Choose a movie you like"
)


# ONLY MOVIE TITLES
selected_movie = st.selectbox(
    "Movie",
    movie_titles,
    index=0,
    label_visibility="collapsed"
)


# ============================================================
# RECOMMEND BUTTON
# ============================================================

if st.button(
    "🔥 Recommend Movies"
):

    recommendations = recommend_movie(
        selected_movie
    )


    if recommendations:

        st.session_state["recommendations"] = recommendations

        st.session_state["selected_movie"] = selected_movie

    else:

        st.error(
            "No recommendations could be generated."
        )


# ============================================================
# SHOW EXACTLY 5 RECOMMENDATIONS
# ============================================================

if "recommendations" in st.session_state:

    selected = st.session_state[
        "selected_movie"
    ]


    st.markdown(
        '<div class="section-title">🍿 Movies You May Like</div>',
        unsafe_allow_html=True
    )


    st.write(
        f"Because you liked **{selected}**"
    )


    # EXACTLY 5 COLUMNS
    rec_cols = st.columns(5)


    for col, title in zip(
        rec_cols,
        st.session_state["recommendations"][:5]
    ):

        info = movie_info(title)


        with col:

            # Poster
            if info["poster"]:

                st.image(
                    info["poster"],
                    use_container_width=True
                )

            else:

                st.markdown(
                    "🎬 Poster unavailable"
                )


            # TITLE
            st.markdown(
                f"**{info['title']}**"
            )


            # RATING
            if info["rating"] is not None:

                st.markdown(
                    f"⭐ **{info['rating']:.1f}/10**"
                )

            else:

                st.markdown(
                    "⭐ Rating unavailable"
                )


            # GENRES
            st.caption(
                f"🎭 {info['genres']}"
            )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <hr>

    <p style="
        text-align:center;
        color:#999;
        padding:20px;
        font-size:14px;
    ">
        🍿 BingeFlix • Movie Recommendation System
        • Powered by ML + TMDB
    </p>
    """,
    unsafe_allow_html=True
)
