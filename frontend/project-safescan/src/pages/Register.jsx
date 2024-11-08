import React, { useState } from 'react';
import { useMutation } from 'react-query';

const postData = async (data) => {
  const response = await fetch('http://127.0.0.1:8000/sign-in', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    throw new Error('Falha ao enviar os dados');
  }

  return response.json();
};

const Register = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const mutation = useMutation(postData, {
    onSuccess: (data) => {
      // O que fazer em caso de sucesso (por exemplo, exibir uma mensagem)
      console.log('Dados enviados com sucesso:', data);
    },
    onError: (error) => {
      // O que fazer em caso de erro
      console.error('Erro ao enviar os dados:', error);
    },
  });

  const handleSubmit = (event) => {
    event.preventDefault();

    const dataToSend = {
      username: name,
      email: email,
      password: password
    };

    // Chama a mutação para enviar os dados
    mutation.mutate(dataToSend);
  };

  return (
    <div className='content'>
      <h1>Register</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="name">Nome</label>
          <input
            type="text"
            id="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
        </div>
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
        {mutation.isSuccess && <p style={{ color: 'green' }}>Dados enviados com sucesso!</p>}
      </form>
    </div>
  );
};

export default Register;
