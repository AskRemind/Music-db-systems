# CSCI-GA 2433 2024 Fall Final Project

## Project Overview
This is the **Final Project** for CSCI-GA 2433 (Software Engineering) in Fall 2024. The project implements a **small-scale backend server** for a music streaming application using **Python Flask** and integrates an **SQLite database** to support various use cases.

In this project, we have built several essential features for a music streaming service, including:

- User registration and login
- Music search
- Music playback
- Playlist management
- Song rating and commenting

This server is designed to handle basic interactions typically found in a music streaming platform, and it's built to be lightweight and easy to run locally.

## Features
- **User Registration & Login**: Users can register an account and log in to access personalized features.
- **Music Search**: Allows users to search for songs by title, artist, or album.
- **Music Playback**: Users can listen to songs directly from the server.
- **Playlist Management**: Users can create, edit, and manage playlists.
- **Song Rating & Comments**: Users can rate songs and leave comments, helping others discover new music.

## Getting Started

To get started with this project on your local machine, follow the steps below:

### Prerequisites
1. **Python**: Ensure you have the latest version of Python installed. You can download it from [python.org](https://www.python.org/downloads/).
   
2. **Required Libraries**: You will need to install the following libraries:
   - Flask
   - SQLite (which is included with Python by default)

   You can install the necessary dependencies using pip:
   
bash
   pip install -r requirements.txt


### Running the Project

1. Clone the repository:
   
bash
   git clone https://github.com/your-username/music-streaming-server.git
   cd music-streaming-server


2. Set up your local Python environment:
   - If you’re using a virtual environment (recommended):
     
bash
     python -m venv venv
     source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

   
3. Install the dependencies:
   
bash
   pip install -r requirements.txt


4. Run the server:
   
bash
   python app.py


   This will start the Flask server on http://localhost:5000.

5. Open your browser and navigate to http://localhost:5000 to access the application.

## Database

This project uses **SQLite** as the database backend. The database schema is set up automatically when the application is first run. It includes tables for storing user information, music data, playlists, ratings, and comments.

## Endpoints

Here’s a quick summary of the API endpoints available in this project:

- **POST /register**: Register a new user
- **POST /login**: Log in an existing user
- **GET /search**: Search for music by song title, artist, or album
- **GET /play**: Play a selected song
- **POST /playlist**: Create or update a playlist
- **POST /rate**: Rate a song
- **POST /comment**: Add a comment to a song

## Contributing

If you'd like to contribute to this project, feel free to fork the repository and create a pull request with your changes. Please ensure that your code adheres to the project's coding style and includes appropriate tests for any new features.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Flask for making web development easier.
- SQLite for providing a lightweight, easy-to-use database solution.
- The CSCI-GA 2433 course for offering this fun and challenging project opportunity! 

---

Feel free to reach out if you have any questions or run into any issues. Enjoy building and exploring the music streaming server!