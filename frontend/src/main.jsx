import './index.css';
import ReactDOM from 'react-dom/client';
import LandingPage from './pages/Landing.jsx';
import Layout from './components/Layout.jsx';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import RegistrationPage from './pages/RegisterPage.jsx';
import LoginPage from './pages/LoginPage.jsx';

const root = document.getElementById('root');

if (!root) {
  throw Error('root element not found');
}

ReactDOM.createRoot(root).render(
  <BrowserRouter>
    <Layout>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/register" element={<RegistrationPage />} />
        <Route path="/login" element={<LoginPage />} />
      </Routes>
    </Layout>
  </BrowserRouter>,
);
