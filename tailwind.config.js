/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ["*.html"],
    theme: {
      extend: {},
    },
    plugins: [],
  }
  // tailwind.config.js
module.exports = {
  theme: {
    // ...
  },
  plugins: [
    require('@tailwindcss/forms'),
    // ...
  ],
}