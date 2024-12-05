import React, { useState } from 'react';
import { useMutation } from 'react-query';
import axios from 'axios';

import recover from '../assets/styles/recoverPassword.module.css'
import robo from '../assets/images/img-robo-recover.png'

const postData = async (data) => {
  const response = await axios.post('https://safescan.onrender.com/api/forgot-password', data, {
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
    <div className={recover.bannerRecover}>
      <div>
        <h2>
            <span>Recover Your<br/>Account Safely</span>
        </h2>
        <div className={recover.secaoRecover}>
          <form className={recover.formRecover} onSubmit={handleSubmit}>
            <div>
              <label
                className={recover.labelRecover}
                htmlFor="email">Registered email</label><br/>
              <input
                className={recover.inputRecover}
                type="email"
                id="email"
                name="email"
                placeholder="Enter your registered email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
            <button className={recover.buttonRecover} type="submit" disabled={mutation.isLoading}>
              {mutation.isLoading ? 'Sending...' : 'To send'}
            </button>
            {mutation.isError && <p style={{ color: 'red' }}>Erro: {mutation.error.message}</p>}
            {mutation.isSuccess && <p style={{ color: 'green' }}>Dados enviados com sucesso!</p>}

          </form>
          <p className={recover.infoParagraph}>
            We will send you an email with a link to reset your password. Check your inbox and follow the instructions!
          </p>
          <div className={recover.sectionImgRecover}>
            <div className={recover.containerImgRecover}>
              <img src={robo} alt="Desktop verde tech"/>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Forgot;
