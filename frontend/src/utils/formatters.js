export function formatMeetingId(meetingId) {
  // If meeting ID follows format: meetingId_user_XXXXX_01
  if (meetingId && meetingId.includes('_')) {
    const parts = meetingId.split('_');
    // Get the last part (the number)
    const meetingNumber = parts[parts.length - 1];
    return `Meeting #${meetingNumber}`;
  }
  return 'Meeting';
}

export function truncateText(text, maxLength = 100) {
  if (!text) return '';
  return text.length > maxLength ? `${text.substring(0, maxLength)}...` : text;
}

export function formatDateRelative(dateString) {
  const date = new Date(dateString);
  const now = new Date();
  
  // Get the difference in days
  const diffTime = Math.abs(now - date);
  const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
  
  if (diffDays === 0) {
    return 'Today';
  } else if (diffDays === 1) {
    return date > now ? 'Tomorrow' : 'Yesterday';
  } else if (diffDays < 7) {
    return date.toLocaleDateString(undefined, { weekday: 'long' });
  } else {
    return date.toLocaleDateString();
  }
}