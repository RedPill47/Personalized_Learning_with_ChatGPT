import React from 'react';
import './style/Header.css';
import {useContext} from 'react'
import jwt_decode from "jwt-decode"
import AuthContext from '../context/AuthContext'
import { Link } from 'react-router-dom';

const Header = () => {
    const {user, logoutUser} = useContext(AuthContext)
    const token = localStorage.getItem("authTokens")
  
    if (token){
      const decoded = jwt_decode(token) 
      var user_id = decoded.user_id
    }
    
    return (
        <header className="header">
            <button id="darkModeToggle" className="dark-mode-toggle">🌙</button>
            <div className="profile-container">
                <a id="profileLink" className="profile-icon">👤</a>
                <div id="profileDropdown" className="dropdown-content">
                    <p>My Account</p>
                    <Link to="Account">Account</Link>
                    {token !== null &&
                    <a className="nav-link" onClick={logoutUser} style={{cursor:"pointer"}}> <i className='fas fa-sign-out-alt'></i>Logout</a>
                    }
                </div>
            </div>
        </header>
    );
}

export default Header;