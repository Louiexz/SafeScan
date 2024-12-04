import { useState } from 'react';
import { useQuery, useMutation } from 'react-query';
import { fetchProfile, updateProfile } from '../services/profileService';
import { logout } from '../services/authService';
import { deleteSoftware } from '../services/softwareService';
import PopupSoftware from '../components/softwarePopup';

const Profile = () => {
  const [softwareToUpdate, setSoftwareToUpdate] = useState(null);
  const [showPopup, setShowPopup] = useState(false);
  const [profileData, setProfileData] = useState({});
  const [name, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  
  const { data: response, error, isLoading, refetch } = useQuery('profile', fetchProfile, {
    refetchOnWindowFocus: false,
    onSuccess: (response) => {
      setProfileData(response.data);
      setUsername(response.data.data.username);
      setEmail(response.data.data.email);
      setPassword(''); // Esvazia o campo de senha por segurança
    },
  });

  const updateMutation = useMutation(updateProfile);
  const logoutMutation = useMutation(logout);

  const handleUpdate = () => {
    if (name !== profileData.username ||
        email !== profileData.email) {
      const updatedData = { name, password, email };
      updateMutation.mutate(updatedData);
    } else {
      alert("Deve ter pelo menos um valor diferente.");
    }
  };

  const handleDelete = (id) => {
  deleteSoftware(id)
    .then(() => {
      console.log('Software deletado com sucesso');
      window.location.reload()
    })
    .catch((error) => {
      console.error('Erro ao deletar software:', error);
    });
  };

  if (isLoading) return <p className="content">Carregando perfil...</p>;
  if (error) return <p className="content">Erro ao carregar perfil: {error.message}</p>;

  return (
    <div>
      <h1>Perfil</h1>
      <label htmlFor="name">
        Nome:
        <input
          className="profile-inputs"
          value={name}
          id="name"
          onChange={(e) => setUsername(e.target.value)}
        />
      </label><br/>
      <label htmlFor="email">
        Email:
        <input
          className="profile-inputs"
          value={email}
          id="email"
          onChange={(e) => setEmail(e.target.value)}
        />
      </label><br/>
      <label htmlFor="password">
        Senha:
        <input
          type="password"
          className="profile-inputs"
          value={password}
          id="password"
          onChange={(e) => setPassword(e.target.value)}
        />
      </label><br/>

      <button onClick={handleUpdate}>
        {updateMutation.isLoading ? 'Atualizando...' : 'Atualizar Perfil'}
      </button><br/>
      
      {updateMutation.isError && <p style={{ color: 'red' }}>Erro: {updateMutation.error.message}</p>}
      {updateMutation.isSuccess && <p style={{ color: 'green' }}>Perfil atualizado com sucesso!</p>}
      <br/>
      {profileData.softwares && profileData.softwares.length > 0 ? (
        <div className="cards">
          {profileData.softwares.map((software) => (
            <div className="card" key={software.id}>
              <span>Nome: {software.name}</span><br />
              <span>Status: {software.label}</span><br />
              <span>Criado em: {software.created_at}</span><br />
              <span>Atualizado em: {software.updated_at}</span><br />
              <button onClick={() => {
                setShowPopup(true);
                setSoftwareToUpdate(software)
              }}>Update software</button>

              {showPopup && (
                <PopupSoftware 
                  method="update"
                  data={softwareToUpdate}
                  onClose={() => setShowPopup(false)}
                  refetch={refetch}
                />
              )}
              <button onClick={() => handleDelete(software.id)}>Deletar</button>
            </div>
          ))}
        </div>
      ) : (
        <span>Usuário não possui softwares.</span>
      )}
      <br/>
      <button onClick={() => logoutMutation.mutate()}>
        {logoutMutation.isLoading ? 'Saindo...' : 'Sair da conta'}
      </button><br/>
    </div>
  );
};

export default Profile;
