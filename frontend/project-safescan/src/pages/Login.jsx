import { useState, useEffect } from 'react';
import { useMutation } from 'react-query';
import { useNavigate } from 'react-router-dom';
import { login } from '../services/authService';  // Importa a função de login
import Register from '../components/Register';

import style from '../assets/styles/Login.module.css'

import robo from "../assets/images/img-ia-login.png"

const Login = () => {
  const [name, setName] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();
  const [showPopup, setShowPopup] = useState(false);

  const mutation = useMutation(login, {
    onSuccess: (data) => {
      console.log('Login succesfully:', data);
      navigate('/profile');  // Redireciona o usuário para o perfil após login
    },
    onError: (error) => {
      console.error('Error sending data:', error);
    },
  });

  const handleSubmit = (event) => {
    event.preventDefault();

    const dataToSend = {
      username: name,
      password: password,
    };

    mutation.mutate(dataToSend);
  };

  useEffect(() => {
    const handleKeyPress = (event) => {
      if (event.key === "Enter" && username && password) {
        document.getElementByID('login').click();
        // Coloque a ação desejada aqui
      }
    };

    // Adiciona o listener ao montar o componente
    window.addEventListener("keydown", handleKeyPress);

    // Remove o listener ao desmontar o componente
    return () => {
      window.removeEventListener("keydown", handleKeyPress);
    };
  }, []); // O array vazio garante que o efeito seja executado apenas uma vez (no mount e unmount)

  return (
    <section className={style.banner}>
      <div className={style.left}>
        <div>
            <span className={style.linhaWhite}>Your First Line of Defense</span><br/>
            <span className={style.linhaBlack}>Against Digital Threats.</span>
        </div>
        <p>Developed with cutting-edge AI technology detecting and<br/>
            fighting malware with efficiency and precision.</p>
        <div className={style.secaoForm}>
          {mutation.isSuccess && <p style={{ color: 'green' }}>Login succesfully!</p>}
          <form className={style.formLogin} onSubmit={handleSubmit}>
            <label className={style.labelLogin} htmlFor="name">Username</label>
            <input
              className={style.inputLogin}
              type="text"
              id="name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Enter your username"
              required
            />
            <label className={style.labelLogin} htmlFor="password">Password</label>
            <input
              className={style.inputLogin}
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter your password"
              required
            />
            <div className={style.links}>
              <button type="button" onClick={() => navigate('/forgot')}>
                Forgot password?
              </button>
              <button onClick={() => {
                setShowPopup(true); 
              }}>Sign up</button>

              {showPopup && (
                <Register
                  onClose={() => setShowPopup(false)}
                />
              )}
            </div>
            <button className={style.buttonLogin} type="submit" id='login' disabled={mutation.isLoading}>
              {mutation.isLoading ? 'Signing in...' : 'Sign in'}
            </button>
            {mutation.isError && <p style={{ color: 'red' }}>Erro: {mutation.error.message}</p>}
          </form>
        </div>
      </div>
      <div className={style.right}>
          <div className={style.secaoImg}>
              <div className={style.containerImg}>
                  <img className={style.imgRobo} src={robo} alt="Desktop verde com cabeça de robô tech"/>
              </div>
          </div>
      </div>
    </section>
  );
};

export default Login;
