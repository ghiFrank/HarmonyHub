// src/components/SpotifyCallback.js
import React, { useEffect } from 'react';
import axiosInstance from '../api/axios';
import { useNavigate } from 'react-router-dom';

const SpotifyCallback = () => {
    const navigate = useNavigate();

    useEffect(() => {
        const handleCallback = async () => {
            const queryParams = new URLSearchParams(window.location.search);
            const code = queryParams.get('code');

            if (code) {
                try {
                    const response = await axiosInstance.get('callback/', {
                        params: { code },
                    });
                    if (response.data.access_token) {
                        localStorage.setItem('spotify_access_token', response.data.access_token);
                        navigate('/');  // Redirect to home page or desired page after login
                    } else {
                        console.error('Failed to retrieve access token');
                    }
                } catch (error) {
                    console.error('Spotify callback handling failed:', error);
                }
            }
        };

        handleCallback();
    }, [navigate]);

    return (
        <div>
            <h1>Processing Spotify Login...</h1>
        </div>
    );
};

export default SpotifyCallback;
