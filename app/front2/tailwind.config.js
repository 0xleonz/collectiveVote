/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/app/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        mocha: {
          background: "#212121",
          surface:    "#2A2A2A",
          overlay:    "#393939",
          muted:      "#6E6E6E",
          text:       "#DCD7BA",
          blue:       "#8AB0F2",
          peach:      "#F5BDE6",
        }
      }
    }
  },
  plugins: [],
}

