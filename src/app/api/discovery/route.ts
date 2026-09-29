import { GeocodingUnavailableError, geocodeSwedishAddress } from "@/features/discovery/geoapify-geocoder";

export async function POST(request: Request) {
  let body: unknown;
  try {
    body = await request.json();
  } catch {
    return Response.json({ error: "Enter a valid address." }, { status: 400 });
  }
  const address = typeof body === "object" && body !== null && "address" in body ? body.address : undefined;
  if (typeof address !== "string" || !address.trim() || address.length > 200) {
    return Response.json({ error: "Enter a valid address." }, { status: 400 });
  }

  try {
    const location = await geocodeSwedishAddress(address.trim());
    if (!location) {
      return Response.json({ error: "We could not find that Swedish address. Check the spelling and try again." }, { status: 404 });
    }
    return Response.json({ location, schools: [], warning: "The national school-directory connector is the next implementation step." });
  } catch (error) {
    if (error instanceof GeocodingUnavailableError) {
      return Response.json({ error: "Address search has not been configured in this environment." }, { status: 503 });
    }
    return Response.json({ error: "The address service is temporarily unavailable. Try again shortly." }, { status: 502 });
  }
}
