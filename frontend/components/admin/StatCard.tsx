import { LucideIcon } from "lucide-react";

export default function StatCard({
  Icon,
  color,
  label,
  count,
}: {
  Icon: LucideIcon;
  color: string;
  label: string;
  count: number;
}) {
  return (
    <div className="flex items-center overflow-hidden rounded-xl bg-white shadow-md">
      <div className={`flex items-center self-stretch ${color} p-4 text-white`}>
        <Icon size={22} />
      </div>
      <div className="px-4 py-4 text-gray-700">
        <h3 className="text-xs font-medium tracking-widest text-gray-500 uppercase">
          {label}
        </h3>
        <p className="text-3xl font-bold">{count}</p>
      </div>
    </div>
  );
}
