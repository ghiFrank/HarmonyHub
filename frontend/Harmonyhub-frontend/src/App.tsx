// src/App.js
import React from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import Nav from './components/Nav.jsx';
import Hero from "./components/Hero.jsx";
import Download from "./components/Download.jsx";
import Footer from "./components/Footer.jsx";
const App = () => {
    return (
      <div className='bg-black'>
        <Router>
          <Nav />
          <Hero />
          <Download />
          <Footer />
        </Router>
      </div>
    );
};

export default App;
