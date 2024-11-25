import './assets/styles/App.css';
import './assets/styles/Header.css';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Home from './pages/Home';
import Software from "./pages/Software1";
import About from './pages/About';
import Login from './pages/Login';
import Register from './pages/Register';
import Profile from './pages/Profile';
import Forgot from './pages/Forgot';
import Confirm from './pages/Confirm';
import PrivateRoute from './components/PrivateRoute';  // Importe o PrivateRoute

const App = () => {
  return (
    <Router>
      <div>
        <nav>
          <Link to="/">Home</Link>
          <Link to="/Software">Software</Link>
          <Link to="/login">Login</Link>
          <Link to="/register">Register</Link>
          <Link to="/profile">Profile</Link>
          <Link to="/about">About</Link>
        </nav>

        <div id="app">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/software" element={<Software />} />
            <Route path="/about" element={<About />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/forgot" element={<Forgot />} />
            <Route path="/confirm/:uidb64/:token" element={<Confirm />} />
            {/* Proteger a rota do perfil */}
            <Route path="/profile" element={<PrivateRoute><Profile /></PrivateRoute>} />
          </Routes>
        </div>
      </div>
    </Router>
  );
};

export default App;
