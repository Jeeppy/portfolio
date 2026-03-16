import { Experience, Profile } from "@/types/api";
import { SiPython } from "@icons-pack/react-simple-icons";

export default function TerminalMockup({
  profile,
  experiences,
}: {
  profile: Profile;
  experiences: Experience[];
}) {
  return (
    <div className="w-full flex-1">
      <div className="overflow-hidden rounded-xl bg-gray-900 shadow-2xl">
        <div className="flex items-center gap-2 bg-gray-800 px-4 py-3">
          <span className="h-3 w-3 rounded-full bg-red-500" />
          <span className="h-3 w-3 rounded-full bg-yellow-500" />
          <span className="h-3 w-3 rounded-full bg-green-500" />
          <span className="ml-auto flex items-center gap-2 text-gray-400">
            <SiPython size={14} />
            <span className="text-xs">developer.py</span>
          </span>
        </div>
        <div className="p-6 font-mono text-sm leading-7">
          <p>
            <span className="text-blue-300">developer: </span>
            <span className="text-purple-300">dict[str, Any]</span>
            <span className="text-white"> =</span>
            <span className="text-white">{" {"}</span>
          </p>
          <p className="pl-6">
            <span className="text-green-300">
              {'"'}full_name{'"'}
            </span>
            <span className="text-white">: </span>
            <span className="text-yellow-300">
              {'"'}
              {profile.full_name}
              {'"'}
            </span>
            <span className="text-white">,</span>
          </p>
          <p className="pl-6">
            <span className="text-green-300">
              {'"'}title{'"'}
            </span>
            <span className="text-white">: </span>
            <span className="text-yellow-300">
              {'"'}
              {profile.title}
              {'"'}
            </span>
            <span className="text-white">,</span>
          </p>
          <p className="pl-6">
            <span className="text-green-300">
              {'"'}location{'"'}
            </span>
            <span className="text-white">: </span>
            <span className="text-yellow-300">
              {'"'}
              {profile.location}
              {'"'}
            </span>
            <span className="text-white">,</span>
          </p>
          <p className="pl-6">
            <span className="text-green-300">
              {'"'}available{'"'}
            </span>
            <span className="text-white">: </span>
            <span className="text-orange-300">True</span>
            <span className="text-white">,</span>
          </p>
          <p className="pl-6">
            <span className="text-green-300">
              {'"'}experiences{'"'}
            </span>
            <span className="text-white">: [</span>
          </p>
          {experiences.slice(0, 3).map((exp) => (
            <p key={exp.id} className="pl-12">
              <span className="text-white">(</span>
              <span className="text-yellow-300">
                {'"'}
                {exp.company}
                {'"'}
              </span>
              <span className="text-white">, </span>
              <span className="text-orange-300">
                {new Date(exp.start_date).getFullYear()}
              </span>
              <span className="text-white">, </span>
              <span className="text-orange-300">
                {exp.end_date ? new Date(exp.end_date).getFullYear() : "None"}
              </span>
              <span className="text-white">),</span>
            </p>
          ))}
          <p className="pl-6">
            <span className="text-white">],</span>
          </p>
          <p className="text-white">{"}"}</p>
        </div>
      </div>
    </div>
  );
}
