// This file can be used for more complex theme configurations if needed,
// especially if not using Tailwind or for custom JS-in-CSS solutions.
// For now, tailwind.config.ts holds the primary theme definitions.

export const theme = {
  colors: {
    primary: "#1565C0",
    secondary: "#43A047",
    accent: "#FF7043",
    background: "#FAFAFA",
    textMain: "#212121",
    interactive: "#7B1FA2",
  },
  fonts: {
    poppins: "Poppins, sans-serif",
    inter: "Inter, sans-serif",
    jetBrainsMono: "JetBrains Mono, monospace",
  },
  spacing: {
    base: "20px",
  },
};

// Example usage (not directly applied in Tailwind setup):
// const GlobalStyle = createGlobalStyle`
//   body {
//     background-color: ${theme.colors.background};
//     color: ${theme.colors.textMain};
//     font-family: ${theme.fonts.inter};
//   }
// `;
