export default function MessageBubble({ sender, role, text, mine, time, tags, relatesTo }) {
  const getTagColor = (tag) => {
    const colors = {
      'weekly-report': 'bg-blue-100 text-blue-800',
      'member-question': 'bg-green-100 text-green-800',
      'team-reply': 'bg-purple-100 text-purple-800'
    };
    return colors[tag] || 'bg-gray-100 text-gray-800';
  };

  return (
    <div className={`flex ${mine ? "justify-end" : "justify-start"} mb-3`}>
      <div className={`max-w-[70%] rounded-2xl px-4 py-3 shadow ${mine ? "bg-green-500 text-white" : "bg-white border"}`}>
        <div className="flex items-center gap-2 mb-2">
          <p className="text-xs opacity-80">{time}</p>
          <p className="text-xs font-semibold">{mine ? "Rohan" : `${sender} (${role})`}</p>
        </div>
        <p className="mt-1 leading-relaxed">{text}</p>
        
        {tags && tags.length > 0 && (
          <div className="flex flex-wrap gap-1 mt-2">
            {tags.map((tag, index) => (
              <span 
                key={index} 
                className={`text-xs px-2 py-1 rounded-full ${getTagColor(tag)}`}
              >
                {tag.replace('-', ' ')}
              </span>
            ))}
          </div>
        )}
        
        {relatesTo && (
          <div className="mt-2 pt-2 border-t border-gray-200">
            <p className="text-xs opacity-70">↩️ Reply to previous message</p>
          </div>
        )}
      </div>
    </div>
  );
}
