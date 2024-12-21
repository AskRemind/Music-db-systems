import React, { useState, useEffect, useCallback } from "react";
import axios from "axios";
import "./Playlists.css";

const Playlists = () => {
    const [playlists, setPlaylists] = useState([]);
    const [selectedPlaylist, setSelectedPlaylist] = useState(null);
    const [newPlaylistTitle, setNewPlaylistTitle] = useState("");
    const [newSongId, setNewSongId] = useState("");
    const [songs, setSongs] = useState([]);
    const [message, setMessage] = useState("");
    const userId = JSON.parse(localStorage.getItem("user_info"))?.UserID;

    // Fetch playlists
    const fetchPlaylists = useCallback(async () => {
        if (!userId) {
            setMessage("Please log in.");
            return;
        }
        try {
            const response = await axios.get("http://127.0.0.1:5000/playlists/", {
                headers: { 'UserID': userId },
            });
            setPlaylists(response.data);
        } catch (error) {
            setMessage("Failed to fetch playlists.");
        }
    }, [userId]);

    useEffect(() => {
        fetchPlaylists();
    }, [fetchPlaylists]);

    // Create a new playlist
    const handleCreatePlaylist = async (e) => {
        e.preventDefault();
        if (!newPlaylistTitle.trim()) {
            setMessage("Playlist title cannot be empty.");
            return;
        }
        try {
            const response = await axios.post(
                "http://127.0.0.1:5000/playlists/",
                { title: newPlaylistTitle },
                { headers: { 'UserID': userId } }
            );
            setMessage(response.data.message);
            fetchPlaylists();
            setNewPlaylistTitle("");
        } catch (error) {
            setMessage(error.response?.data?.error || "Failed to create playlist.");
        }
    };

    // View playlist songs
    const handleSelectPlaylist = async (playlist) => {
        setSelectedPlaylist(playlist);
        try {
            const response = await axios.get(
                `http://127.0.0.1:5000/playlists/${playlist.playlist_id}/songs`,
                { headers: { 'UserID': userId } }
            );
            setSongs(response.data.songs);
        } catch (error) {
            setMessage("Failed to fetch songs.");
        }
    };

    // Add a song to a playlist
    const handleAddSong = async (e) => {
        e.preventDefault();
        if (!newSongId.trim()) {
            setMessage("Song ID cannot be empty.");
            return;
        }
        try {
            const response = await axios.post(
                `http://127.0.0.1:5000/playlists/${selectedPlaylist.playlist_id}/add-song`,
                { song_id: newSongId },
                { headers: { 'UserID': userId } }
            );
            setMessage(response.data.message);
            handleSelectPlaylist(selectedPlaylist);
            setNewSongId("");
        } catch (error) {
            setMessage(error.response?.data?.error || "Failed to add song.");
        }
    };

    // Delete a playlist
    const handleDeletePlaylist = async (playlistId) => {
        try {
            const response = await axios.delete(
                `http://127.0.0.1:5000/playlists/${playlistId}`,
                { headers: { 'UserID': userId } }
            );
            setMessage(response.data.message);
            fetchPlaylists();
            if (selectedPlaylist?.playlist_id === playlistId) {
                setSelectedPlaylist(null);
                setSongs([]);
            }
        } catch (error) {
            setMessage(error.response?.data?.error || "Failed to delete playlist.");
        }
    };

    // Remove a song from the playlist
    const handleRemoveSong = async (songId) => {
        if (!selectedPlaylist || !songId) {
            setMessage("Invalid playlist or song ID.");
            return;
        }
        try {
            const response = await axios.delete(
                `http://127.0.0.1:5000/playlists/${selectedPlaylist.playlist_id}/remove-song`,
                {
                    headers: { 'UserID': userId },
                    data: { song_id: songId }, 
                }
            );
            setMessage(response.data.message);
            handleSelectPlaylist(selectedPlaylist); 
        } catch (error) {
            setMessage(error.response?.data?.error || "Failed to remove song.");
        }
    };

    return (
        <div className="playlist-page">
            <h1>Your Playlists</h1>
            <div className="create-playlist">
                <form onSubmit={handleCreatePlaylist}>
                    <input
                        type="text"
                        placeholder="New Playlist Title"
                        value={newPlaylistTitle}
                        onChange={(e) => setNewPlaylistTitle(e.target.value)}
                        required
                    />
                    <button type="submit">Create Playlist</button>
                </form>
            </div>
            <div className="playlists-container">
                {playlists.map((playlist) => (
                    <div key={playlist.playlist_id} className="playlist-card">
                        <h2>{playlist.title || "Unnamed Playlist"}</h2>
                        <button onClick={() => handleSelectPlaylist(playlist)}>View</button>
                        <button onClick={() => handleDeletePlaylist(playlist.playlist_id)}>Delete</button>
                    </div>
                ))}
            </div>
            {selectedPlaylist && (
                <div className="playlist-details">
                    <h2>{selectedPlaylist.title}</h2>
                    <form onSubmit={handleAddSong}>
                        <input
                            type="text"
                            placeholder="Song ID"
                            value={newSongId}
                            onChange={(e) => setNewSongId(e.target.value)}
                            required
                        />
                        <button type="submit">Add Song</button>
                    </form>
                    <div className="songs-container">
                        {songs.map((song) => (
                            <div key={song.song_id} className="song-card">
                                <p>{song.title}</p>
                                <button onClick={() => handleRemoveSong(song.song_id)}>Remove</button>
                            </div>
                        ))}
                    </div>
                </div>
            )}
            {message && <p className="message">{message}</p>}
        </div>
    );
};

export default Playlists;
