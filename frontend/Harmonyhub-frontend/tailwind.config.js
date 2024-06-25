/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        poppins: ["Poppins", "serif"],
      },
      colors: {
        "custom-start": "#0d2616",
        "custom-end": "#121212",
      },
    },
  },
  plugins: [],
};

