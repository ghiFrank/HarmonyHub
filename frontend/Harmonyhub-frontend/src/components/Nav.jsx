import React from 'react'
import { navLists } from '../utils/navlist';

const Nav = () => {
  return (
    <header className=" bg-black text-white w-full py-2 sm:px-10 flex justify-between items-center">
      <nav className="flex  w-full  gap-[60%]">
        <div className="flex   ">
          <a href="/">
            <img
              src="../public/logo.png"
              alt="logo"
              width={50}
              height={50}
              className="ml-5"
            />
            <label className=' font-bold'>Harmony Hub</label>
          </a>
        </div>

        <div className="flex gap-7 justify-center items-center max-sm:hidden font-bold">
          {navLists.map((nav) => (
            <a
              key={nav}
              className="px-5 text-14px cursor-pointer text-white "
              href={`/${nav === "Home" ? "" : nav}`}
            >
              {nav}
            </a>
          ))}
        </div>
      </nav>
    </header>
  );
}

export default Nav;