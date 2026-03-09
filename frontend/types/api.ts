export interface Profile {
  id: number;
  full_name: string;
  title: string | null;
  bio: string | null;
  email: string | null;
  location: string | null;
  avatar_filename: string | null;
  resume_filename: string | null;
  social_links: SocialLink[];
  skills: Skill[];
  experiences: Experience[];
}

export interface SocialLink {
  id: number;
  platform: string;
  url: string;
}

export interface Project {
  id: number;
  title: string;
  slug: string;
  description: string | null;
  demo_url: string | null;
  repository_url: string | null;
  category: ProjectCategory | null;
  tags: Tag[] | null;
  published: boolean;
  created_at: string;
  updated_at: string;
}

export interface ProjectCategory {
  id: number;
  name: string;
  slug: string;
}

export interface Skill {
  id: number;
  name: string;
  level: number | null;
  category: string | null;
}

export interface Experience {
  id: number;
  company: string;
  position: string;
  location: string | null;
  description: string | null;
  start_date: string;
  end_date: string | null;
}

export interface Education {
  id: number;
  school: string;
  degree: string;
  field: string | null;
  start_date: string;
  end_date: string | null;
  is_alternance: boolean;
}

export interface ContactMessage {
  id: number;
  name: string;
  email: string;
  subject: string;
  message: string;
  created_at: string;
}

export interface Appointment {
  id: number;
  name: string;
  email: string;
  message: string | null;
  status: "pending" | "confirmed" | "cancelled";
  created_at: string;
}

export interface Tag {
  id: number;
  name: string;
}
