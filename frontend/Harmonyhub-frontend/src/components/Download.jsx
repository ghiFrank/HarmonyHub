import React from 'react'

const Download = () => {
  return (
    <div className=" flex flex-col h-full mt-8 bg-[#121212]  rounded-lg  justify-center items-center  gap-15">
        <h1 className="text-white font-bold text-4xl p-10">
          Scan To Download Spotify App
        </h1>


      <img src="./public/download.png" width={300} className="flex-end mt-20" />
    </div>
  );
}

export default Download