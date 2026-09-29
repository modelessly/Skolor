"use client";

import { createTheme } from "@mui/material/styles";

export const theme = createTheme({
  cssVariables: true,
  palette: {
    mode: "light",
    primary: { main: "#315E78", dark: "#173F57", light: "#D1E6F3" },
    secondary: { main: "#356A64" },
    background: { default: "#F8FAFB", paper: "#FFFFFF" },
    text: { primary: "#172126", secondary: "#52616A" },
  },
  shape: { borderRadius: 10 },
  typography: {
    fontFamily: "Roboto, Arial, sans-serif",
    h1: { fontWeight: 650, letterSpacing: "-0.025em" },
    h2: { fontWeight: 650, letterSpacing: "-0.015em" },
    button: { textTransform: "none", fontWeight: 650 },
  },
  components: {
    MuiButton: { defaultProps: { disableElevation: true }, styleOverrides: { root: { minHeight: 44 } } },
    MuiTextField: { defaultProps: { variant: "outlined" } },
  },
});
