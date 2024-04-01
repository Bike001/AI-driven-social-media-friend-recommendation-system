import React, { useState, useEffect, useContext } from 'react';
import axios from 'axios';
import Post from './Post'; // Make sure this path is correct
import UserContext from '../contexts/UserContext';
import './OwnProfilePage.css';

function OwnProfilePage() {
  const [userPosts, setUserPosts] = useState([]);
  const [profile, setProfile] = useState(null);
  const { user } = useContext(UserContext);

  useEffect(() => {
    if (user) {
      // Fetch the profile information of the logged-in user
      axios.get(`http://localhost:8000/myapp/api/ownprofile`, {
        headers: { Authorization: `Token ${user.token}` }
      })
      .then(response => {
        setProfile(response.data);
      })
      .catch(error => {
        console.error('Error fetching profile info:', error);
      });

      // Fetch the posts of the logged-in user
      axios.get(`http://localhost:8000/myapp/api/ownposts`, {
        headers: { Authorization: `Token ${user.token}` }
      })
      .then(response => {
        setUserPosts(response.data);
      })
      .catch(error => {
        console.error('Error fetching user posts:', error);
      });
    }
  }, [user]);

  if (!user) {
    return <p>Please log in to view this page.</p>;
  }

  return (
    <div className="profile-page">
      <h1>{profile?.username || 'Your'} Profile</h1>
      <div className="user-posts">
        {userPosts.length > 0 ? (
          userPosts.map((post) => <Post key={post.id} {...post} />)
        ) : (
          <p>You haven't posted anything yet.</p>
        )}
      </div>
    </div>
  );
}

export default OwnProfilePage;
