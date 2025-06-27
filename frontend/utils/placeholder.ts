// Placeholder for utility functions
// For example, functions for API calls, data formatting, etc.

export const formatDate = (date: Date): string => {
  return new Intl.DateTimeFormat('en-US').format(date);
};
