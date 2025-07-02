/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html", //Template at the project level
    "./**/templates/**/*.html", //Template inside app
    "./**/*.html"
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

