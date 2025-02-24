import './index.css';
import ReactDOM from 'react-dom/client';
import Playground from '$pages/Playground.jsx';
import LandingPage from '$pages/Landing.jsx';
import Layout from '$lib/components/Layout.jsx';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import RegistrationPage from '$pages/RegisterPage.jsx';
import LoginPage from '$pages/LoginPage';
import StudentHomePage from '$pages/StudentHomePage';
import TermsPage from '$pages/TermsPage';
import JoinClassPage from '$pages/JoinClassPage';

const root = document.getElementById('root');

if (!root) {
  throw Error('root element not found');
}

ReactDOM.createRoot(root).render(
  <BrowserRouter >
    <Layout>
      <Routes>
        <Route path="/">
          <Route index element={<LandingPage />} />
          <Route path="register" element={<RegistrationPage />} />
          <Route path="login" element={<LoginPage />} />
          <Route path="terms" element={<TermsPage />} />
          <Route path="catalog" element={<StudentHomePage />} />
          <Route path="playground" element={<Playground />} />
          <Route path="s/">
            <Route path="home" element={<StudentHomePage />} />
            <Route path="join" element={<JoinClassPage />} />
            <Route path="classes" element={<StudentHomePage />} />
            <Route path="courses" element={<StudentHomePage />} />
          </Route>
          <Route path="t/">
            <Route path="home" element={<StudentHomePage />} />
            <Route path="classes" element={<StudentHomePage />} />
            <Route path="courses" element={<StudentHomePage />} />
          </Route>
          <Route path="u/">
            <Route path="profile/:userId" element={<StudentHomePage />} />
            <Route path="edit/:userId" element={<StudentHomePage />} />
          </Route>
        </Route>
      </Routes>
    </Layout>
  </BrowserRouter>,
);
