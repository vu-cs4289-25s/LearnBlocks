import ReactDOM from 'react-dom/client';
import LandingPage from './pages/Landing.tsx';
import Layout from './components/Layout.tsx';

import './index.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

const root = document.getElementById('root');

if (!root) {
  throw Error('root element not found');
}

ReactDOM.createRoot(root).render(
  <BrowserRouter>
    <Layout>
      <Routes>
        <Route path="/" element={<LandingPage />} />
      </Routes>
    </Layout>
  </BrowserRouter>,
);
