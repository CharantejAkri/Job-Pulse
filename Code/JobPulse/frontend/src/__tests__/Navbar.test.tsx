import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import { Navbar } from "../components/Navbar";

vi.mock("@/hooks/useSupabase", () => ({
  useSupabase: vi.fn(() => ({
    session: null,
    loading: false,
    signOut: vi.fn(),
  })),
}));

describe("Navbar", () => {
  it("renders the JobPulse logo", () => {
    render(<Navbar />);
    expect(screen.getByText("JobPulse")).toBeInTheDocument();
  });

  it("shows Sign In button when not authenticated", () => {
    render(<Navbar />);
    expect(screen.getByText("Sign In")).toBeInTheDocument();
  });
});
