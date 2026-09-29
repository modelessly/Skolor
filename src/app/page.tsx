import { AppBar, Box, Container, Stack, Toolbar, Typography } from "@mui/material";
import { DiscoveryForm } from "@/features/discovery/discovery-form";

export default function Home() {
  return (
    <Box component="main" sx={{ minHeight: "100vh" }}>
      <AppBar position="static" color="transparent" elevation={0} component="header">
        <Toolbar sx={{ borderBottom: 1, borderColor: "divider" }}>
          <Typography variant="h6" component="span" sx={{ flexGrow: 1, fontWeight: 700 }}>
            Schools
          </Typography>
        </Toolbar>
      </AppBar>

      <Container maxWidth="lg" sx={{ py: { xs: 6, md: 10 } }}>
        <Stack spacing={6}>
          <Box sx={{ maxWidth: 760 }}>
            <Typography variant="overline" color="primary.main" sx={{ fontWeight: 700 }}>
              Swedish compulsory schools
            </Typography>
            <Typography variant="h1" sx={{ mt: 1, fontSize: { xs: "2.5rem", md: "4rem" } }}>
              Start with your nearest schools
            </Typography>
          </Box>

          <DiscoveryForm />

          <Box id="method" sx={{ maxWidth: 900 }}>
            <Typography variant="h2" sx={{ fontSize: { xs: "1.75rem", md: "2.25rem" } }}>How this works</Typography>
            <Typography color="text.secondary" sx={{ mt: 2, maxWidth: 760 }}>
              Every result will show its source, period, coverage, and underlying value. Our current national analysis found that a universal 0–100 ranking would exclude too many schools and move materially when reasonable weights change, so no composite score is shown yet.
            </Typography>
          </Box>
        </Stack>
      </Container>
    </Box>
  );
}
