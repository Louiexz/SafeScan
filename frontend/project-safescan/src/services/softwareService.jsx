import api from './api';

// Função para listar softwares (necessita de login)
export const listSoftwares = () => {
  return api.get('/software');
};

// Função para criar um novo software (com ou sem login)
export const createSoftware = (data) => {
  const token = localStorage.getItem('token');
  return api.post('/software', data, { withCredentials: false });//token ? true : false });
};

export const checkSoftware = (data) => {
  const token = localStorage.getItem('token'); 

  return api.post('/virustotal', data, {
    withCredentials: false
  });
};

// Função para excluir um software específico (precisa de login)
export const deleteSoftware = (id) => {
  return api.delete(`/delete-software/${id}/`, {
    withCredentials: false
  });
};
