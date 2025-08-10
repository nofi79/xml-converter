/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        smokeBlue: "#6785C1" // Azul Fumaça
      }
    }
  },
  plugins: []
}