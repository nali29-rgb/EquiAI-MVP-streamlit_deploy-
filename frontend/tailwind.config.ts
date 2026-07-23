import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{js,ts,jsx,tsx}", "./components/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        brand: {
          canvas: "#FFF1F9", // Soft Pink background accent
          blue: "#748BC5",   // Royal Primary
          coral: "#F18D7A",  // Risk / Action Accent
          dark: "#171717",   // Crisp Typography
        }
      }
    }
  },
  plugins: [],
};
export default config;