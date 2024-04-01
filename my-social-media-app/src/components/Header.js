import { Link } from 'react-router-dom';
import './Header.css';

function Header() {
  return (
    <header className="header">
      <Link to="/" className="logo">
        <img src="/logo.png" alt="Logo" className="logo-img" />
      </Link>
      <input type="text" placeholder="Search Here" />
      <nav>
        <Link to="/" className="nav-link">
          <img src="/Homepage.png" alt="Homepage" className="nav-img home-img" />
        </Link>
        <Link to="/friends" className="nav-link">
          <img src="/friends.png" alt="Friends" className="nav-img friends-img" />
        </Link>
        <Link to="/messages" className="nav-link">
          <img src="/message.png" alt="Messages" className="nav-img messages-img" />
        </Link>
        <Link to="/profile" className="nav-link">
          <img src="/profile.png" alt="Profile" className="nav-img profile-img" />
        </Link>
      </nav>
    </header>
  );
}

export default Header;
