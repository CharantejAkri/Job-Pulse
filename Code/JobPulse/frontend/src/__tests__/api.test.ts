import { describe, it, expect } from "vitest";
import { api, setAuthToken } from "../lib/api";

describe("API Client", () => {
  it("should have correct base URL", () => {
    expect(api.defaults.baseURL).toBe(
      process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"
    );
  });

  it("should have JSON content type", () => {
    expect(api.defaults.headers["Content-Type"]).toBe("application/json");
  });

  it("should set auth token when provided", () => {
    setAuthToken("test-token");
    expect(api.defaults.headers.common["Authorization"]).toBe(
      "Bearer test-token"
    );
  });

  it("should clear auth token when null", () => {
    setAuthToken("test-token");
    setAuthToken(null);
    expect(api.defaults.headers.common["Authorization"]).toBeUndefined();
  });
});
