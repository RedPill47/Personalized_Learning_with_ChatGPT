import {useContext} from 'react'
import jwt_decode from "jwt-decode"
import AuthContext from '../context/AuthContext'
import { Link } from 'react-router-dom'
import './style/Sidebar.css'

function Sidebar() {
    const {user, logoutUser} = useContext(AuthContext)
    const token = localStorage.getItem("authTokens")
  
    if (token){
      const decoded = jwt_decode(token) 
      var user_id = decoded.user_id
    }

  return (
    <div className="sidebar">
      <h1>Tutor AI</h1>
      <ul>
        <li><Link to="/create">Create</Link></li>
        <li><Link to="/quiz">Quiz</Link></li>
        <li><Link to="/flashcardspage">Flashcards</Link></li>
      </ul>

      
    </div>
  );
}

export default Sidebar;