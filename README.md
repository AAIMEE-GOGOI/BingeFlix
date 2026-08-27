<div align="center">

<h1 style="color:#E50914; font-size:60px;">🍿 BingeFlix</h1>

<p><em>Your next movie obsession starts here.</em> 🍿</p>

<p>
BingeFlix is a content-based movie recommendation system built with
Python and Machine Learning.<br>
It recommends movies based on similarity between movie features such as
genres, keywords, cast, and crew.
</p>

</div>

---

## 🚀 Live Demo

<div align="center">

👉 **[Try BingeFlix](https://bingeflix-o9l5xomtjivh323wuyqcw4.streamlit.app/)**

</div>

---

## 📸 Screenshots

### 🏠 BingeFlix Home

<p align="center">
  <img src="Screenshots/BingeFlix_home.png" width="800">
</p>

### 🎬 Movie Recommendations

<p align="center">
  <img src="Screenshots/BingeFlix_recommendations.png" width="800">
</p>

---

## ✨ Features

- 🎬 Content-based movie recommendations
- 🔍 Movie selection and search
- ⭐ Movie ratings
- 🎭 Genre information
- 🖼️ Movie posters using TMDB API
- 🔥 Trending movies
- 🎨 Streamlit web interface

---

## 🧠 How It Works

1. Movie data is loaded from the TMDB 5000 dataset.
2. Relevant movie features are combined into a text representation.
3. Features are converted into numerical vectors.
4. Cosine similarity is used to measure similarity between movies.
5. BingeFlix finds the most similar movies to the selected movie.
6. TMDB API provides movie posters and additional information.

---

## 🗂️ Dataset

The project uses the **TMDB 5000 Movies** and **Credits** datasets.

### Main Features

- Movie title
- Movie ID
- Genres
- Keywords
- Cast
- Crew

---

## 🛠️ Technologies

- Python
- Pandas
- NumPy
- Scikit-learn
- Streamlit
- TMDB API
- Pickle
- GitHub

---

## 📁 Project Structure

```text
BingeFlix/
│
├── BingeFlix.py
├── movie_dict.pkl
├── similarity.pkl
├── Screenshots/
│   ├── BingeFlix_home.png
│   └── BingeFlix_recommendations.png
├── README.md
├── .gitignore
└── .gitattributes
