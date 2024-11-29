import { useState } from 'react';
import { useMutation } from 'react-query';
import { useNavigate } from 'react-router-dom';
import { login } from '../services/authService';  // Importa a função de login
import '../assets/styles/Card.css'

const Login = () => {
  const [name, setName] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const mutation = useMutation(login, {
    onSuccess: (data) => {
      console.log('Login bem-sucedido:', data);
      navigate('/profile');  // Redireciona o usuário para o perfil após login
      window.location.reload()
    },
    onError: (error) => {
      console.error('Erro ao enviar os dados:', error);
    },
  });

  const handleSubmit = (event) => {
    event.preventDefault();

    const dataToSend = {
      username: name,
      password: password,
    };

    mutation.mutate(dataToSend);
  };

  return (
    <div className='content'>
      <h1>Login</h1>

      {mutation.isSuccess && <p style={{ color: 'green' }}>Login bem-sucedido!</p>}
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="name">Username</label>
          <input
            type="text"
            id="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
        </div>
        <div>
          <label htmlFor="password">Password</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit" disabled={mutation.isLoading}>
          {mutation.isLoading ? 'Enviando...' : 'Enviar'}
        </button>
        {mutation.isError && <p style={{ color: 'red' }}>Erro: {mutation.error.message}</p>}
      </form>
      <button type="button" onClick={() => navigate('/forgot')}>
        Forgot password
      </button>
    </div>
  );
};

export default Login;
