import React from "react";
import "./Home.css";
import heroVideo from "./assets/hero-video.mp4";  // Ensure you have this video in your assets folder
import { FaSearch, FaMicrophone } from 'react-icons/fa';

function Home() {
  return (
    <div className="hero-container">
      <video className="hero-video" src={heroVideo} autoPlay loop muted />
      <div className="hero-overlay">
        <div className="hero-content">
        <div className="headline-container">
            <div className="headline">Start saving smartly with Bank of Baroda's Trial Account</div>
          </div>
          <h1>Namaste!</h1>
          
          <p>Welcome to Bank of Baroda</p>
          <h2>Thank you for contacting Bank of Baroda. How can I assist you today?</h2>
          <div className="search-box">
            <FaSearch className="search-icon" />
            <input type="text" className="search-bar" placeholder="" />
            <FaMicrophone className="mic-icon" />
          </div>
        </div>
      </div>
    </div>
  );
}

export default Home;
