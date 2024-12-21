import React from "react";
import { Link } from "react-router-dom";

const Sidebar = () => {
  return (
    <aside className="sidebar">
      <ul>
        <li><Link to="/">Home</Link></li>
        <li><Link to="/user">User</Link></li>
        <li><Link to="/songs">Songs</Link></li>
        <li><Link to="/artists">Artists</Link></li>
        <li><Link to="/playlists">Playlists</Link></li>
        <li><Link to="/Subscription">Subscription</Link></li> 
      </ul>
    </aside>
  );
};

export default Sidebar;
