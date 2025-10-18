import { createClient } from '@supabase/supabase-js'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL || 'https://xubkhjcyqnoyvpqlfnjm.supabase.co'
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh1YmtoamN5cW5veXZwcWxmbmptIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjA2OTcwMDgsImV4cCI6MjA3NjI3MzAwOH0.16Ex-yxI8gihMPPOvmpF1urFgfot9rcHTVxJ8k0yG7Q'

export const supabase = createClient(supabaseUrl, supabaseAnonKey)
