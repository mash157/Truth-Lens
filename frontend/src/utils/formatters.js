/**
 * Formats a decimal probability into a clean percentage string.
 * Example: 0.9423 -> "94.2%"
 */
export const formatPercentage = (value) => {
  if (value === undefined || value === null || isNaN(value)) {
    return '0.0%';
  }
  return `${(value * 100).toFixed(1)}%`;
};

/**
 * Formats an integer count with comma separators.
 * Example: 72134 -> "72,134"
 */
export const formatNumber = (value) => {
  if (value === undefined || value === null || isNaN(value)) {
    return '0';
  }
  return value.toLocaleString();
};

/**
 * Truncates text to a maximum length with ellipses.
 */
export const truncateText = (text, maxLength = 100) => {
  if (!text) return '';
  if (text.length <= maxLength) return text;
  return `${text.slice(0, maxLength)}...`;
};
