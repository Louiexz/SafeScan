import { useState } from 'react';
import { useMutation, useQuery } from 'react-query';
import { listSoftwares, checkSoftwareUrl } from '../../services/softwareService';

import PopupSoftware from '../../components/softwarePopup';

const Software = () => {
  const [softwareData, setSoftwareData] = useState(null);
  const [responseData, setResponseData] = useState(null);
  const [softwareUrl, setSoftwareUrl] = useState("");
  const [showPopup, setShowPopup] = useState(false);

  const { isLoading, refetch } = useQuery("softwares", listSoftwares, {
    refetchOnWindowFocus: false,
    onSuccess: (response) => {
      console.log('Lista de softwares recebida com sucesso');
      setSoftwareData(response.data.data); 
    },
  });

  // Mutação para enviar URL do software
  const mutationCheckUrl = useMutation(checkSoftwareUrl, {
    onSuccess: (response) => {
      console.log('URL verificada com sucesso');
      setResponseData(response.data);
    },
    onError: (error) => {
      console.error('Erro ao verificar a URL:', error);
    },
  });

  const handleSubmitUrl = (event) => {
    event.preventDefault();
    if (!softwareUrl) {
      alert("Por favor, insira uma URL válida.");
      return;
    }
    const dataToSend = { url: softwareUrl };
    mutationCheckUrl.mutate(dataToSend);
  };

  return (
    <div className='content home'>
      <h1>Softwares</h1>
      <div className='cards'>
        {isLoading ? (
            <div className="spinner">Carregando...</div>
          ) : softwareData && softwareData.length > 0 ? (
            softwareData.map((software, index) => (
              <div className="card" key={index}>
                <span>Name: {software.name}</span><br />
                <span>Status: {software.label}</span><br />
                <span>Created at: {software.created_at}</span><br />
                <span>Updated at: {software.updated_at}</span>
              </div>
            ))
          ) : (
            <span>Nenhum software cadastrado ainda.</span>
        )}
      </div>

      <h3>Check software by data or URL</h3>
      <button onClick={() => {
        setShowPopup(true); 
      }}>Create software</button>

      {showPopup && (
        <PopupSoftware 
          method="create" 
          onClose={() => setShowPopup(false)}
          refetch={refetch}
        />
      )}

      {responseData && (
        <div className="card">
          <h4>Informações da URL</h4>
          <p><strong>Malicious:</strong> {responseData.data.malicious.toString()}</p>
          <p><strong>Suspicious:</strong> {responseData.data.suspicious.toString()}</p>
          <p><strong>Harmless:</strong> {responseData.data.harmless.toString()}</p>
          <p><strong>Undetected:</strong> {responseData.data.undetected.toString()}</p>
        </div>
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
