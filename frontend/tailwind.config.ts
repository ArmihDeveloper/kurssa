import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: "#1565C0", // education blue
        secondary: "#43A047", // progress green
        accent: "#FF7043", // highlight orange
        background: "#FAFAFA", // light grey
        textMain: "#212121", // charcoal
        interactive: "#7B1FA2", // purple
      },
      fontFamily: {
        poppins: ["Poppins", "sans-serif"],
        inter: ["Inter", "sans-serif"],
        jetBrainsMono: ["JetBrains Mono", "monospace"],
      },
      spacing: {
        '20px': '20px',
      }
    },
  },
  plugins: [],
};
export default config;
