import { useState } from 'react';
import { useMutation } from 'react-query';
import { checkSoftwareUrl } from '../services/softwareService';

import banner from '../assets/styles/Home/Banner.module.css'
import info from '../assets/styles/Home/Info.module.css'
import soft from '../assets/styles/Home/Soft.module.css'

import sobreImg from "../assets/images/home/img-Sobre.png"
import pencil from "../assets/images/home/pencil-fill 1.png"
import arrow from "../assets/images/home/send-arrow-up 1.png"
import graph from "../assets/images/home/graph-up-arrow 2.png"
import PopupSoftware from '../components/softwarePopup';

const Home = () => {
  const [showPopup, setShowPopup] = useState(false);
  const [responseData, setResponseData] = useState(null);
  const [softwareUrl, setSoftwareUrl] = useState('');

  // Mutação para enviar URL do software
  const mutationCheckUrl = useMutation(checkSoftwareUrl, {
    onSuccess: (response) => {
      console.log('Url verified sucessfully!');
      setResponseData(response.data);
    },
    onError: (error) => {
      console.error('Error verifying URL:', error);
    },
  });

  const handleSubmitUrl = (event) => {
    event.preventDefault();
    if (!softwareUrl) {
      alert("Please, insert a valide URL.");
      return;
    }
    const dataToSend = { url: softwareUrl };
    mutationCheckUrl.mutate(dataToSend);
  };


  return (
    <div className={banner.container}>
      <div id="home" className={banner.bannerSoftAi}>
        <img src={sobreImg} alt="Hero Image" className={banner.heroImage}/>
        <div className={banner.bannerContent}>
          <h1>YOUR SECURITY, OUR MISSION</h1>
          <div className={banner.description}>
            <p>Soft.AI is an innovative digital security verification tool,
              developed to identify threats in programs in a practical and efficient way.
              With an approach based on Artificial Intelligence, our technology analyzes
              responses provided by users in a form, grounded in an extensive malware database.</p>
          </div>
        </div>
      </div>

      <div id="sobre" className={info.information}>
        <h1>HOW IT WORKS?</h1>
        <div className={info.info}>
          <div className={info.form}>
            <img id="icon" src={pencil} alt=""/>
            <h2>Fill out the form</h2>
            <p>
              Answer the questions about the program<br/>
              you wish to analyze. Provide as much <br/>
              information as possible for an accurate <br/>
              analysis.</p>
          </div>

          <div className={info.respostas}>
            <img id="icon" src={arrow} alt=""/>
            <h2>Submit Answers</h2>
            <p>
              After filling out all the questions, click<br/>
              on 'Submit' so that our AI can start the <br/>
              analysis and provide you with the best security <br/>
              for your browsing.</p>
          </div>

          <div className={info.resultados}>
            <img id="icon" src={graph} alt=""/>
            <h2>Receive the Result</h2>
            <p>
              In a few seconds, you will receive <br/>
              a diagnosis informing whether the program <br/>
              is safe or if it shows signs of <br/>
              malware.</p>
          </div>
        </div>
      </div>
      <div id="formulario" className={soft.fundoSoft}>
        <div>
          <h3>Check software by data or URL</h3><br/>
          <button className={soft.saveButton} onClick={() => 
            { setShowPopup(true); }}>Create software</button>
            {showPopup && (
              <PopupSoftware
              method="create"
              onClose={() => setShowPopup(false)}
          /> )}
        {responseData && (
          <div className="card">
            <h4>Url informations</h4>
            <p><strong>Malicious:</strong> {responseData.data.malicious.toString()}</p>
            <p><strong>Suspicious:</strong> {responseData.data.suspicious.toString()}</p>
            <p><strong>Harmless:</strong> {responseData.data.harmless.toString()}</p>
            <p><strong>Undetected:</strong> {responseData.data.undetected.toString()}</p>
            <br/>
          </div>
        )}
        <form onSubmit={handleSubmitUrl}>
          <div>
            <br/>
            <label htmlFor="url">Software URL</label><br/>
            <input
              type="url"
              id="url"
              value={softwareUrl}
              onChange={(e) => setSoftwareUrl(e.target.value)}
            />
          </div><br/>
          <button className={soft.saveButton} type="submit" disabled={mutationCheckUrl.isLoading}>
            {mutationCheckUrl.isLoading ? 'Verifying...' : 'Verify'}
          </button>
          {mutationCheckUrl.isError && <p className={soft.message} style={{ color: 'red' }}>Error: {mutationCheckUrl.error.message}</p>}
          {mutationCheckUrl.isSuccess && <p className={soft.message} style={{ color: 'green' }}>Url verified sucessfully!</p>}
        </form>
        </div>
      </div>
    </div>
  );
};

export default Home;
