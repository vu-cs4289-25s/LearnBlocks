import './index.css';
import React from 'react';
import ReactDOM from 'react-dom/client';
import Heading from './components/header/Heading.js';
import LandingPage from './components/landing/Landing.js';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <Heading />
    <LandingPage />
  </React.StrictMode>
);