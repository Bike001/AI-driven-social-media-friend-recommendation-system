// Post.js
import React from 'react';
import './Post.css'; // Make sure the path to your CSS file is correct

function Post({ username, content }) {
  return (
    <div className="post">
      <div className="post-header">
        <div className="post-user">{username}</div>
        {/* ... other header content ... */}
      </div>
      <div className="post-content">{content}</div>
      <div className="post-actions">
        {/* Add icons for liking, commenting, etc. here */}
        <span className="post-like" style={{ backgroundImage: `url(${process.env.PUBLIC_URL}/comment-icon.png)` }}></span>
        <span className="post-comment" style={{ backgroundImage: `url(${process.env.PUBLIC_URL}/like-icon.png)` }}></span>
        {/* ... other action icons ... */}
      </div>
    </div>
  );
}

export default Post;
