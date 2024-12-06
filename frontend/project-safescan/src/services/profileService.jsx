import api from './api';

// Função para buscar os dados do perfil

export const fetchProfile = () => {
  return api.get('/profile')
};

// Função para atualizar os dados do perfil
export const updateProfile = (data) => {
    return api.put('/profile-update/', data);
}