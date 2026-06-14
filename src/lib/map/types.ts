export interface MapPin {
	slug: string;
	id: string;
	title: string;
	time: string;
	lat: number;
	lon: number;
	region: string;
	// Short preview shown on hover (first ~140 chars of narrative)
	preview: string;
	// Verdict snippet for the popup
	verdict: string;
	// Number of telemetry points (shown in the popup as a credibility marker)
	telemetryCount: number;
}
