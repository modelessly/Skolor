"use client";

import { AppBar, Box, Container, Stack, Toolbar, Typography } from "@mui/material";
import { DiscoveryForm } from "@/features/discovery/discovery-form";
import { LanguageToggle } from "@/i18n/language-toggle";
import { useI18n } from "@/i18n/translations";

export default function Home() {
  const { t } = useI18n();
  return (
    <Box component="main" sx={{ minHeight: "100vh" }}>
      <AppBar position="static" color="transparent" elevation={0} component="header">
        <Toolbar sx={{ borderBottom: 1, borderColor: "divider" }}>
          <Typography variant="h6" component="span" sx={{ flexGrow: 1, fontWeight: 700 }}>
            {t("appName")}
          </Typography>
          <LanguageToggle />
        </Toolbar>
      </AppBar>

      <Container maxWidth="lg" sx={{ py: { xs: 6, md: 10 } }}>
        <Stack spacing={6}>
          <Box sx={{ maxWidth: 760 }}>
            <Typography variant="overline" color="primary.main" sx={{ fontWeight: 700 }}>
              {t("swedishCompulsorySchools")}
            </Typography>
            <Typography variant="h1" sx={{ mt: 1, fontSize: { xs: "2.5rem", md: "4rem" } }}>
              {t("hero")}
            </Typography>
          </Box>

          <DiscoveryForm />

          <Box id="method" sx={{ maxWidth: 900 }}>
            <Typography variant="h2" sx={{ fontSize: { xs: "1.75rem", md: "2.25rem" } }}>{t("howItWorks")}</Typography>
            <Typography color="text.secondary" sx={{ mt: 2, maxWidth: 760 }}>
              {t("method")}
            </Typography>
          </Box>
        </Stack>
      </Container>
    </Box>
  );
}
