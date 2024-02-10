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
module.exports = {
  theme: {
    extend: {
      animation: {
        'border-color-change': 'border-color-change 2s infinite',
      },
      keyframes: {
        'border-color-change': {
          '0%': { borderColor: '#ff0000' },
          '33%': { borderColor: '#00ff00' },
          '66%': { borderColor: '#0000ff' },
          '100%': { borderColor: '#ff0000' },
        },
      },
    },
  },
  variants: {},
  plugins: [],
}
