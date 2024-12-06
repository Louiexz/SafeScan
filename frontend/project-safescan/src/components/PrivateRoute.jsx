import { Navigate } from 'react-router-dom';

const PrivateRoute = ({ children }) => {
  const isLoggedIn = localStorage.getItem('token'); // Verifique o token no localStorage
  
  if (!isLoggedIn) {
    return <Navigate to="/login" />;  // Redireciona para login se não estiver logado
  }

  return children; // Caso contrário, renderiza os filhos
};

export default PrivateRoute;