import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Home from '../pages/Home';
import Login from '../pages/Login';
import Profile from '../pages/Profile';
import Forgot from '../pages/Forgot';
import Confirm from '../pages/Confirm';
import PrivateRoute from './PrivateRoute';  // Importe o PrivateRoute

import '../index.css'

const Navigation = () => {
    return (
        <Router>
            <div>
                <nav className='navbar'>
                {window.location.pathname.includes('confirm') ? null : (
                    <>
                        <Link to="/">Home</Link>
                        {!localStorage.getItem('token') ? <Link to="/login">Login</Link> : null}
                        {window.location.pathname === '/' && (
                            <>
                                <a href="#sobre">About</a>
                                <a href="#formulario">Form</a>
                            </>
                        )}
                        <Link to="/profile">Profile</Link>
                    </>
                )}
                </nav>

                <div className="app">
                    <Routes>
                        <Route path="/" element={<Home />} />
                        <Route path="/login" element={<Login />} />
                        <Route path="/forgot" element={<Forgot />} />
                        <Route path="/confirm/:uidb64/:token" element={<Confirm />} />
                        {/* Proteger a rota do perfil */}
                        <Route path="/profile" element={<PrivateRoute><Profile /></PrivateRoute>} />
                    </Routes>
                </div>
            </div>
        </Router>
    )
}

export default Navigation