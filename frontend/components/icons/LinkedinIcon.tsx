import Image from "next/image";

export default function LinkedinIcon({
  size,
  className,
}: {
  size: number;
  className?: string;
}) {
  return (
    <Image
      src="/icons/linkedin.png"
      alt="Linkedin"
      width={size}
      height={size}
      className={className}
    />
  );
}
