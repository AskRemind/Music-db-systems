import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Sidebar from "./components/Sidebar";
import Home from "./pages/Home";
import User from "./pages/User";
import Songs from "./pages/Songs";
import Artists from "./pages/Artists";
import Playlists from "./pages/Playlists";
import Login from "./pages/Login";
import Register from "./pages/Register";
import ResetPassword from "./pages/ResetPassword";
import Subscription from "./pages/Subscription"
import SearchResults from "./pages/SearchResults";
import SongDetail from "./pages/SongDetail"

function App() {
  return (
    <Router>
      <div className="app">
        <Navbar />
        <div className="main">
          <Sidebar />
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/user" element={<User />} />
            <Route path="/songs" element={<Songs />} />
            <Route path="/artists" element={<Artists />} />
            <Route path="/playlists" element={<Playlists />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/reset-password" element={<ResetPassword />} />
            <Route path="/Subscription" element={<Subscription />} />
            <Route path="/search" element={<SearchResults />} />
            <Route path="/ratings/song/:songId" element={<SongDetail />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;

