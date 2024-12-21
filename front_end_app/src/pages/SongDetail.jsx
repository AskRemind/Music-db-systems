import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom"; 
import './SongDetail.css';

const SongDetail = () => {
  const { songId } = useParams(); // 获取URL中的songId参数
  const [songInfo, setSongInfo] = useState({});
  const [comments, setComments] = useState([]);
  const [newRating, setNewRating] = useState(0);
  const [newComment, setNewComment] = useState("");
  const [message, setMessage] = useState("");
  const userId = JSON.parse(localStorage.getItem("user_info"))?.UserID; // 假设用户信息存储在localStorage

  useEffect(() => {
    if (!songId) {
      setMessage("Song ID is missing!");
      return;
    }

    if (!userId) {
      setMessage("Please log in.");
      return;
    }

    // 获取歌曲的详细信息（评分和评论）
    fetch(`http://localhost:5000/ratings/song/${songId}`)
      .then((res) => {
        if (!res.ok) {
          throw new Error(`HTTP error! status: ${res.status}`);
        }
        return res.json();
      })
      .then((data) => {
        setSongInfo({
          title: data.title || "Unknown Song",
          genre: data.genre || "Unknown Genre",
          average_rating: data.average_rating || 0,
          rating_count: data.rating_count || 0,
        });
        setComments(data.comments || []);
      })
      .catch((error) => {
        console.error("Error fetching song details:", error);
        setMessage("Error fetching song details. Please try again later.");
      });
  }, [songId, userId]);

  const handleSubmitRating = async (e) => {
    e.preventDefault();

    if (newRating < 1 || newRating > 5) {
      setMessage("Rating must be between 1 and 5.");
      return;
    }

    if (!userId) {
      setMessage("Please log in to rate songs.");
      return;
    }

    try {
      const response = await fetch(`http://localhost:5000/ratings/${songId}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "UserID": userId,
        },
        body: JSON.stringify({ user_id: userId, rating: newRating }),
      });
      if (!response.ok) {
        throw new Error(`Error: ${response.status}`);
      }

      const data = await response.json();
      setMessage("Rating submitted!");
      setNewRating(0); // Reset rating input

      // Refresh song details after rating submission
      fetch(`http://localhost:5000/ratings/song/${songId}`)
        .then((res) => res.json())
        .then((data) => {
          setSongInfo({
            title: data.title,
            genre: data.genre,
            average_rating: data.average_rating,
            rating_count: data.rating_count,
          });
          setComments(data.comments);
        })
        .catch((error) => console.error("Error fetching updated details:", error));
    } catch (error) {
      console.error("Error submitting rating:", error);
      setMessage("An error occurred while submitting your rating.");
    }
  };

  const handleSubmitComment = async (e) => {
    e.preventDefault();

    if (newComment.trim().length < 3) {
      setMessage("Comment is too short.");
      return;
    }

    if (!userId) {
      setMessage("Please log in to comment.");
      return;
    }

    try {
      const response = await fetch(`http://localhost:5000/ratings/comments/${songId}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "UserID": userId,
        },
        body: JSON.stringify({ user_id: userId, comment: newComment }),
      });
      if (!response.ok) {
        throw new Error(`Error: ${response.status}`);
      }

      const data = await response.json();
      setMessage("Comment added!");
      setComments((prev) => [data.comment, ...prev]); // Prepend new comment
      setNewComment(""); // Clear the comment input field
    } catch (error) {
      console.error("Error submitting comment:", error);
      setMessage("An error occurred while submitting your comment.");
    }
  };

  return (
    <div className="song-detail-page">
      <h1>{songInfo.title || "Loading..."}</h1>
      <p>Genre: {songInfo.genre || "Unknown"}</p>
      <p>
        Average Rating: {songInfo.average_rating || "No ratings yet"} (
        {songInfo.rating_count || 0} ratings)
      </p>

      <div className="rating-section">
        <form onSubmit={handleSubmitRating}>
          <label htmlFor="rating">Rate this song (1-5):</label>
          <input
            type="number"
            id="rating"
            min="1"
            max="5"
            value={newRating}
            onChange={(e) => setNewRating(Number(e.target.value))}
            required
          />
          <button type="submit">Submit Rating</button>
        </form>
      </div>

      <div className="comment-section">
        <form onSubmit={handleSubmitComment}>
          <textarea
            placeholder="Leave a comment"
            value={newComment}
            onChange={(e) => setNewComment(e.target.value)}
            required
          ></textarea>
          <button type="submit">Submit Comment</button>
        </form>
      </div>

      <div className="comments">
        <h2>Comments</h2>
        {comments.length > 0 ? (
          comments.map((comment, index) => (
            <div key={index} className="comment-card">
              <p>{comment.comment_text}</p>
              <small>By User {comment.user_id || "Unknown"}</small>
            </div>
          ))
        ) : (
          <p>No comments yet.</p>
        )}
      </div>

      {message && <p className="message">{message}</p>}
    </div>
  );
};

export default SongDetail;
