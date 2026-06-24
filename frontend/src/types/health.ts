export type HealthResponse = {
  status: string;
  service: string;
  version: string;
  phase: string;
  mvp_countries: string[];
  mvp_sectors: string[];
};
