// src/services/api.js
import axios from 'axios';
import { getCookie } from '../components/cookieService'

// Pega o CSRF Token do cookie
const csrftoken = getCookie('csrftoken');
const token = localStorage.getItem('token');  // Obtém o token salvo no localStorage

// Configuração padrão do Axios
const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
  headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': csrftoken,
    Authorization: token ? `Token ${token}` : {},
  },
  withCredentials:true
});

api.interceptors.response.use(
  response => response, // Retorna a resposta normalmente
  error => {
    if (error.response && error.response.status === 403) {
      window.location.href ='/login'; // Redireciona para login se erro 403
    }
    return Promise.reject(error); // Se não for erro 403, rejeita a promessa
  }
);

export default api;
