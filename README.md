# 🎬 BingeFlix

> **Your next movie obsession starts here. 🍿**

BingeFlix is a **content-based movie recommendation system** built with
Python and Machine Learning. It recommends movies based on the similarity
between movie features such as **genres, keywords, cast, and crew**.

The recommendation model is deployed as an interactive **Streamlit web
application**, with movie posters and additional information fetched using
the **TMDB API**.

---

## 🚀 Live Demo

👉 **[Try BingeFlix](https://bingeflix-o9l5xomtjivh323wuyqcw4.streamlit.app/)**

---

## 📸 Screenshots

### 🏠 BingeFlix Home

![BingeFlix Home](<img width="960" height="1600" alt="BingeFlix_Homepage" src="https://github.com/user-attachments/assets/7e1d6b0c-0f38-4016-a005-d46d5cfec9dc" />
)

### 🎬 Movie Recommendations

![BingeFlix Recommendations](<img width="1036" height="1600" alt="BingeFlix_recommendation" src="https://github.com/user-attachments/assets/d9158c83-0ba6-48da-bbec-e29fd12e8d68" />
)

---

## ✨ Features

- 🎬 Content-based movie recommendations
- 🔍 Movie selection and search
- ⭐ Movie ratings
- 🎭 Genre information
- 🖼️ Movie posters using TMDB API
- 🔥 Trending movies
- 🎨 Dark-themed Streamlit interface
- ⚡ Fast recommendations using precomputed similarity data

---

## 🧠 How the Recommendation System Works

BingeFlix uses a **content-based filtering approach**.

### Step 1 — Dataset

The project uses the **TMDB 5000 Movies** and **TMDB 5000 Credits**
datasets.

### Step 2 — Feature Selection

Important movie information is extracted, including:

- Genres
- Keywords
- Cast
- Crew
- Movie title
- Movie ID

### Step 3 — Feature Combination

Relevant movie features are combined into a single textual representation
for each movie.

### Step 4 — Vectorization

The text representation is converted into numerical vectors using
**CountVectorizer**.

### Step 5 — Similarity Calculation

**Cosine similarity** is calculated between movie vectors to determine how
similar two movies are.

### Step 6 — Recommendation

When a user selects a movie, BingeFlix finds the movies with the highest
similarity scores and displays them as recommendations.

### Step 7 — TMDB API

The TMDB API is used to retrieve movie posters and additional movie
information for the application.

---

## 🗂️ Dataset

The project uses:

**TMDB 5000 Movies Dataset**

**TMDB 5000 Credits Dataset**

Important features include:

- Genres
- Keywords
- Cast
- Crew
- Movie title
- Movie ID

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| 🐍 Python | Core programming |
| 🐼 Pandas | Data manipulation |
| 🔢 NumPy | Numerical operations |
| 🤖 Scikit-learn | Machine learning & vectorization |
| 🎨 Streamlit | Web application |
| 🎬 TMDB API | Movie posters & information |
| 📦 Pickle | Storing precomputed model data |
| 🐙 GitHub | Version control & project hosting |

---

## 📁 Project Structure

```text
BingeFlix/
│
├── BingeFlix.py
│       └── Main Streamlit application
│
├── movie_dict.pkl
│       └── Processed movie information
│
├── similarity.pkl
│       └── Precomputed cosine similarity matrix
│
├── BingeFlix_home.png
│       └── Application homepage screenshot
│
├── BingeFlix_recommendations.png
│       └── Recommendation page screenshot
│
├── README.md
│       └── Project documentation
│
├── .gitignore
└── .gitattributes
