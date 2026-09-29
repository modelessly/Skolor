import type { GeocodedAddress } from "@/features/discovery/types";

type GeoapifyResponse = {
  features?: Array<{
    geometry?: { coordinates?: [number, number] };
    properties?: { formatted?: string };
  }>;
};

export class GeocodingUnavailableError extends Error {}

export async function geocodeSwedishAddress(address: string): Promise<GeocodedAddress | null> {
  const apiKey = process.env.GEOAPIFY_API_KEY;
  if (!apiKey) {
    throw new GeocodingUnavailableError("Geoapify has not been configured.");
  }

  const query = new URLSearchParams({
    apiKey,
    filter: "countrycode:se",
    format: "json",
    limit: "1",
    text: address,
  });
  const response = await fetch(`https://api.geoapify.com/v1/geocode/search?${query}`, {
    cache: "no-store",
    signal: AbortSignal.timeout(8_000),
  });
  if (!response.ok) {
    throw new Error("The address service could not complete this search.");
  }
  const payload = (await response.json()) as GeoapifyResponse;
  const result = payload.features?.[0];
  const [longitude, latitude] = result?.geometry?.coordinates ?? [];
  if (typeof latitude !== "number" || typeof longitude !== "number" || !Number.isFinite(latitude) || !Number.isFinite(longitude) || !result?.properties?.formatted) {
    return null;
  }
  return { latitude, longitude, label: result.properties.formatted };
}
