import { useState } from 'react';
import { useMutation } from 'react-query';
import { useParams } from 'react-router-dom';
import axios from 'axios';

const Confirm = () => {
  const { uidb64, token } = useParams();
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  const mutation = useMutation(
    async (data) => {
      const response = await axios.patch(`http://127.0.0.1:8000/api/reset-password/${uidb64}/${token}/`, data, {
        headers: {
          'Content-Type': 'application/json',
        },
      });
      return response.data;
    },
    {
      onSuccess: (data) => {
        console.log('Dados enviados com sucesso:', data);
      },
      onError: (error) => {
        console.error('Erro ao enviar os dados:', error);
      },
    }
  );

  const handleSubmit = (event) => {
    event.preventDefault();

    if (password !== confirmPassword) {
      alert('As senhas precisam ser iguais.');
      return;
    }

    mutation.mutate({ password });
  };

  return (
    <div className="content">
      <h1>Confirm password</h1>
      <form onSubmit={handleSubmit}>
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
        <div>
          <label htmlFor="confirm-password">Confirm Password</label>
          <input
            type="password"
            id="confirm-password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit" disabled={mutation.isLoading}>
          {mutation.isLoading ? 'Enviando...' : 'Enviar'}
        </button>
        {mutation.isError && <p style={{ color: 'red' }}>Erro: {mutation.error.message}</p>}
        {mutation.isSuccess && <p style={{ color: 'green' }}>Senha redefinida com sucesso!</p>}
      </form>
    </div>
  );
};

export default Confirm;
