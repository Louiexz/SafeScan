// src/services/authService.js
import api from './api';

// Função de login
export const login = async (data) => {
  const response = await api.post('/sign-in', data);

  // Salve o token no localStorage (ou sessionStorage, conforme sua necessidade)
  localStorage.setItem('token', response.data.token);

  return response.data;
};

// Função de logout
export const logout = async () => {
  try {
    window.location.href ='/login';
    return api.get('/sign-out');
  } catch (error) {
    console.error("Erro ao tentar fazer logout:", error);
  }
};

// Função de registro
export const register = (data) => api.post('/sign-up', data);

// Solicitar redefinição de senha
export const forgotPassword = (email) => api.post('/forgot-password', { email });

// Confirmar nova senha com token
export const resetPassword = (uidb64, token, password) =>
  api.patch(`/reset-password/${uidb64}/${token}/`, { password });
