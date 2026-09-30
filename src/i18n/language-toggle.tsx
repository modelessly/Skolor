"use client";

import { ToggleButton, ToggleButtonGroup } from "@mui/material";
import { useI18n, type Locale } from "@/i18n/translations";

export function LanguageToggle() {
  const { locale, setLocale } = useI18n();
  return (
    <ToggleButtonGroup
      exclusive
      size="small"
      value={locale}
      aria-label="Language"
      onChange={(_, value: Locale | null) => value && setLocale(value)}
    >
      <ToggleButton value="en" aria-label="English">EN</ToggleButton>
      <ToggleButton value="sv" aria-label="Svenska">SV</ToggleButton>
    </ToggleButtonGroup>
  );
}
