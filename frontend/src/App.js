import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import '@/App.css';
import LandingPage from './pages/LandingPage';
import ResearchPage from './pages/ResearchPage';

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/research" element={<ResearchPage />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;