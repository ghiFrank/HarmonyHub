// src/App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import SpotifyLogin from './components/SpotifyLogin';
import SpotifyCallback from './components/SpotifyCallback';

const App = () => {
    return (
        <Router>
            <div className="App">
                <header className="App-header">
                    <h1>Welcome to the Spotify App</h1>
                </header>
                <main>
                    <Routes>
                        <Route path="/" element={<SpotifyLogin />} />
                        <Route path="/callback" element={<SpotifyCallback />} />
                    </Routes>
                </main>
            </div>
        </Router>
    );
};

export default App;
