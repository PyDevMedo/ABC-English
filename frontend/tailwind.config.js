/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        journey: {
          blue: "#38bdf8",
          purple: "#a855f7",
          yellow: "#facc15",
          pink: "#f472b6",
          green: "#4ade80",
          orange: "#fb923c"
        }
      },
      fontFamily: {
        fredoka: ['Fredoka', 'sans-serif'],
        cairo: ['Cairo', 'sans-serif']
      }
    },
  },
  plugins: [],
}
