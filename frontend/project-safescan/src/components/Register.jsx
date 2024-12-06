import { useState } from 'react';
import { useMutation } from 'react-query';
import { useNavigate } from 'react-router-dom';
import Modal from 'react-modal'; // Biblioteca para modal
import { register } from '../services/authService';  // Importe a função register

import style from '../assets/styles/PopupRegister.module.css'

const Register = ({onClose}) => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmEmail, setConfirmEmail] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const navigate = useNavigate();

  const registerMutation = useMutation(register, {
    onSuccess: () => {
      navigate('/login');  // Redireciona para a página de login após o registro
    },
    onError: (error) => {
      console.error('Error sending data:', error);
    },
  });

  const handleSubmit = (event) => {
    event.preventDefault();
    if (email!== "" && password !== "" &&
        email === confirmEmail && password === confirmPassword) {
        registerMutation.mutate({ username, email, password });
    }
  };

  return (
    <Modal
      isOpen={true} // Use um estado para controlar a visibilidade
      contentLabel="Software Form"
      ariaHideApp={false} // Para evitar warning do React Modal
      style={{
        overlay: {
          backgroundColor: 'rgba(0, 0, 0, 0.5)', // Fundo semi-transparente
        },
        content: {
          background: 'transparent', // Cor do conteúdo do modal
          border: 'transparent',
          padding: '20px',
          maxWidth: '500px',
          margin: 'auto',
        },
      }}
    >
      <div id="popup-container" className={style.popup}>
        <div className={style.overlay}>
          <div className={style.popupContent}>
            <h2>Sign up</h2>
            <form onSubmit={handleSubmit}>
              <label
                className={style.labelRegistro}
                htmlFor="username">
                  Username
              </label>
              <input
                className={style.inputRegistro}
                id="username"
                name="username"
                placeholder="Enter your username"
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              /><br/>
              <label
                className={style.labelRegistro}
                htmlFor="email">
                  E-mail
              </label>
              <input
                className={style.inputRegistro}
                id="email"
                name="email"
                placeholder="Enter your e-mail"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              /><br/>
              <label
                className={style.labelRegistro}
                htmlFor="confirm-email">
                  Confirm e-mail
              </label>
              <input
                className={style.inputRegistro}
                id="confirmEmail"
                name="confirmEmail"
                placeholder="Confirm your e-mail"
                type="email"
                value={confirmEmail}
                onChange={(e) => setConfirmEmail(e.target.value)}
                required
              /><br/>
              <label
                className={style.labelRegistro}
                htmlFor="password">
                  Password
              </label>
              <input
                className={style.inputRegistro}
                type="password"
                id="password"
                name="password"
                placeholder="Enter your password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              /><br/>
              <label
                className={style.labelRegistro}
                htmlFor="confirmPassword">
                  Confirm Password
              </label>
              <input
                className={style.inputRegistro}
                type="password"
                id="confirmPassword"
                name="confirmPassword"
                placeholder="Confirm your password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                required
              /><br/>
              <div className={style.botoes}>
                <button className={style.botaoRegistro} type="submit" disabled={registerMutation.isLoading}>
                  {registerMutation.isLoading ? 'Signing up...' : 'Sign up'}
                </button>
                <button className={style.botaoVoltarRegistro} type="button" onClick={() => onClose()}>
                  Back
                </button>
              </div><br/>
              {registerMutation.isError && (
                <p style={
                  { color: 'red',
                    fontSize: '16px',
                    fontWeight: "200" }}>Error: {registerMutation.error.message}</p>
              )}
              {registerMutation.isSuccess && <p style={
                {color: '#00EE90',
                fontSize: '16px',
                fontWeight: "200" }}>Account created sucessfully!</p>}
            </form>
          </div>
        </div>
      </div>
    </Modal>
  );
};

export default Register;
