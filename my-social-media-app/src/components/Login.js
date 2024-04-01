import React, { useState, useContext } from 'react';
import axios from 'axios';
import UserContext from '../contexts/UserContext'; // Adjust the import path as needed
import { useNavigate } from 'react-router-dom';


const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const { setUser } = useContext(UserContext);
  

  const handleLogin = async (event) => {
    event.preventDefault();
    try {
      const response = await axios.post('http://localhost:8000/myapp/api/login/', {
        username: username,
        password: password,
      });

      // Assuming the response contains the user data and a token
      const userData = {
        ...response.data.user,
        token: response.data.token,
      };

      localStorage.setItem('user', JSON.stringify(userData)); 

      // Set user in context and localStorage
      setUser(userData);
      navigate('/');
      

      // Redirect to the homepage or desired route after login
      // This part will depend on your routing setup
    } catch (error) {
      // Handle login error
      setError('Login failed. Please check your credentials.');
      if (error.response) {
        // The request was made and the server responded with a status code
        // that falls out of the range of 2xx
        console.error('Login error response:', error.response.data);
      } else if (error.request) {
        // The request was made but no response was received
        console.error('Login error request:', error.request);
      } else {
        // Something happened in setting up the request that triggered an Error
        console.error('Login error message:', error.message);
      }
      console.error('Login error config:', error.config);
    }
  };

  return (
    <div>
      {/* Your login form */}
      <form onSubmit={handleLogin}>
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="submit">Login</button>
      </form>

      {/* Display error if there is one */}
      {error && <p>{error}</p>}
    </div>
  );
};

export default Login;
