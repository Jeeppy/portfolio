import { SiGithub } from "@icons-pack/react-simple-icons";
import LinkedinIcon from "./LinkedinIcon";
import { ExternalLink } from "lucide-react";

export default function PlatformIcon({
  platform,
  size,
  className,
}: {
  platform: string;
  size: number;
  className?: string;
}) {
  if (platform.includes("github")) {
    return <SiGithub size={size} className={className} />;
  } else if (platform.includes("linkedin")) {
    return <LinkedinIcon size={size} className={className} />;
  } else {
    return <ExternalLink size={size} className={className} />;
  }
}
