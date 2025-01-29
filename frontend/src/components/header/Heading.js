import logo from '../../assets/logo.png';
import './Heading.css';

function Heading() {
  return (
    <header id="page-header">
      <img src={logo} className="logo" alt="logo" />
      <h3 id="title">LearnBlox</h3>
      <button id="login-button">Login</button>
    </header>
  );
}

export default Heading;