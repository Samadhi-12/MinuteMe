import { useState, useEffect } from "react";
import { getAgenda } from "../api";

function Agenda() {
	const [agenda, setAgenda] = useState(null);

	useEffect(() => {
		async function fetchAgenda() {
			const data = await getAgenda();
			setAgenda(data);
		}
		fetchAgenda();
	}, []);

	return (
		<div>
			<h2>Agenda</h2>
			{agenda ? (
				<ul>
					{agenda.agenda.map((item, idx) => (
						<li key={idx}>
							{item.topic} - {item.priority} ({item.time_allocated})
						</li>
					))}
				</ul>
			) : (
				<p>Loading agenda...</p>
			)}
		</div>
	);
}

export default Agenda;
