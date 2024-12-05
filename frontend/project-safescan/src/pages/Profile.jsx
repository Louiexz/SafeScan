import { useState } from 'react';
import { useQuery, useMutation } from 'react-query';
import { fetchProfile, updateProfile } from '../services/profileService';
import { logout } from '../services/authService';
import { deleteSoftware } from '../services/softwareService';
import PopupSoftware from '../components/softwarePopup';

import style from '../assets/styles/Profile.module.css'

import group from '../assets/images/profile/Group 1.png'
import pencil from '../assets/images/profile/pencil-square 3.png'
import imageOne from '../assets/images/profile/image 1.png'

const Profile = () => {
  const [softwareToUpdate, setSoftwareToUpdate] = useState(null);
  const [showPopup, setShowPopup] = useState(false);
  const [profileData, setProfileData] = useState({});
  const [username, setUsername] = useState('');
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
    if (username !== profileData.username ||
        email !== profileData.email) {
      const updatedData = { username, password, email };
      updateMutation.mutate(updatedData);
    } else {
      alert("Deve ter pelo menos um valor diferente.");
    }
  };

  const handleDelete = (id) => {
  deleteSoftware(id)
    .then(() => {
      console.log('Software deletado com sucesso');
      refetch();
    })
    .catch((error) => {
      console.error('Erro ao deletar software:', error);
    });
  };

  if (isLoading) return <p >Carregando perfil...</p>;
  if (error) return <p >Erro ao carregar perfil: {error.message}</p>;

  return (
    <div className={style.profileBody}>
      <div className={style.gridPerfil}>
        <div className={style.containerPerfil}>
          <div className={style.infoPerfil}>
            <div className={style.logo}>
              <span><img src={group} alt=""/></span>
                <h1>Profile</h1>
            </div>
            <div className={style.user}>
              <h1>HELLO, <br/> {name}</h1>
              <div className={style.descricao}>
                <label htmlFor="name">
                  Nome:
                  <input
                    className={style.inputs}
                    value={username}
                    id="name"
                    onChange={(e) => setUsername(e.target.value)}
                  />
                </label><br/>
                <label htmlFor="email">
                  Email:
                  <input
                    className={style.inputs}
                    value={email}
                    id="email"
                    onChange={(e) => setEmail(e.target.value)}
                  />
                </label><br/>
                <label htmlFor="password">
                  Senha:
                  <input
                    type="password"
                    className={style.inputs}
                    value={password}
                    id="password"
                    onChange={(e) => setPassword(e.target.value)}
                  />
                </label><br/>
                <button className={style.backButton} onClick={handleUpdate}>
                  {updateMutation.isLoading ? 'Updating...' : 'Update'}
                </button><br/>
                
                {updateMutation.isError && (
                  <p className={style.errorMessage}>Erro: {updateMutation.error.message}</p>
                )}
                {updateMutation.isSuccess && (
                  <p className={style.successMessage}>Perfil atualizado com sucesso!</p>
                )}

                <button className={style.backButton} onClick={() => logoutMutation.mutate()}>
                  {logoutMutation.isLoading ? 'Exiting...' : 'Sign out'}
                </button><br/>
              </div>
            </div>
          </div>
        <img className={style.foto} src={imageOne}/>
        </div>
      </div>
      <div className={style.programs}>
        <h1 id="programs"> Registered Programs</h1>
        {profileData.softwares && profileData.softwares.length > 0 ? (
          <div>
            {profileData.softwares.map((software) => (
              <div className={style.verification} key={software.id}>
                <span>Name: {software.name}</span><br />
                <span>Status: {software.label}</span><br />
                <span>Created at: {software.created_at}</span><br />
                <span>Updated at: {software.updated_at}</span><br />
                <button className={style.buttonProfile} onClick={() => {
                  setShowPopup(true);
                  setSoftwareToUpdate(software)
                }}>Update software</button>

                {showPopup && (
                  <PopupSoftware
                    method="update"
                    data={softwareToUpdate}
                    onClose={() => {
                      setShowPopup(false);
                      setSoftwareToUpdate(null); // Limpa o software selecionado
                      refetch(); // Recarrega os dados
                    }}
                  />
                )}
                <button className={style.buttonProfile} onClick={() => handleDelete(software.id)}>Deletar</button>
              </div>
            ))}
          </div>
        ) : (
          <span>User don't have softwares.</span>
        )}
      </div>
    </div>
  );
};

export default Profile;
