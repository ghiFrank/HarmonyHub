import React from 'react'
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import SpotifyLogin from "./SpotifyLogin";
import SpotifyCallback from "./SpotifyCallback";

const Hero = () => {
  return (
    <main className="flex w-full h-full justify-center gap-2 text-center text-white relative">
      <div className="w-[50%] flex flex-col gap-5 bg-[#121212] rounded-lg  justify-center">
        <h1 className=" font-bold text-[50px]  ">Welcome to Harmony Hub</h1>
        <p className="text-sm ml-2 mr-2">
          Your Personalized Soundtrack Awaits! Dive into a world of music
          perfectly curated from your Spotify favorites.
        </p>
        <button>
          <Routes>
            <Route path="/" element={<SpotifyLogin />} />
            <Route path="/callback" element={<SpotifyCallback />} />
          </Routes>
        </button>
      </div>
      <div className="relative w-[50%] bg-gradient-to-b from-custom-start to-custom-end flex justify-center rounded-lg items-center ">
        <img src="./public/spotify.png" className="absolute    z-100" />

        <img src="./public/hero.png" width={500} className="z-0" />

        <img
          src="./public/song1.png"
          width={300}
          className="absolute top-[80%] left-[30%]"
        />

        <img
          src="./public/song2.png"
          width={300}
          className="absolute top-[70%] left-[5%]"
        />
      </div>
    </main>
  );
}

export default Hero;