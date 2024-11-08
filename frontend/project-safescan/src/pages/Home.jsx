import React, { useEffect, useState } from 'react';
import { useMutation } from 'react-query';
import '../assets/styles/Card.css';

const postData = async (data) => {
  const response = await fetch('http://127.0.0.1:8000/', {
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

const Home = () => {
  const [data, setData] = useState(null);
  const [responseData, setResponseData] = useState(null);
  const [softwareUrl, setSoftwareUrl] = useState("");
  const [softwareName, setSoftwareName] = useState("");
  const [softwareStatus, setSoftwareStatus] = useState("");

  const mutation = useMutation(postData, {
    onSuccess: (data) => {
      setResponseData(data)
      console.log('Dados enviados com sucesso:', data);
    },
    onError: (error) => {
      console.error('Erro ao enviar os dados:', error);
    },
  });

  const handleSubmit = (event) => {
    event.preventDefault();
    const dataToSend = {};

    if (softwareUrl) {
      dataToSend.url = softwareUrl;
    }
    else if (softwareName && softwareStatus) { 
      dataToSend.name = softwareName;
      dataToSend.status = softwareStatus;
    }

    mutation.mutate(dataToSend);
  };

  useEffect(() => {
    fetch('http://127.0.0.1:8000/')
      .then(response => response.json())
      .then(data => {
        setData(data);
      })
      .catch(error => {
        console.error('Erro ao fazer a requisição:', error);
      });
  }, []);

  return (
    <div className='content home'>
      <h1>Home Page</h1>
      <p>Bem-vindo ao SafeScan!</p>
      <p>Aqui você pode visualizar os softwares existentes e verificar novos!</p>
      <div className='cards'>
        {data ? (
          <pre>
            {data.data && data.data.length > 0 ? (
              data.data.map((software, index) => (
                <div className="card" key={index}>
                  <span>Name: {software.name}</span><br />
                  <span>Status: {software.status}</span><br />
                  <span>Created at: {software.created_at}</span><br />
                  <span>Updated at: {software.updated_at}</span>
                </div>
              ))
            ) : (
              <span>Nenhum software cadastrado ainda.</span>
            )}
          </pre>
        ) : (
          <p>Carregando...</p>
        )}
      </div>
      
      <h3>Check software por nome, status ou url</h3>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="name">Nome do software</label>
          <input
            type="text"
            id="name"
            value={softwareName}
            onChange={(e) => setSoftwareName(e.target.value)}
          />
        </div>
        <div>
          <label htmlFor="software-status">Status do software</label>
          <input
            type="text"
            id="software-status"
            value={softwareStatus}
            onChange={(e) => setSoftwareStatus(e.target.value)}
          />
        </div>
      </form>
      {responseData ? (
        <pre>
          <div className="card">
            <span>
              Informações da URL:
            </span>
            <span>Malicious: {JSON.stringify(responseData.data.malicious, null, 2)}</span>
            <span>Suspicious: {JSON.stringify(responseData.data.suspicious, null, 2)}</span>
            <span>Harmless: {JSON.stringify(responseData.data.harmless, null, 2)}</span>
            <span>Undetected: {JSON.stringify(responseData.data.undetected, null, 2)}</span>
          </div>
        </pre>
      ) : (
        <span>URL não encontrado.</span>
      )}
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="url">Url do software</label>
          <input
            type="url"
            id="url"
            value={softwareUrl}
            onChange={(e) => setSoftwareUrl(e.target.value)}
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

export default Home;
