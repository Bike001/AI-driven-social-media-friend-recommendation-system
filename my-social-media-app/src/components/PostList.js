import React, { useEffect, useState, useContext } from 'react';
import axios from 'axios';
import Post from './Post'; // Import the Post component
import UserContext from '../contexts/UserContext'; // Adjust the path as necessary

function PostList() {
  const [posts, setPosts] = useState([]);
  const { user } = useContext(UserContext); // Use the UserContext to access the logged-in user's info

  useEffect(() => {
    const fetchUserPosts = async () => {
      if (user && user.token) {
        try {
          const response = await axios.get('http://localhost:8000/myapp/api/posts/', {
            headers: { Authorization: `Token ${user.token}` } // Use the token from the UserContext
          });
          setPosts(response.data); // Set the posts returned from the backend
        } catch (error) {
          console.error("Failed to fetch user's posts:", error);
        }
      }
    };

    fetchUserPosts();
  }, [user]); // Depend on user to refetch when the user changes (login/logout)

  return (
    <div>
      {posts.map((post) => (
        <Post key={post.id} content={post.content} username={post.username} />
      ))}
    </div>
  );
}

export default PostList;

