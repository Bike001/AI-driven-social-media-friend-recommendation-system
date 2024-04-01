import React, { useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import UserContext from '../contexts/UserContext'; // Adjust the import path as needed

const Logout = () => {
  const { logoutUser } = useContext(UserContext);
  const navigate = useNavigate();

  const handleLogout = () => {
    logoutUser(); // Clears the user state and removes user from localStorage
    navigate('/login'); // Redirect to login page after logout
  };

  return (
    <button onClick={handleLogout}>Logout</button>
  );
};

export default Logout;
