import { useState } from 'react';
import { useMutation } from 'react-query';
import { useParams } from 'react-router-dom';
import axios from 'axios';

import styles from '../assets/styles/ConfirmPassword.module.css';

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
    <div class="banner-confirm">
      <h2>
        <span class="span1-confirm">Reset Your Password And</span><br/>
        <span class="span2-confirm">Log Back In With Peace Of Mind!</span>
      </h2>
      <div class="secao-confirm">
        <form class="form-confirm" onSubmit={handleSubmit} method="POST">
          <label class="label-confirm" for="password">New password</label>

          <input
            class="input-confirm"
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Enter a new password"
            required
          />

          <label class="label-confirm" for="confirm-password">Confirm password</label>
          <input
            class="input-confirm"
            type="password"
            id="confirm-password"
            name="confirm-password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            placeholder="Confirm your password"
            required
          />

          <button type="submit" disabled={mutation.isLoading}>
            {mutation.isLoading ? 'Sending...' : 'To send'}
          </button>
          {mutation.isError && <p style={{ color: 'red' }}>Erro: {mutation.error.message}</p>}
          {mutation.isSuccess && <p style={{ color: 'green' }}>Senha redefinida com sucesso!</p>}
        </form>
      </div>
    </div>
  );
};

export default Confirm;
