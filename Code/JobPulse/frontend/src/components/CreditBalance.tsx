"use client";

import { useState, useEffect } from "react";
import { creditsApi } from "@/lib/api";
import { Wallet, Plus } from "lucide-react";

export function CreditBalance() {
  const [balance, setBalance] = useState<{ subscription_credits: number; addon_credits: number; total_credits: number } | null>(null);

  useEffect(() => {
    creditsApi.getBalance().then((res) => setBalance(res.data)).catch(() => {});
  }, []);

  if (!balance) return null;

  return (
    <div className="card flex items-center justify-between">
      <div className="flex items-center gap-4">
        <div className="bg-primary-100 p-3 rounded-lg">
          <Wallet className="w-6 h-6 text-primary-600" />
        </div>
        <div>
          <p className="text-sm text-gray-500">Available Credits</p>
          <p className="text-2xl font-bold text-gray-900">{balance.total_credits}</p>
        </div>
      </div>
      <div className="flex gap-4 text-sm">
        <div className="text-right">
          <p className="text-gray-500">Subscription</p>
          <p className="font-medium">{balance.subscription_credits}</p>
        </div>
        <div className="text-right">
          <p className="text-gray-500">Add-on</p>
          <p className="font-medium">{balance.addon_credits}</p>
        </div>
      </div>
      <button className="btn-primary flex items-center gap-2">
        <Plus className="w-4 h-4" />
        Buy Credits
      </button>
    </div>
  );
}
