const MSPERDAY = 1000 * 60 * 60 * 24;

const DAYSOFTHEWEEK = [
  'Sunday',
  'Monday',
  'Tuesday',
  'Wednesday',
  'Thursday',
  'Friday',
  'Saturday',
];

const masks = new Uint8Array([
  0b00000001, 0b00000010, 0b00000100, 0b00001000, 0b00010000, 0b00100000,
  0b01000000, 0b10000000,
]);

const combiners = [
  new Uint8Array([0b00000001, 0b11111100]),
  new Uint8Array([0b00000011, 0b11111000]),
  new Uint8Array([0b00000111, 0b11110000]),
  new Uint8Array([0b00001111, 0b11100000]),
  new Uint8Array([0b00011111, 0b11000000]),
  new Uint8Array([0b00111111, 0b10000000]),
  new Uint8Array([0b01111111, 0b00000000]),
  new Uint8Array([0b11111110, 0b00000000]),
];

/**
 * Returns the days that have elapsed since the beginning of start
 *
 * @export
 * @param {Date} date
 * @param {Date | undefined} start
 *
 * @returns {number}
 **/
export function getDaysElapsed(
  date,
  start = new Date(date.getFullYear().toString()),
) {
  const unixDiff = date - start;
  const daysElapsed = Math.floor(unixDiff / MSPERDAY);
  return daysElapsed;
}
