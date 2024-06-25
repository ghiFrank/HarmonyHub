import React from 'react';
import axios from 'axios';  // Use axios for making HTTP requests

const SpotifyLogin = () => {
    const handleLogin = async () => {
        try {
            const response = await axios.get('http://localhost:8000/api/login');  // Adjust URL as per your Django setup
            console.log('Redirecting to Spotify authorization:', response);
        } catch (error) {
            console.error('Spotify authorization failed:', error);
        }
    };

    return (
        <div>
            <h1>Login with Spotify</h1>
            <button onClick={handleLogin}>Login with Spotify</button>
        </div>
    );
};

export default SpotifyLogin;