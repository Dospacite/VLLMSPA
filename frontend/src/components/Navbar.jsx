// Navbar.jsx
import React, { Component } from 'react';
import './Navbar.css';

class Navbar extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isAuthenticated: false, // Change this dynamically based on actual auth state
    };
  }

  toggleAuth = () => {
    this.setState((prevState) => ({
      isAuthenticated: !prevState.isAuthenticated,
    }));
  };

  render() {
    const { isAuthenticated } = this.state;

    return (
      <nav className="navbar">
         <a href="/" className="navbar-logo">Trickster</a>
        <ul className="navbar-links">
          <li><a href="/">Home</a></li>
          <li><a href="/explore">Explore</a></li>
          <li><a href="/profile">Profile</a></li>
          <li><a href="/ai-chat">AI-Chat</a></li>
          <li>
            <button className="auth-button" onClick={this.toggleAuth}>
              {isAuthenticated ? 'Logout' : 'Login'}
            </button>
          </li>
        </ul>
      </nav>
    );
  }
}

export default Navbar;
