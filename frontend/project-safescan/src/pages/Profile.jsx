import React, { useEffect, useState } from 'react';

const Profile = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/profile', {
      method: 'GET',
      credentials: 'include', // Envia o cookie de sessão
    })
      .then(response => {
        if (response.ok) {
          return response.json();
        }
        throw new Error("Usuário não autenticado");
      })
      .then(data => {
        setData(data);
      })
      .catch(error => {
        console.error('Erro ao buscar perfil:', error);
      });
  }, []);

  if (!data) {
    return <div className='content'><p>Usuário precisa estar logado.</p></div>;
  }
  
  return (
    <div className='content'>
      <h1>Profile</h1>
      <h4>Bem-vindo à página de perfil!</h4>
      <p>Aqui você pode editar seu perfil e atualizar ou deletar seus softwares.</p>
      {data.data ? (
        <pre>
          <span>Username: {data.data.username}</span><br />
          <span>Email: {data.data.email}</span><br />
          <span>Password: {data.data.password}</span>
        </pre>
      ) : (
        <p>Usuário precisa estar logado.</p>
      )}
    </div>
  );
};

export default Profile;
