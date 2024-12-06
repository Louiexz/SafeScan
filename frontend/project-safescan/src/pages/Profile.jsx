import { useState } from 'react';
import { useQuery, useMutation } from 'react-query';
import { fetchProfile, updateProfile } from '../services/profileService';
import { logout } from '../services/authService';
import { deleteSoftware } from '../services/softwareService';
import PopupSoftware from '../components/softwarePopup';
import { useNavigate } from 'react-router-dom';

import style from '../assets/styles/Profile.module.css'

import group from '../assets/images/profile/Group 1.png'
import pencil from '../assets/images/profile/pencil-square 3.png'
import imageOne from '../assets/images/profile/image 1.png'

const Profile = () => {
  const [softwareToUpdate, setSoftwareToUpdate] = useState(null); // Armazena o software que será atualizado
  const [profileData, setProfileData] = useState({});
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const navigate = useNavigate();

  const { data: response, error, isLoading, refetch } = useQuery('profile', fetchProfile, {
    refetchOnWindowFocus: false,
    onSuccess: (response) => {
      setProfileData(response.data);
      setUsername(response.data.data.username);
      setEmail(response.data.data.email);
      setPassword(''); // Esvazia o campo de senha por segurança
    },
    onError: () => {
      navigate('/');
      navigate('/profile');
    },
  });

  const updateMutation = useMutation(updateProfile);
  const logoutMutation = useMutation(logout);

  const handleUpdate = () => {
    if (username !== profileData.username || email !== profileData.email) {
      const updatedData = { username, password, email };
      updateMutation.mutate(updatedData);
    } else {
      alert("May have one different value.");
    }
  };

  const handleDelete = (id) => {
    deleteSoftware(id)
      .then(() => {
        console.log('Software deleted successfully');
        refetch();
      })
      .catch((error) => {
        console.error('Error to delete software:', error);
      });
  };

  if (isLoading) return (
    <div className={style.profileBody}>
      <div className={style.gridPerfil}>
        <div className={style.containerPerfil}>
          <div className={style.infoPerfil}>
            <div className={style.logo}>
              <h1>Loading profile...</h1>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
  if (error) {
    navigate('/')
    window.location.reload()
    return (
      <div className={style.profileBody}>
        <div className={style.gridPerfil}>
          <div className={style.containerPerfil}>
            <div className={style.infoPerfil}>
              <div className={style.logo}>
                <h1>Fetching profile...</h1>
              </div>
            </div>
          </div>
        </div>
      </div>
    )
  }
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
              <h1>HELLO, <br/> {username}</h1>
              <div className={style.descricao}>
                <label htmlFor="username">
                  User:
                  <br/>
                  <input
                    className={style.inputs}
                    value={username}
                    id="username"
                    onChange={(e) => setUsername(e.target.value)}
                  />
                </label><br/>
                <label htmlFor="email">
                  Email:
                  <br/>
                  <input
                    className={style.inputs}
                    value={email}
                    id="email"
                    onChange={(e) => setEmail(e.target.value)}
                  />
                </label><br/>
                <label htmlFor="password">
                  Password:
                  <br/>
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
                  <p className={style.errorMessage}>Error: All data required or invalid values.</p>
                )}
                {updateMutation.isSuccess && (
                  <p className={style.successMessage}>Profile updated sucessfully!</p>
                )}

                <button className={style.backButton} onClick={() => logoutMutation.mutate()}>
                  {logoutMutation.isLoading ? 'Signing out...' : 'Sign out'}
                </button><br/>
              </div>
            </div>
          </div>
        <img className={style.foto} src={imageOne}/>
        </div>
      </div>
      <div className={style.programs}>
        <h1 id="programs">Registered Programs</h1>
        {profileData.softwares && profileData.softwares.length > 0 ? (
          <div>
            {profileData.softwares.map((software) => (
              <div className={style.verification} key={software.id}>
                <span>Name: {software.name}</span><br />
                <span>Status: {software.label}</span><br />

                <button
                  className={style.buttonProfile}
                  onClick={() => setSoftwareToUpdate(software)}
                >
                  Update software
                </button>

                {softwareToUpdate && softwareToUpdate.id === software.id && (
                  <PopupSoftware
                    method="update"
                    data={softwareToUpdate}
                    onClose={() => setSoftwareToUpdate(null)}
                    softName={software.name}
                    refetch={refetch}
                  />
                )}
                <button
                  className={style.buttonProfile}
                  onClick={() => handleDelete(software.id)}
                >
                  Delete
                </button>
              </div>
            ))}
          </div>
        ) : (
          <span>User doesn't have any software.</span>
        )}
      </div>
    </div>
  );
};

export default Profile;
