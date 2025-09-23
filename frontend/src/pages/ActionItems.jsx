import { useState } from "react";

function ActionItems() {
	const [actionItems, setActionItems] = useState([]);

	// Placeholder: In future, fetch action items from backend or context

	return (
		<div>
			<h2>Action Items</h2>
			{actionItems.length > 0 ? (
				<ul>
					{actionItems.map((item, idx) => (
						<li key={idx}>
							{item.task} - {item.owner} - {item.deadline}
						</li>
					))}
				</ul>
			) : (
				<p>No action items available. Generate from Dashboard.</p>
			)}
		</div>
	);
}

export default ActionItems;
