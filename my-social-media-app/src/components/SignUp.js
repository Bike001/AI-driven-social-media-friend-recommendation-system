import React, { useState } from 'react';
import axios from 'axios';
// import './SignUp.css';

function SignUp() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSignUp = (e) => {
    e.preventDefault(); // Prevent default form submission behavior
    axios.post('http://localhost:8000/myapp/signup/', {
      username: username,
      email: email,
      password: password
    })
    .then(response => {
      // Handle response here
      console.log(response.data);
      // Redirect the user to the login page or homepage upon successful signup
    })
    .catch(error => {
      // Handle errors here, such as displaying a message to the user
      console.error('An error occurred during sign up:', error);
      setError('An error occurred during sign up. Please try again.');
    });
  };

  return (
    <div>
      <h2>Sign Up</h2>
      {error && <p className="error">{error}</p>}
      <form onSubmit={handleSignUp}>
        <div>
          <label>Username:</label>
          <input 
            type="text" 
            value={username} 
            onChange={(e) => setUsername(e.target.value)} 
            required 
          />
        </div>
        <div>
          <label>Email:</label>
          <input 
            type="email" 
            value={email} 
            onChange={(e) => setEmail(e.target.value)} 
            required 
          />
        </div>
        <div>
          <label>Password:</label>
          <input 
            type="password" 
            value={password} 
            onChange={(e) => setPassword(e.target.value)} 
            required 
          />
        </div>
        <button type="submit">Sign Up</button>
      </form>
    </div>
  );
}

export default SignUp;
