import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import axios from 'axios';

import Header from './components/Header';
import PostCreator from './components/PostCreator';
import PostList from './components/PostList';
import FriendsPage from './components/FriendsPage';
import MessagesPage from './components/MessagesPage';
import ProfilePage from './components/ProfilePage';
import SignUp from './components/SignUp';
import Login from './components/Login';
import OwnProfilePage from './components/OwnProfilePage';
import { UserProvider } from './contexts/UserContext'; // Make sure this is correctly imported

import './App.css';

function App() {
  const [posts, setPosts] = useState([]);

  // Function to fetch posts
  const fetchPosts = () => {
    const user = JSON.parse(localStorage.getItem('user')); // Retrieve the user from localStorage
  
    // Only proceed if we have a user and token
    if (user && user.token) {
      axios.get('/api/posts/', {
        headers: {
          Authorization: `Token ${user.token}`
        }
      })
      .then(response => {
        setPosts(response.data);
      })
      .catch(error => {
        console.error('There was an error fetching the posts', error);
      });
    }
  };

  // Fetch posts on component mount
  useEffect(() => {
    fetchPosts();
  }, []);

  return (
    <UserProvider> {/* Correctly wrap the Router with UserProvider */}
      <Router>
        <div className="App">
          <Header />
          <Routes>
            
            <Route path="/messages" element={<MessagesPage />} />
            <Route path="/friends" element={<FriendsPage />} />
            <Route path="/signup" element={<SignUp />} />
            <Route path="/login" element={<Login />} />
            <Route path="/profile/:username" element={<ProfilePage />} />
            <Route path="/profile" element={<OwnProfilePage />} />
            

            <Route path="/" element={
              <>
                <PostCreator fetchPosts={fetchPosts} />
                <PostList posts={posts} />
              </>
            } />
          </Routes>
        </div>
      </Router>
    </UserProvider>
  );
}

export default App;
