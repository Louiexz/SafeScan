import { useState } from 'react';
import { useMutation, useQuery } from 'react-query';
import { listSoftwares, createSoftware, checkSoftware } from '../services/softwareService';
import Radio from '../components/inputRadio';
import '../assets/styles/index.css'
import '../assets/styles/Card.css';

const Software = () => {
  const [softwareData, setSoftwareData] = useState(null);
  const [responseData, setResponseData] = useState(null);
  const [softwareUrl, setSoftwareUrl] = useState("");
  const [softwareName, setSoftwareName] = useState("");
  const [softwareLocalizacaoRede, setSoftwareLocalizacaoRede] = useState(0);
  const [softwareBluetoothFunc, setSoftwareBluetoothFunc] = useState(0);
  const [softwareArquivosConfOS, setSoftwareArquivosConfOS] = useState(0);
  const [softwareSms, setSoftwareSms] = useState(0);
  const [softwareMidiaAudio, setSoftwareMidiaAudio] = useState(0);
  const [softwareCamera, setSoftwareCamera] = useState(0);
  const [softwareRedeOperadora, setSoftwareRedeOperadora] = useState(0);
  const [softwareSimPais, setSoftwareSimPais] = useState(0);
  const [softwareBibliotecaClasses, setSoftwareBibliotecaClasses] = useState(0);
  const [softwarePacotes, setSoftwarePacotes] = useState(0);

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

    if (softwareName !== "" && softwareLocalizacaoRede !== null && softwareBluetoothFunc !== null &&
      softwareArquivosConfOS !== null && softwareSms !== null && softwareMidiaAudio !== null &&
      softwareCamera !== null && softwareRedeOperadora !== null && softwareSimPais !== null &&
      softwareBibliotecaClasses !== null && softwarePacotes !== null)
    {
      dataToSend.name = softwareName;
      dataToSend.localizacao_rede = softwareLocalizacaoRede;
      dataToSend.bluetooth_funcionalidades = softwareBluetoothFunc;
      dataToSend.arquivos_confOS = softwareArquivosConfOS;
      dataToSend.sms = softwareSms;
      dataToSend.midia_audio = softwareMidiaAudio;
      dataToSend.camera = softwareCamera;
      dataToSend.rede_operadora = softwareRedeOperadora;
      dataToSend.sim_pais = softwareSimPais;
      dataToSend.biblioteca_class = softwareBibliotecaClasses;
      dataToSend.pacotes = softwarePacotes
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
        <Radio
          pergunta="Software localização-rede"
          nome="localizacao-rede"
          value={softwareLocalizacaoRede}
          onchange={setSoftwareLocalizacaoRede}
        />
        <Radio
          pergunta="Software bluetooth-func"
          nome="bluetooth-func"
          value={softwareBluetoothFunc}
          onchange={setSoftwareBluetoothFunc}
        />
        <Radio
          pergunta="Software arquivos-confOS"
          nome="arquivos-confOS"
          value={softwareArquivosConfOS}
          onchange={setSoftwareArquivosConfOS}
        />
        <Radio
          pergunta="Software sms"
          nome="sms"
          value={softwareSms}
          onchange={setSoftwareSms}
        />
        <Radio
          pergunta="Software midia-audio"
          nome="midia-audio"
          value={softwareMidiaAudio}
          onchange={setSoftwareMidiaAudio}
        />
        <Radio
          pergunta="Software camera"
          nome="camera"
          value={softwareCamera}
          onchange={setSoftwareCamera}
        />
        <Radio
          pergunta="Software rede-operadora"
          nome="rede-operadora"
          value={softwareRedeOperadora}
          onchange={setSoftwareRedeOperadora}
        />
        <Radio
          pergunta="Software sim-pais"
          nome="sim-pais"
          value={softwareSimPais}
          onchange={setSoftwareSimPais}
        />
        <Radio
          pergunta="Software biblioteca-class"
          nome="biblioteca-class"
          value={softwareBibliotecaClasses}
          onchange={setSoftwareBibliotecaClasses}
        />
        <Radio
          pergunta="Software pacotes"
          nome="pacotes"
          value={softwarePacotes}
          onchange={setSoftwarePacotes}
        />
        
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
