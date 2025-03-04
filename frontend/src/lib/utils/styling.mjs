
/**
 * Check whether the viewport width is greater than or equal to a given TailwindCSS breakpoint
 *
 * @export
 * @param {'sm' | 'md' | 'lg' | 'xl' | '2xl'} size  - The Tailwind breakpoint to compare
 * @returns {boolean} True if the viewport width is greater than or equal to the breakpoint
 */
export function screenGreaterThan(size = 'md') {
  const mdBreakpoint = getComputedStyle(document.documentElement).getPropertyValue(`--tw-screen-${size}`).trim();

  // Validate the retrieved breakpoint
  if (!mdBreakpoint) {
    console.warn(`Tailwind breakpoint "${size}" not found.`);
    return false;
  }
  return window.matchMedia(`(min-width: ${mdBreakpoint})`).matches;
}
