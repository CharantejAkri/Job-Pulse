"use client";

import { useState } from "react";
import { useSupabase } from "@/hooks/useSupabase";
import { Navbar } from "@/components/Navbar";
import { SearchForm } from "@/components/SearchForm";
import { CreditBalance } from "@/components/CreditBalance";
import { SearchHistory } from "@/components/SearchHistory";
import { DownloadHistory } from "@/components/DownloadHistory";

export default function Home() {
  const { session, loading } = useSupabase();
  const [activeTab, setActiveTab] = useState<"search" | "history" | "downloads">("search");

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (!session) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-primary-50 to-accent-50">
        <Navbar />
        <main className="max-w-7xl mx-auto px-4 py-20">
          <div className="text-center">
            <h1 className="text-5xl font-bold text-gray-900 mb-6">
              Find Jobs. Get HR Contacts. <span className="text-primary-600">Get Hired.</span>
            </h1>
            <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
              India's smartest job lead extraction tool. Search LinkedIn, Naukri, and Indeed with AI-powered HR contact discovery and match scoring.
            </p>
            <div className="flex gap-4 justify-center">
              <a href="/login" className="btn-primary text-lg px-8 py-3">
                Get Started Free
              </a>
              <a href="#pricing" className="btn-secondary text-lg px-8 py-3">
                View Pricing
              </a>
            </div>
          </div>

          <div id="pricing" className="mt-20 grid md:grid-cols-3 gap-8">
            <PricingCard
              name="Freemium"
              price="₹0"
              credits="5"
              features={["Basic search", "Indeed only", "No HR leads"]}
              cta="Start Free"
            />
            <PricingCard
              name="Pro Hunter"
              price="₹1,499"
              credits="500"
              features={["All sites", "HR Contact Info", "AI Match %", "Excel Export"]}
              popular
              cta="Go Pro"
            />
            <PricingCard
              name="Agency"
              price="₹4,999"
              credits="2,500"
              features={["Team access", "Priority scraping", "API export", "GST Invoice"]}
              cta="Contact Sales"
            />
          </div>
        </main>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <main className="max-w-7xl mx-auto px-4 py-8">
        <div className="mb-8">
          <CreditBalance />
        </div>

        <div className="flex gap-4 mb-6 border-b border-gray-200">
          <TabButton label="New Search" active={activeTab === "search"} onClick={() => setActiveTab("search")} />
          <TabButton label="Search History" active={activeTab === "history"} onClick={() => setActiveTab("history")} />
          <TabButton label="Downloads" active={activeTab === "downloads"} onClick={() => setActiveTab("downloads")} />
        </div>

        {activeTab === "search" && <SearchForm />}
        {activeTab === "history" && <SearchHistory />}
        {activeTab === "downloads" && <DownloadHistory />}
      </main>
    </div>
  );
}

function PricingCard({ name, price, credits, features, popular, cta }: {
  name: string;
  price: string;
  credits: string;
  features: string[];
  popular?: boolean;
  cta: string;
}) {
  return (
    <div className={`card ${popular ? "ring-2 ring-primary-500 relative" : ""}`}>
      {popular && (
        <span className="absolute -top-3 left-1/2 -translate-x-1/2 bg-primary-600 text-white text-sm px-4 py-1 rounded-full">
          Most Popular
        </span>
      )}
      <h3 className="text-xl font-bold text-gray-900">{name}</h3>
      <div className="mt-4">
        <span className="text-4xl font-bold text-gray-900">{price}</span>
        <span className="text-gray-500">/month</span>
      </div>
      <p className="mt-2 text-primary-600 font-medium">{credits} credits/month</p>
      <ul className="mt-6 space-y-3">
        {features.map((feature, i) => (
          <li key={i} className="flex items-center text-gray-600">
            <svg className="w-5 h-5 text-green-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
            {feature}
          </li>
        ))}
      </ul>
      <button className={`w-full mt-8 py-3 rounded-lg font-medium ${popular ? "btn-primary" : "btn-secondary"}`}>
        {cta}
      </button>
    </div>
  );
}

function TabButton({ label, active, onClick }: { label: string; active: boolean; onClick: () => void }) {
  return (
    <button
      onClick={onClick}
      className={`px-4 py-3 font-medium transition-colors ${
        active
          ? "text-primary-600 border-b-2 border-primary-600"
          : "text-gray-500 hover:text-gray-700"
      }`}
    >
      {label}
    </button>
  );
}
