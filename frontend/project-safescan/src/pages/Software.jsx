import { useState } from 'react';
import { useMutation, useQuery } from 'react-query';
import { listSoftwares, createSoftware, checkSoftware } from '../services/softwareService';
import '../assets/styles/index.css'
import '../assets/styles/Card.css';

const Software = () => {
  const [softwareData, setSoftwareData] = useState(null);
  const [responseData, setResponseData] = useState(null);
  const [softwareUrl, setSoftwareUrl] = useState("");
  const [softwareName, setSoftwareName] = useState("");
  const [softwareStatus, setSoftwareStatus] = useState("");

  const { isLoading, refetch } = useQuery("softwares", listSoftwares, {
    refetchOnWindowFocus: false,
    onSuccess: (response) => {
      console.log('Lista de softwares recebida com sucesso');
      setSoftwareData(response.data.data); 
    },
  });
  
  // Mutação para enviar dados do software
  const mutationCreateSoftware = useMutation(createSoftware, {
    onSuccess: (response) => {
      console.log('Software enviado com sucesso');
      setResponseData(response.data);
      refetch()
    },
    onError: (error) => {
      console.error('Erro ao enviar os dados do software:', error);
    },
  });

  // Mutação para enviar URL do software
  const mutationCheckUrl = useMutation(checkSoftware, {
    onSuccess: (response) => {
      console.log('URL verificada com sucesso');
      setResponseData(response.data);
    },
    onError: (error) => {
      console.error('Erro ao verificar a URL:', error);
    },
  });

  const handleSubmit = (event) => {
    event.preventDefault();
    const dataToSend = {};

    if (softwareName && softwareStatus) {
      dataToSend.name = softwareName;
      dataToSend.status = softwareStatus;
    }

    mutationCreateSoftware.mutate(dataToSend);
  };

  const handleSubmitUrl = (event) => {
    event.preventDefault();
    const dataToSend = {};

    if (softwareUrl) {
      dataToSend.url = softwareUrl;
    }

    mutationCheckUrl.mutate(dataToSend);
  };

  return (
    <div className='content home'>
      <h1>Softwares</h1>
      <div className='cards'>
        {isLoading ? (
          <p>Carregando...</p>
        ) : softwareData && softwareData.length > 0 ? (
          softwareData.map((software, index) => (
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
      </div>

      <h3>Check software by data or URL</h3>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="name">Software name</label>
          <input
            type="text"
            id="name"
            value={softwareName}
            onChange={(e) => setSoftwareName(e.target.value)}
          />
        </div>
        <div>
          <label htmlFor="software-status">Software status</label>
          <input
            type="text"
            id="software-status"
            value={softwareStatus}
            onChange={(e) => setSoftwareStatus(e.target.value)}
          />
        </div>
        <button type="submit" disabled={mutationCreateSoftware.isLoading}>
          {mutationCreateSoftware.isLoading ? 'Enviando...' : 'Enviar'}
        </button>
        {mutationCreateSoftware.isError && <p style={{ color: 'red' }}>Erro: {mutationCreateSoftware.error.message}</p>}
        {mutationCreateSoftware.isSuccess && <p style={{ color: 'green' }}>Software enviado com sucesso!</p>}
      </form><br/>

      {responseData && (
        <pre>
          <div className="card">
            <span>Informações da URL:</span>
            <span>Malicious: {JSON.stringify(responseData.data.malicious, null, 2)}</span>
            <span>Suspicious: {JSON.stringify(responseData.data.suspicious, null, 2)}</span>
            <span>Harmless: {JSON.stringify(responseData.data.harmless, null, 2)}</span>
            <span>Undetected: {JSON.stringify(responseData.data.undetected, null, 2)}</span>
          </div><br/>
        </pre>
      )}

      <form onSubmit={handleSubmitUrl}>
        <div>
          <label htmlFor="url">Software URL</label>
          <input
            type="url"
            id="url"
            value={softwareUrl}
            onChange={(e) => setSoftwareUrl(e.target.value)}
          />
        </div>
        <button type="submit" disabled={mutationCheckUrl.isLoading}>
          {mutationCheckUrl.isLoading ? 'Verificando...' : 'Verificar'}
        </button>
        {mutationCheckUrl.isError && <p style={{ color: 'red' }}>Erro: {mutationCheckUrl.error.message}</p>}
        {mutationCheckUrl.isSuccess && <p style={{ color: 'green' }}>URL verificada com sucesso!</p>}
      </form>
    </div>
  );
};

export default Software;
