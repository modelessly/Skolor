"use client";

import { useState } from "react";
import { Alert, Box, Button, Chip, Link, Paper, Stack, TextField, Typography } from "@mui/material";
import type { DiscoveryResponse } from "@/features/discovery/types";

const grades = ["F", "1", "2", "3", "4", "5", "6", "7", "8", "9"];

export function DiscoveryForm() {
  const [address, setAddress] = useState("");
  const [grade, setGrade] = useState<string | null>(null);
  const [submitted, setSubmitted] = useState(false);
  const [result, setResult] = useState<DiscoveryResponse | null>(null);
  const [searching, setSearching] = useState(false);

  const canSearch = address.trim().length > 0 && grade !== null;
  const addressError = submitted && !address.trim() ? "Enter a home address." : undefined;
  const gradeError = submitted && !grade ? "Select the required grade." : undefined;

  async function submit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitted(true);
    if (!canSearch) return;
    setSearching(true);
    setResult(null);
    try {
      const response = await fetch("/api/discovery", {
        body: JSON.stringify({ address }),
        headers: { "Content-Type": "application/json" },
        method: "POST",
      });
      setResult((await response.json()) as DiscoveryResponse);
    } catch {
      setResult({ error: "The address service is temporarily unavailable. Try again shortly." });
    } finally {
      setSearching(false);
    }
  }

  return (
    <Paper component="form" aria-label="Find nearby schools" elevation={1} onSubmit={submit} sx={{ p: { xs: 2, md: 4 }, maxWidth: 900 }}>
      <Stack spacing={3}>
        <TextField
          fullWidth
          label="Home address"
          placeholder="Knektedalsgatan 2B, Göteborg"
          helperText={addressError ?? "Sent to Geoapify only when you select Find schools; it is not stored by Schools."}
          error={Boolean(addressError)}
          value={address}
          onChange={(event) => setAddress(event.target.value)}
          autoComplete="street-address"
        />
        <Box>
          <Typography component="h2" variant="subtitle1" sx={{ mb: 1.5, fontWeight: 650 }}>
            Required grade
          </Typography>
          <Stack direction="row" useFlexGap sx={{ flexWrap: "wrap", gap: 1 }}>
            {grades.map((item) => (
              <Chip
                key={item}
                label={item}
                clickable
                color={grade === item ? "primary" : "default"}
                variant={grade === item ? "filled" : "outlined"}
                onClick={() => setGrade(item)}
                aria-pressed={grade === item}
                aria-label={`Grade ${item}`}
              />
            ))}
          </Stack>
          {gradeError && <Typography role="alert" color="error" variant="body2" sx={{ mt: 1 }}>{gradeError}</Typography>}
        </Box>
        <Box>
          <Button type="submit" variant="contained" size="large" disabled={searching}>
            {searching ? "Finding schools…" : "Find schools"}
          </Button>
        </Box>
        <Typography variant="caption" color="text.secondary">
          Address lookup powered by <Link href="https://www.geoapify.com/" target="_blank" rel="noreferrer">Geoapify</Link>.
        </Typography>
        {result?.error && <Alert severity="error">{result.error}</Alert>}
        {result?.location && (
          <Alert severity="success">
            Address found: {result.location.label}. Searching for {grade === "F" ? "förskoleklass" : `grade ${grade}`} schools is ready.
          </Alert>
        )}
        {result?.warning && <Alert severity="info">{result.warning}</Alert>}
      </Stack>
    </Paper>
  );
}
