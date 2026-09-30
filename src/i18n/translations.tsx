"use client";

import { createContext, useContext, useMemo, useSyncExternalStore } from "react";

const messages = {
  en: {
    addressFound: "Address found:",
    addressHelper: "Sent to Geoapify only when you select Find schools; it is not stored by Skolor.",
    appName: "Skolor",
    discoveryHeading: "Find nearby schools",
    findSchools: "Find schools",
    findingSchools: "Finding schools…",
    geoAttribution: "Address lookup powered by",
    grade: "Required grade",
    homeAddress: "Home address",
    hero: "Start with your nearest schools",
    howItWorks: "How this works",
    method: "Every result will show its source, period, coverage, and underlying value. Our current national analysis found that a universal 0–100 ranking would exclude too many schools and move materially when reasonable weights change, so no composite score is shown yet.",
    schoolSearchReady: "Searching for {grade} schools is ready.",
    swedishCompulsorySchools: "Swedish compulsory schools",
    validationAddress: "Enter a home address.",
    validationGrade: "Select the required grade.",
  },
  sv: {
    addressFound: "Adress hittad:",
    addressHelper: "Adressen skickas till Geoapify först när du väljer Hitta skolor. Skolor sparar den inte.",
    appName: "Skolor",
    discoveryHeading: "Hitta närliggande skolor",
    findSchools: "Hitta skolor",
    findingSchools: "Hämtar skolor…",
    geoAttribution: "Adressökning drivs av",
    grade: "Årskurs",
    homeAddress: "Hemadress",
    hero: "Börja med skolorna närmast dig",
    howItWorks: "Så fungerar det",
    method: "Varje resultat visar källa, period, täckning och underliggande värde. Vår nationella analys visar att en universell skala från 0 till 100 skulle utesluta för många skolor och förändras väsentligt med rimliga viktningar. Därför visas inget sammansatt betyg ännu.",
    schoolSearchReady: "Sökningen efter skolor för {grade} är klar att använda.",
    swedishCompulsorySchools: "Svenska grundskolor",
    validationAddress: "Ange en hemadress.",
    validationGrade: "Välj årskurs.",
  },
} as const;

export type Locale = keyof typeof messages;
export type MessageKey = keyof (typeof messages)["en"];

type I18nContextValue = {
  locale: Locale;
  setLocale: (locale: Locale) => void;
  t: (key: MessageKey) => string;
};

const I18nContext = createContext<I18nContextValue | null>(null);

export function I18nProvider({ children }: Readonly<{ children: React.ReactNode }>) {
  const locale = useSyncExternalStore<Locale>(
    (onStoreChange) => {
      window.addEventListener("skolor.locale", onStoreChange);
      return () => window.removeEventListener("skolor.locale", onStoreChange);
    },
    () => {
      const stored = window.localStorage.getItem("skolor.locale");
      return stored === "sv" ? "sv" : "en";
    },
    () => "en",
  );

  const value = useMemo<I18nContextValue>(() => ({
    locale,
    setLocale: (nextLocale) => {
      window.localStorage.setItem("skolor.locale", nextLocale);
      window.dispatchEvent(new Event("skolor.locale"));
    },
    t: (key) => messages[locale][key],
  }), [locale]);

  return <I18nContext.Provider value={value}>{children}</I18nContext.Provider>;
}

export function useI18n() {
  const context = useContext(I18nContext);
  if (!context) throw new Error("useI18n must be used within I18nProvider.");
  return context;
}
