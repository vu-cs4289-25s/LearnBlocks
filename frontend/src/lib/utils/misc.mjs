export function chunkArray(arr, chunks) {
  const newCourses = [[]];
  arr.forEach((course, i) => {
    if ((i + 1) % chunks === 0) newCourses.push([]);
    newCourses.at(-1).push(course);
  });
  return newCourses;
}
