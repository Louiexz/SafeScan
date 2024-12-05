import head from './assets/styles/Header.module.css';
import style from './assets/styles/Footer.module.css'

import Navigation from './components/Navigation';

import logo from './assets/images/logo-Soft-IA.png'

const App = () => {
  return (
    <>
      <style>
        @import url('https://fonts.googleapis.com/css2?family=Aldrich&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Albert+Sans:ital,wght@0,100..900;1,100..900&family=Aldrich&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Albert+Sans:ital,wght@0,100..900;1,100..900&family=Aldrich&family=Jura:wght@300..700&display=swap');
        @import url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css");
      </style>
      <header className={head.header}>
        <div>
            <img src={logo} alt="Logo Soft.IA"/>
            <h1>Soft.AI</h1>
        </div>
      </header>
      <Navigation/>
      <footer >
        <div className={style.footerContainer}>
            <div className={style.logoSection}>
                <img className={style.footerLogo}
                  src={logo}
                  alt="Logo Soft.IA"/>
                <h1>Soft.AI</h1>
            </div>
            <div className={style.contato}>
                <h2>Contact</h2>
                <p>(81) 1122-3344</p>
                <p>support@softai.com</p>
                <a href="https://www.instagram.com"><i className={style.biInstagram}></i></a>
                <a href="https://www.facebook.com/login/?locale=pt_BR"><i className={style.biFacebook}></i></a>
                <a href="https://x.com/?lang=pt-br"><i className={style.biTwitterX}></i></a>
            </div>
            <div className={style.endereco}>
                <h2>Location</h2>
                <p>123, Security Avenue</p>
                <p>Recife, PE, 12345678, BR</p>
            </div>
        </div>
      </footer>
    </>
  );
};

export default App;
