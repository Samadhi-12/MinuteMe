import { useState } from "react";

function Minutes() {
	const [minutes, setMinutes] = useState(null);

	// Placeholder: In future, fetch minutes from backend or context

	return (
		<div>
			<h2>Minutes</h2>
			{minutes ? (
				<pre>{JSON.stringify(minutes, null, 2)}</pre>
			) : (
				<p>No minutes available. Generate minutes from Dashboard.</p>
			)}
		</div>
	);
}

export default Minutes;
