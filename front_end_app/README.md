# CSCI-GA 2433 2024 Fall Database Systems Final Project —— Frontend Page

# Frontend - React Music Streaming App

## Project Overview
This is a **React** based frontend application designed to interact with our music streaming backend server. The app is built to handle user interactions and provides functionalities such as:

- User registration and login
- Music search and playback
- Playlist management
- Song ratings and comments
- Real-time data updates

The frontend communicates with the backend via RESTful APIs and ensures data synchronization in real-time.

## Features

- **User Registration & Login**: Forms for users to register and log in.
- **Music Search & Playback**: Allows users to search for music by song, artist, or album and play selected tracks.
- **Playlist Management**: Users can create, delete, and modify playlists.
- **Song Ratings & Comments**: Users can rate songs and leave comments, helping others discover new music.
- **Real-Time Data Updates**: Using WebSockets or polling to sync data, such as song history, ratings, and comments in real time.

## Tech Stack

- **React**: Used for building the user interface.
- **React Router**: For handling page navigation.
- **Axios**: For making HTTP requests to the backend and handling data.
- **Socket.IO / WebSocket**: For real-time data updates (e.g., song playback state, comments, ratings).

## Installation and Setup

### 1. Clone the Repository

First, clone the frontend repository to your local machine:

### 2. Install Dependencies

Use npm or yarn to install the required dependencies

### 3. Configure Backend API

### 4. Run the Frontend Application

To run the app locally in development mode, use:
    npm start

## Connecting to the Backend

The frontend connects to the backend through **Axios** for making API requests.

## Contributing

If you'd like to contribute to the project, feel free to fork the repository and submit a pull request. Please ensure your code follows the project's coding conventions and includes appropriate tests.

## License

This project is licensed under the [MIT License](LICENSE). See the LICENSE file for details.
