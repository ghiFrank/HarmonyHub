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
            <button onClick={handleLogin} className='bg-green-500 p-2 border-white border-2 rounded-xl'>Get Started</button>
        </div>
    );
};

export default SpotifyLogin;