export type GeocodedAddress = {
  latitude: number;
  longitude: number;
  label: string;
};

export type NearbySchool = {
  address: string;
  distanceKm: number;
  grades: string[];
  name: string;
  schoolUnitCode: string;
};

export type NearbySearchResult = {
  address: GeocodedAddress;
  schools: NearbySchool[];
};

export type DiscoveryResponse = {
  error?: string;
  location?: GeocodedAddress;
  schools?: NearbySchool[];
  warning?: string;
};
