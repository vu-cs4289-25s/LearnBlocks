

const MSPERDAY = 1000 * 60 * 60 * 24 

export const DAYSOFTHEWEEK = [
  'Sunday', 
  'Monday',
  'Tuesday',
  'Wednesday',
  'Thursday',
  'Friday',
  'Saturday',
]


/**
 * Returns the days that have elapsed since the beginning of start
 *
 * @export
 * @param {Date} date 
 * @param {Date | undefined} start 
 * 
 * @returns {number}
 **/
export function getDaysElapsed(date, start = new Date(date.getFullYear().toString())) {
  const unixDiff = date - start 
  const daysElapsed = Math.floor(unixDiff / MSPERDAY)
  return daysElapsed
}


