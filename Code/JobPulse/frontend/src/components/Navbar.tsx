"use client";

import Link from "next/link";
import { useSupabase } from "@/hooks/useSupabase";
import { Briefcase } from "lucide-react";

export function Navbar() {
  const { session, signOut } = useSupabase();

  return (
    <nav className="bg-white border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2">
          <Briefcase className="w-8 h-8 text-primary-600" />
          <span className="text-xl font-bold text-gray-900">JobPulse</span>
        </Link>

        <div className="flex items-center gap-4">
          {session ? (
            <>
              <span className="text-sm text-gray-600">{session.user.email}</span>
              <button onClick={signOut} className="btn-secondary text-sm">
                Sign Out
              </button>
            </>
          ) : (
            <Link href="/login" className="btn-primary">
              Sign In
            </Link>
          )}
        </div>
      </div>
    </nav>
  );
}
