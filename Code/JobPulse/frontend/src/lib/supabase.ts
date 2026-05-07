import { createClient } from "@supabase/supabase-js";

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;

export const supabase = createClient(supabaseUrl, supabaseAnonKey);

export type Database = {
  public: {
    Tables: {
      users: {
        Row: {
          id: string;
          email: string;
          full_name: string | null;
          role: string;
          resume_url: string | null;
          created_at: string;
        };
      };
      subscriptions: {
        Row: {
          id: string;
          user_id: string;
          status: string;
          plan_type: string;
          monthly_credits: number;
          current_period_end: string | null;
        };
      };
      credit_wallets: {
        Row: {
          id: string;
          user_id: string;
          credit_type: string;
          balance: number;
          expires_at: string | null;
        };
      };
      scrape_jobs: {
        Row: {
          id: string;
          user_id: string;
          job_title: string;
          company: string;
          location: string | null;
          salary: string | null;
          source: string;
          source_url: string;
          hr_name: string | null;
          hr_email: string | null;
          hr_email_verified: boolean;
          match_score: number | null;
          status: string;
          scraped_at: string | null;
        };
      };
      search_logs: {
        Row: {
          id: string;
          user_id: string;
          job_title: string;
          location: string | null;
          sources: string[];
          date_posted: string | null;
          created_at: string;
        };
      };
      download_history: {
        Row: {
          id: string;
          user_id: string;
          file_name: string;
          file_format: string;
          job_count: number;
          created_at: string;
          expires_at: string | null;
        };
      };
    };
  };
};
