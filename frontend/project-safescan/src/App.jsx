import head from './assets/styles/Header.module.css';
import style from './assets/styles/Footer.module.css'

import Navigation from './components/Navigation';

const App = () => {
  return (
    <>
      <header className={head.header}>
        <div>
            <img src="./Asserts/logo-Soft-IA.png" alt="Logo Soft.IA"/>
            <h1>Soft.AI</h1>
        </div>
      </header>
      <Navigation/>
      <footer>
        <div className={style.footerContainer}>
            <div className={style.logoSection}>
                <img className={style.footerLogo}
                  src="../assets/images/logo-Soft-IA.png"
                  alt="Logo Soft.IA"/>
                <h1>Soft.AI</h1>
            </div>
            <div className={style.contato}>
                <h2>Contact</h2>
                <p>(81) 1122-3344</p>
                <p>support@softai.com</p>
                <a href="https://www.instagram.com"><i className={style.biInstagram}></i></a>
                <a href="https://www.facebook.com/login/?locale=pt_BR"><i className={style.bFacebook}></i></a>
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
