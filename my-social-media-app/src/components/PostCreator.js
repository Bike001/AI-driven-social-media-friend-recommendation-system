import React, { useState, useContext } from 'react';
import UserContext from '../contexts/UserContext'; // Adjust the import path as needed
import './PostCreator.css'; // Create PostCreator.css for styling

// PostCreator.js
function PostCreator({ fetchPosts }) {
  const [postContent, setPostContent] = useState('');
  const { user } = useContext(UserContext); // Use UserContext to access the user's token

  const handlePostChange = (event) => {
    setPostContent(event.target.value);
  };

  const handlePostSubmit = () => {
    if (user && user.token) {
      fetch('http://localhost:8000/myapp/api/posts/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Token ${user.token}`, // Include the token in the Authorization header
        },
        body: JSON.stringify({ content: postContent }),
      })
      .then(response => {
        if (response.ok) {
          return response.json();
        }
        throw new Error('Network response was not ok.');
      })
      .then(data => {
        console.log('Post created:', data);
        setPostContent(''); // Clear the input after successful post creation
        fetchPosts(); // Call the function passed as a prop to refresh the post list
      })
      .catch((error) => {
        console.error('Error:', error);
      });
    } else {
      console.error('User token is not available.');
    }
  };

  return (
    <div className="post-creator">
      <textarea
        value={postContent}
        onChange={handlePostChange}
        placeholder="What's on your mind?"
      />
      <button onClick={handlePostSubmit}>Post</button>
    </div>
  );
}

export default PostCreator;

