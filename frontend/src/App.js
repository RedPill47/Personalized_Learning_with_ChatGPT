import React from 'react'

import {BrowserRouter as Router, Route, Switch} from "react-router-dom"
import PrivateRoute from "./utils/PrivateRoute"
import { AuthProvider } from './context/AuthContext'

import Homepage from './views/Homepage'
import Registerpage from './views/Registerpage'
import Loginpage from './views/Loginpage'
import Quiz from './views/Quiz';

import Header from './views/Header';
import Sidebar from './views/Sidebar';
import Create from './views/Create';

import Layout from './views/Layout'


import FlashcardsPage from './views/FlashcardsPage'
import Chatbot from './views/Chatbot'
import Account from './views/Account';

import './views/style/Quiz.css';
import './views/style/Flashcards.css';
import './views/style/Chatbot.css';
import './views/style/Account.css';
import './views/style/Header.css';
import './views/style/Sidebar.css';
import './views/style/HomePage.css';
import './views/style/Layout.css';
import './views/style/FlashcardsPage.css';
import './views/style/Auth.css';
import './views/style/Base.css';
import './views/style/Styles.css';



function App() {
  return (
    <Router>
      <AuthProvider>
        <Switch>
          <Route path="/" exact>
            <Homepage />
          </Route>
          <Route path="/login">
            <Loginpage />
          </Route>
          <Route path="/register" exact>
            <Registerpage />
          </Route>
          <Route path="/sidebar" exact>
            <Layout>
              <Sidebar />
            </Layout>
          </Route>
          <Route path="/header" exact>
            <Layout>
              <Header />
            </Layout>
          </Route>
          <PrivateRoute path="/create" exact>
            <Layout>
              <Create />
            </Layout>
          </PrivateRoute>
          <PrivateRoute path="/quiz" exact>
            <Layout>
              <Quiz />
            </Layout>
          </PrivateRoute>
          <PrivateRoute path="/flashcardspage" exact>
            <Layout>
              <FlashcardsPage />
            </Layout>
          </PrivateRoute>
          <PrivateRoute path="/chatbot" exact>
            <Layout>
              <Chatbot />
            </Layout>
          </PrivateRoute>
          <PrivateRoute path="/account" exact>
            <Layout>
              <Account />
            </Layout>
          </PrivateRoute>
        </Switch>
      </AuthProvider>
    </Router>
  );
}

export default App;