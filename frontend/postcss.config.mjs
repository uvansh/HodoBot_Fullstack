const config = {
  content: [
      "./pages/**/*.{js,ts,jsx,tsx,mdx}",
      "./components/**/*.{js,ts,jsx,tsx,mdx}",
      "./app/**/*.{js,ts,jsx,tsx,mdx}",
    ],
    theme: {
      extend: {
        colors: {
          dark: {
            bg: "#0a0a0a",
            card: "#1a1a1a",
            hover: "#2a2a2a",
            border: "#333333",
            text: "#e5e5e5",
            "text-dim": "#a0a0a0",
          },
          accent: {
            blue: "#3b82f6",
            "blue-dark": "#2563eb",
            green: "#10b981",
            purple: "#8b5cf6",
          },
        },
        fontFamily: {
          sans: ["Inter", "system-ui", "sans-serif"],
          mono: ["JetBrains Mono", "Fira Code", "monospace"],
        },
      },
    },
  plugins: {
    "@tailwindcss/postcss": {},
  },
};

export default config;
