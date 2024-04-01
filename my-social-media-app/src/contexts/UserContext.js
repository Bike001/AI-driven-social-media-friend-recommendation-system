import React, { createContext, useState, useEffect } from 'react';

const UserContext = createContext({
  user: null,
  setUser: () => {},
  logoutUser: () => {},
  isLoading: true // Add this line to track the loading state
});

export const UserProvider = ({ children }) => {
  const [user, setUser] = useState(JSON.parse(localStorage.getItem('user')) || null);

  useEffect(() => {
    // Update localStorage when the user state changes
    console.log("User state updated:", user); // Log the current user state
    localStorage.setItem('user', JSON.stringify(user));
  }, [user]);

  const logoutUser = () => {
    localStorage.removeItem('user');
    setUser(null);
  };

  return (
    <UserContext.Provider value={{ user, setUser, logoutUser }}>
      {children}
    </UserContext.Provider>
  );
};

export default UserContext;

