import React, { useState } from 'react';
import { useMutation } from 'react-query';
import axios from 'axios';

const postData = async (data) => {
  const response = await axios.post('http://127.0.0.1:8000/api/forgot-password', data, {
    headers: {
      'Content-Type': 'application/json',
    },
  });

  const responseData = response.data;
  return responseData;
};

const Forgot = () => {
  const [email, setEmail] = useState('');

  const mutation = useMutation(postData, {
    onSuccess: (data) => {
      console.log('Dados enviados com sucesso:', data);
    },
    onError: (error) => {
      console.error('Erro ao enviar os dados:', error);
    },
  });

  const handleSubmit = (event) => {
    event.preventDefault();

    const dataToSend = {
      email: email,
    };

    mutation.mutate(dataToSend);
  };

  return (
    <div className='content'>
      <h1>Forgot password</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="email">Email</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <button type="submit" disabled={mutation.isLoading}>
          {mutation.isLoading ? 'Enviando...' : 'Enviar'}
        </button>
        {mutation.isError && <p style={{ color: 'red' }}>Erro: {mutation.error.message}</p>}
        {mutation.isSuccess && <p style={{ color: 'green' }}>Dados enviados com sucesso!</p>}
      </form>
    </div>
  );
};

export default Forgot;
