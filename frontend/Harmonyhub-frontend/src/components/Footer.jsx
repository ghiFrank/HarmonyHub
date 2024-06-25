import React from 'react';
import { FaXTwitter } from "react-icons/fa6";
import { FaInstagram, FaFacebookF } from "react-icons/fa";

const footer = () => {
  return (
    <div className="flex flex-col mt-8 bg-[#121212] rounded-lg justify-center items-center pt-10  px-10 gap-20">
      <div className="flex justify-between w-full items-stretch">
        <div className="flex items-start flex-1">
          <img src="./public/logo.png" alt="Logo" className="h-10 w-10" />
        </div>

        <div className="flex flex-col items-center gap-2 flex-1">
          <h3 className="text-white text-lg font-semibold">Navigation</h3>
          <div className="flex flex-col gap-2">
            <a href="#" className="text-white hover:underline">
              Home
            </a>
            <a href="#" className="text-white hover:underline">
              About
            </a>
            <a href="#" className="text-white hover:underline">
              Contact
            </a>
          </div>
        </div>

        <div className="flex flex-col items-center gap-2 text-white flex-1">
          <h3 className="text-lg font-semibold">Credit</h3>
          <h4>Amine Atyq</h4>
          <h4>Ayoub Abouchadi</h4>
        </div>

        <div className="flex items-start space-x-4 flex-1 justify-end">
          <a
            href="https://facebook.com"
            target="_blank"
            className="text-white hover:underline"
          >
            <FaFacebookF />
          </a>
          <a
            href="https://twitter.com"
            target="_blank"
            className="text-white hover:underline"
          >
            <FaXTwitter />
          </a>
          <a
            href="https://instagram.com"
            target="_blank"
            className="text-white hover:underline"
          >
            <FaInstagram />
          </a>
        </div>
      </div>

      <div className="text-center text-white mt-4">&copy; 2024 ALX-Morocco</div>
    </div>
  );
}

export default footer