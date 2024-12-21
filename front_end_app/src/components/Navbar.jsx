import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "./Navbar.css";

const Navbar = () => {
  const [query, setQuery] = useState("");
  const navigate = useNavigate();

  const handleSearch = (e) => {
    e.preventDefault();
    if (query.trim()) {
      navigate(`/search?q=${query}`);
    }
  };

  return (
    <nav className="navbar">
      <div className="logo" onClick={() => navigate("/")}>MusicDB</div>
      <form className="search-bar" onSubmit={handleSearch}>
        <input
          type="text"
          placeholder="Search for music..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button type="submit">Search</button>
      </form>
      <div className="user-profile">
        <Link to="/login">
          <button className="nav-btn">Sign In</button>
        </Link>
        <Link to="/register">
          <button className="nav-btn">Register</button>
        </Link>
      </div>
    </nav>
  );
};

export default Navbar;