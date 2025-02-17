import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './Login';
import ProtectedPage from './ProtectedPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login/>}/>
        <Route path="/protected" element={<ProtectedPage/>}/>
      </Routes>
    </Router>
  );
}

export default App;