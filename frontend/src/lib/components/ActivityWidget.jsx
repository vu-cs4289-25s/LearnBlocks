import { getDaysElapsed, DAYSOFTHEWEEK } from '$lib/utils/time.mjs';


const masks = [1, 2, 4, 8, 16, 32, 64, 128];
const example = [0, 1, 0, 0, 1, 0, 0]


const combiner = [
  [254, 1],
  [252, 3],
  [248, 7],
  [240, 15],
  [224, 31],
  [192, 63],
  [128, 127],
];

/**
 * Description placeholder
 *
 * @returns {import('react/jsx-runtime').JSX.Element}
 */
export default function ActivityWidget() {
  const numArray = new Array(368).fill(1);
  const allActivityBits = new Uint8Array(numArray);
  const today = new Date();
  const daysElapsed = getDaysElapsed(today);
  console.log(daysElapsed - today.getDay());
  console.log(today);

  return (
    <div>
      <h1 className='font-bold text-xl '>Your Week</h1>
      <section className='flex flex-1 flex-row justify-evenly'>
       
      </section>
    </div>
  );
}
