import { getDaysElapsed } from '$lib/utils/time.mjs';
import { FireIcon } from '@heroicons/react/20/solid';

const example = {
  sunday: true,
  monday: false,
  tuesday: false,
  wednesday: true,
  thursday: false,
  friday: true,
  saturday: false,
};

/**
 * Description placeholder
 *
 * @returns {import('react/jsx-runtime').JSX.Element}
 */
export default function ActivityWidget({className}) {
  const numArray = new Array(368).fill(1);
  const allActivityBits = new Uint8Array(numArray);
  const today = new Date();
  const daysElapsed = getDaysElapsed(today);
  const daysElapsedSunday = daysElapsed - today.getDay();

  return (
    <section className={className}>
      <h1 className="text-xl font-bold">Your Activity</h1>
      <hr className="text-zinc-600" />
      <ul className="flex flex-1 flex-row justify-evenly gap-4">
        {Object.entries(example).map(([day, wasActive], key) => {
          return (
            <li key={key} className='flex flex-col items-center flex-1/7'>
              <FireIcon
                className="rounded-full bg-zinc-700 "
                color={`${wasActive ? '#ff8000' : 'gray'}`}
              />
              <h2>{day.slice(0, 2).toUpperCase()}</h2>
            </li>
          );
        })}
      </ul>
    </section>
  );
}
