import type { Metadata } from "next";
import { AppRouterCacheProvider } from "@mui/material-nextjs/v16-appRouter";
import { CssBaseline, ThemeProvider } from "@mui/material";
import { theme } from "@/theme/theme";
import { VersionBadge } from "@/app/version-badge";
import { I18nProvider } from "@/i18n/translations";

export const metadata: Metadata = {
  title: "Skolor — Swedish school research",
  description: "Find and compare Swedish compulsory schools using transparent public evidence.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>
        <AppRouterCacheProvider options={{ enableCssLayer: true }}>
          <ThemeProvider theme={theme}>
            <CssBaseline />
            <I18nProvider>
              {children}
              <VersionBadge />
            </I18nProvider>
          </ThemeProvider>
        </AppRouterCacheProvider>
      </body>
    </html>
  );
}
