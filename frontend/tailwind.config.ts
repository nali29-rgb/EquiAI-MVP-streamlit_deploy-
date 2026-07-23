import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          canvas: "#FFF1F9",
          blue: "#748BC5",
          coral: "#F18D7A",
          dark: "#171717",
        },
      },
    },
  },
  plugins: [],
};
export default config;
