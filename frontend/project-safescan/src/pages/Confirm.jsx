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
      const response = await axios.patch(`https://safescan.onrender.com/api/reset-password/${uidb64}/${token}/`, data, {
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
    <div className={styles.bannerConfirm}>
      <h2>
        <span className={styles.span1Confirm}>Reset Your Password And</span><br/>
        <span className={styles.span2Confirm}>Log Back In With Peace Of Mind!</span>
      </h2>
      <div className={styles.secaoConfirm}>
        <form className={styles.formConfirm} onSubmit={handleSubmit} method="POST">
          <label className={styles.labelConfirm} for="password">New password</label>

          <input
            className={styles.inputConfirm}
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Enter a new password"
            required
          />

          <label className={styles.labelConfirm} for="confirm-password">Confirm password</label>
          <input
            className={styles.inputConfirm}
            type="password"
            id="confirm-password"
            name="confirm-password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            placeholder="Confirm your password"
            required
          />

          <button className={styles.buttonConfirm} type="submit" disabled={mutation.isLoading}>
            {mutation.isLoading ? 'Sending...' : 'To send'}
          </button>
          {mutation.isError && <p style={{ color: 'red' }}>Erro: {mutation.error.message}</p>}
          {mutation.isSuccess && <p style={{ color: 'green' }}>Password recovered sucessfully!</p>}
        </form>
      </div>
    </div>
  );
};

export default Confirm;
