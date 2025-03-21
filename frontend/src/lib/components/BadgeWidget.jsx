import { getDaysElapsed } from '$lib/utils/time.mjs';
import { CheckBadgeIcon } from '@heroicons/react/24/outline';

const example = [
  'badge',
  'badge',
  'badge',
  'badge',
  'badge',
  'badge',
  'badge',
  'badge',
];

/**
 * Description placeholder
 *
 * @returns {import('react/jsx-runtime').JSX.Element}
 */
export default function BadgeWidget({ className }) {
  return (
    <section className={className}>
      <h1 className="text-xl font-bold">Earned Badges</h1>
      <hr className="text-zinc-600" />
      <ul className="flex flex-1 flex-row justify-evenly gap-4">
        {example.slice(0,5).map((badge, key) => {
          return (
            <li key={key} className="flex flex-1/7 flex-col items-center">
              <CheckBadgeIcon className="rounded-full bg-zinc-700" />
            </li>
          );
        })}
      </ul>
    </section>
  );
}
