import { Box, Typography } from "@mui/material";

const version = process.env.NEXT_PUBLIC_APP_VERSION ?? "0.1.0";

export function VersionBadge() {
  return (
    <Box
      aria-label={`Application version ${version}`}
      sx={{
        bottom: 16,
        color: "text.secondary",
        left: 16,
        position: "fixed",
        zIndex: 1100,
      }}
    >
      <Typography variant="caption">v{version}</Typography>
    </Box>
  );
}
