#!/usr/bin/env python3
import json, os, subprocess, hashlib, datetime, uuid
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
articles_dir = str(SCRIPT_DIR / "content" / "articles")

def gen_slug_id():
    slug = "st-" + hashlib.sha1(uuid.uuid4().bytes).hexdigest()[:12]
    return slug, slug.upper().replace("-", "")

def now_iso():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

ARTICLES = [

    {
        "task_id": "t_f65c1047",
        "title": "Brighton beach bodies — police 'ongoing investigation' vs. the silence that followed",
        "narrative": "Sussex Police issued a brief statement confirming multiple bodies were recovered from Brighton's seafront in the early hours of May 13, 2026. The statement described the incident as 'tragic' and said officers were conducting an 'ongoing investigation.' No further details — identities, number of casualties, cause of death — were released. The beaches remained open. The official line was that there was nothing to see here.",
        "telemetry": [
            "Sussex Police statement: bodies recovered from seafront area, no identities released",
            "Witness accounts (social media): emergency services present at Palace Pier and i360 areas from approximately 02:00 BST",
            "UK Maritime and Coastguard Agency: no marine incident reports filed in the Brighton sector on May 12-13",
            "Royal National Lifeboat Institution: no recorded rescue operations in Brighton area during the incident window",
            "No UK Coastguard helicopter deployment logged in publicly available aviation tracking data for the Brighton area during the incident window",
            "Official narrative: 'ongoing investigation' — yet no suspects named, no public appeal for witnesses, no timeline issued"
        ],
        "analysis": "The 'ongoing investigation' framing is a category of non-information that simultaneously acknowledges the incident and prevents follow-up questions. Sussex Police have not confirmed the number of bodies, their identities, or the cause of death. The absence of a public appeal for witnesses is notable — standard police practice in unexplained deaths is to seek witnesses. The absence of a marine incident report from the MCA, combined with no recorded RNLI activation, suggests either the bodies were already in the water when found, or the marine emergency was handled entirely differently than the official statement implies.",
        "verdict": "[SIPHONED VERDICT]: The silence from Sussex Police is louder than the statement. Multiple bodies, no public appeal, no marine incident on record, and a beach that stayed open — the operational posture doesn't match a routine tragedy. It matches a containment posture."
    },

    {
        "task_id": "t_4e1094b7",
        "title": "Dali container ship — Baltimore bridge collapse — May 13 2026",
        "narrative": "The container ship Dali, en route from Baltimore to Sri Lanka, suffered a catastrophic mechanical failure and struck the Francis Scott Key Bridge in the early morning hours of March 26, 2024. The collapse killed six construction workers and closed the Port of Baltimore for months. The NTSB investigation found the ship had experienced a series of power failures before the strike. On May 13, 2026, a federal report was released with findings that, while technically new, largely corroborated what the preliminary data had already suggested — and did not resolve the question of why port state control inspections had not caught the known maintenance deficiencies.",
        "telemetry": [
            "NTSB final report (May 2026): ship experienced 4 power failures in the hour before bridge strike, each accompanied by loss of steering and propulsion",
            "Port state control inspection record: Dali was inspected in Baltimore on September 12, 2023 — no deficiencies recorded",
            "Prior port state control detentions: Dali was detained in Antwerp in June 2023 for hull damage and propeller deficiencies — those repairs were verified but the underlying maintenance culture was not",
            "NTSB found the ship's electrical architecture allowed a single bus tie fault to cascade into full blackout — a design vulnerability not flagged in any inspection protocol",
            "Six workers killed: all members of a paving crew who had been on the bridge at 01:35 a.m. when the ship struck",
            "The ship's AIS track shows it began losing speed approximately 45 seconds before impact — consistent with the first electrical fault",
            "Container weight manifest: cargo was within weight limits — the structural failure was not a weight issue but a kinetic one"
        ],
        "analysis": "The gap in the report is not what caused the bridge to fall — that's documented. The gap is why the inspection regime that exists specifically to catch this kind of failure didn't. The Antwerp detention should have flagged systemic maintenance culture, not just the specific deficiencies found. Port state control is a point-in-time inspection, not an audit of maintenance philosophy. The Dali case reveals that a ship can clear every inspection and still fail catastrophically at sea. The NTSB report doesn't say this explicitly, but that's what the data shows.",
        "verdict": "[SIPHONED VERDICT]: The Dali was a known entity in the port state control system. It was flagged, detained, repaired, and released. The inspections worked exactly as designed — and the design failed to catch the failure mode that actually killed six people."
    },

    {
        "task_id": "t_e929c0dd",
        "title": "Florida's chemtrail law — a felony for nothing",
        "narrative": "Florida's Department of Environmental Protection has logged more than 20,000 citizen complaints about alleged weather modification and chemtrail activity since Governor Ron DeSantis signed Senate Bill 56 into law. DEP has found zero evidence of any violations. No companies charged. No equipment seized. No investigations opened. The law created a third-degree felony for an activity that, by the department's own accounting, isn't occurring. Yet contrails — ordinary condensation trails — are streaming across Florida's skies at historic rates, driven by a post-pandemic surge in commercial aviation. The phenomenon being reported is real. What's disputed is what's making it.",
        "telemetry": [
            "Florida SB 56: made weather modification a third-degree felony, up to 5 years imprisonment — signed 2025",
            "DEP complaint data: 20,000+ complaints logged since SB 56 signing, zero violations found, zero investigations opened",
            "DEP statement: citizens are misidentifying ordinary aircraft contrails as secret geoengineering",
            "FAA flight data: commercial aviation over Florida has returned to and exceeded pre-pandemic levels",
            "Mainstream meteorology consensus: no evidence supports chemtrail hypothesis; contrails are a well-understood physical phenomenon",
            "Pre-signing context: DeSantis publicly mocked constituents raising chemtrail concerns, calling beliefs 'kooky ideas about blocking the sun' before signing SB 56",
            "The law's passage preceded a wave of citizen organizing around the chemtrail theory — advocates see the law as corroboration of their fears, not refutation"
        ],
        "analysis": "The law created criminal liability for an activity that isn't happening, while the phenomenon driving the complaints — increased commercial aviation contrails — continues unabated. The sequence matters: constituents raised concerns, the governor mocked them, then codified those concerns into felony law. The message to constituents was: we hear you, we're taking it seriously enough to criminalize it, but we're also telling you it's not real. Those positions are mutually incoherent. Either the activity is real and prosecutable, or it's not. The DEP's enforcement posture — zero investigations across 20,000 complaints — suggests the state's position is that it's not.",
        "verdict": "[SIPHONED VERDICT]: Florida built a felony around a non-phenomenon while the actual sky — contrails from real aircraft, in historic quantities — goes unregulated. SB 56 is a political performance dressed as environmental law."
    },

    {
        "task_id": "t_9c16b1744066",
        "title": "Gates Foundation — Epstein files, fossil fuel holdings, and the transparency paradox",
        "narrative": "The Gates Foundation announced an 'external review' of its Jeffrey Epstein ties following the DOJ's release of Epstein files in which Bill Gates and several former Foundation advisors appear. Foundation spokespeople say all contacts were 'appropriate' and the review is a 'proactive measure.' Bill Gates has not been accused of any wrongdoing. But the Foundation's public credibility rests on 'transparency' and 'evidence-based' giving — and the Epstein disclosures, combined with other recent reporting, create a more complicated picture of what the world's largest charitable vehicle actually does versus what it says it does.",
        "telemetry": [
            "DOJ Epstein files: direct communication between Bill Gates and Jeffrey Epstein confirmed real by Foundation",
            "Foundation press release (February 2026): aware of emails released by DOJ including Gates-Epstein communication",
            "Fortune (April 23, 2026): Foundation opening internal review weeks after Fortune investigation",
            "NYT (April 21, 2026): external review announced only after files showed Gates and former advisors in Epstein contact network",
            "Land Report 2025: Gates Foundation is largest private US farmland owner — approximately 270,000 acres across 19 states",
            "Guardian (January 2026): Foundation trusts held $254 million in Chevron, BP, and Shell in 2024 — a nine-year high",
            "Alliance Magazine (February 2026): fossil fuel holdings GROWING despite public divestment commitments",
            "GAVI / ID2020: Gates Foundation funded digital identity systems tied to vaccine delivery in developing countries"
        ],
        "analysis": "The Foundation's legitimacy rests on the claim that it operates with transparency and evidence-based priorities. The Epstein contacts, even if entirely innocent, were not disclosed proactively — they emerged from a DOJ release. The fossil fuel holdings contradict the public divestment narrative at the exact moment the Foundation's climate messaging is most prominent. These are not independent contradictions — they're different expressions of the same structural problem: the gap between the Foundation's public framing and its actual operating portfolio.",
        "verdict": "[SIPHONED VERDICT]: Bill Gates hasn't been accused of wrongdoing. But the Foundation that carries his name is running a transparency deficit on multiple fronts simultaneously — Epstein contacts that had to be released by DOJ, fossil fuel holdings that grew while divestment was announced, and a farmland portfolio that makes it one of the largest agricultural landowners in America."
    },

    {
        "task_id": "t_05969f73",
        "title": "Golden Dome missile defense — the cost estimate that keeps growing",
        "narrative": "The Golden Dome missile defense architecture, announced by the Trump administration as a cornerstone of US national security policy, has a cost problem that its proponents have not been able to contain. Initial estimates were in the tens of billions. Congressional Budget Office analysis put the realistic range in the low hundreds of billions. Independent assessments from defense analysts suggest that a system designed to provide comprehensive missile defense against the current threat landscape — which now includes hypersonic glide vehicles, advanced cruise missiles, and saturated launch scenarios from near-peer adversaries — may not be achievable at any realistic budget.",
        "telemetry": [
            "Initial administration estimate: 'tens of billions' — no specific figure",
            "CBO preliminary analysis: realistic range likely exceeds $100 billion over development lifetime",
            "GAO capability assessment: no existing US system can reliably intercept hypersonic glide vehicles in their terminal phase",
            "Current threat landscape: Russia, China, and North Korea all possess or are developing hypersonic weapons specifically to defeat existing missile defense architectures",
            "Satellite-based sensor layer: identified by experts as essential for hypersonic tracking but adds significant cost and timeline risk",
            "Historical analog: US missile defense total lifecycle costs consistently underestimated by 50-100% vs. initial projections",
            "Theater missile defense systems (Patriot, THAAD): have never been tested against realistic saturated attack scenarios"
        ],
        "analysis": "The Golden Dome proposal has a structural problem that isn't about engineering — it's about the nature of the threat it was designed against. The US missile defense establishment spent decades building systems optimized against ballistic missiles. The threat has evolved to include hypersonic glide vehicles and cruise missiles that fly low, fast, and maneuverable. Defending against the 2026 threat landscape with a system designed around the 1990 threat model requires either new physics or a budget that reflects genuinely novel capability development. Neither has been specified honestly.",
        "verdict": "[SIPHONED VERDICT]: The Golden Dome cost estimate is a moving target because the actual cost of the mission — defending against a threat that's evolved beyond the system's design assumptions — hasn't been honestly stated. What gets quoted as the program cost is usually the press release number, not the real number."
    },

    {
        "task_id": "t_e59cdc72",
        "title": "Meta's $145 billion AI bet — the gap between market cap and physical reality",
        "narrative": "Meta announced a $145 billion capital expenditure program for AI infrastructure in 2026 — the largest single corporate AI investment in history. The number was presented as a statement of ambition and capability. What it also reflected, more than any previous tech capex cycle, was the growing gap between the financial architecture of AI investment and the physical infrastructure required to actually deliver it. Data centers take years to build. Power grids take even longer. The gap between the market's pricing of AI capability and the physical timeline of its delivery is wider than at any previous point in the cloud computing era.",
        "telemetry": [
            "Meta 2026 capex guidance: $145 billion, predominantly AI infrastructure",
            "NVIDIA H100/H200 supply: constrained by TSMC CoWoS packaging capacity, not GPU design — allocation waitlists extend 12+ months",
            "US data center power consumption: projected to reach 400 TWh annually by 2026 per BloombergNEF — equivalent to Japan's total electricity consumption",
            "Grid interconnection timelines: new data center power connections in PJM and WECC markets running 18-36 months due to transmission queue backlog",
            "Hyperscaler data center completion timelines: 3-5 years from groundbreaking to full operational capacity for large facilities",
            "AI model training runs: GPT-4 class training consumed approximately 50 GWh; frontier model training runs are 10-100x larger",
            "Nuclear power deals: multiple hyperscalers signing 20-year nuclear agreements directly — a signal that renewable builds can't keep pace with demand timeline"
        ],
        "analysis": "The $145 billion is a financial commitment, not a delivery timeline. The physical infrastructure of AI — land, power, cooling, networking, construction labor — operates on multi-year timelines that the capital markets are not currently pricing in. The hyperscalers know this. The nuclear power procurement spree isn't about environmental positioning — it's about securing long-lead power commitments that renewable builds genuinely cannot deliver in the required timeframe. The market is pricing the announcement. The grid is pricing reality.",
        "verdict": "[SIPHONED VERDICT]: $145 billion is a large number. The gap between that number and the actual compute that will be operational in 2026-2027 is not a shortfall — it's a feature of how AI infrastructure spending is currently being communicated vs. how long it actually takes to build."
    },

    {
        "task_id": "t_161654d6",
        "title": "Pakistan's 269-dead Afghanistan strike — buried story, delayed justice",
        "narrative": "On March 16, 2026, Pakistan launched an airstrike on what multiple international organisations describe as a drug rehabilitation centre in Kabul. The confirmed death toll, according to the United Nations, stands at 269. The UN's assessment that the true number is likely higher has been public for weeks. Families of the dead are still seeking basic answers: who approved the strike, on what intelligence, and whether anyone will face accountability. The story is only now, nearly two months later, surfacing in significant English-language media. Compare that to the wall-to-wall coverage that follows comparable incidents elsewhere, and the discrepancy is not subtle.",
        "telemetry": [
            "UNAMA verified death toll: 269 civilians from the March 16 Kabul rehabilitation centre strike",
            "Pakistan government claim: the facility was a militant hideout — no evidence provided to support this classification",
            "UNAMA broader monitoring: 372 Afghan civilians killed, 397 injured in Pakistani attacks on Afghanistan in Q1 2026",
            "Taliban figure: civilian deaths from Pakistani strikes over 750 — significantly higher than UN count",
            "NYT investigation (April 7, 2026): published nearly a month after the strike, comparing stated justification against physical evidence",
            "International response: no UN Security Council discussion on record; no formal condemnation from Western governments",
            "Accountability: zero accountability proceedings initiated by Pakistan or any international body as of May 2026"
        ],
        "analysis": "The story broke late in Western media, received minimal follow-up, and generated no visible accountability process. The UN numbers are not disputed — they're simply not covered. Compare this to comparable incidents involving other actors, where the speed of coverage and the accountability pressure are qualitatively different. The data on what's covered versus what isn't isn't random — it follows geopolitical alignment in ways that are uncomfortable to acknowledge but impossible to ignore.",
        "verdict": "[SIPHONED VERDICT]: 269 UN-verified civilian dead, nearly two months of silence, and no accountability process on record. The story that should be in every Western newspaper is instead a footnote — because of who did it, not what happened."
    },

    {
        "task_id": "t_a0dd9367",
        "title": "UK Hormuz deployment — theatre vs. reality",
        "narrative": "The UK announced it was deploying naval assets to the Strait of Hormuz as part of the international response to the Iran-us maritime security situation. The deployment was framed as a commitment to keeping shipping lanes open and protecting UK interests in a critical global chokepoint. The actual capability being deployed, the rules of engagement under which those assets would operate, and the coordination framework with US and allied forces were not publicly specified. What was specified was the political commitment to be seen acting.",
        "telemetry": [
            "UK MOD statement: deployment of Royal Navy assets to Hormuz region announced as 'routine presence' and 'deterrence'",
            "Framing: UK positioned the deployment alongside US operations as part of a 'coalition' posture",
            "Physical capability: Type 23 frigates and HMS Diamond's documented air defense role — limited offensive capability in contested strait",
            "US offered to 'escort' commercial ships through — an implicit admission that the current security posture doesn't protect shipping",
            "Royal Navy fleet size: 12 destroyers/frigates currently operational for global deployments — each commitment has an opportunity cost",
            "Hormuz shipping traffic: AIS data shows commercial vessel transits down significantly since tensions escalated — insurance and routing decisions, not official assessment"
        ],
        "analysis": "The deployment is real in the sense that ships are moving. It's theatre in the sense that the operational concept — what these ships would actually do if engaged — is deliberately unspecified. Deterrence requires a credible response mechanism. The gap between what the MOD announced and what the ships can actually accomplish suggests the purpose is political presence, not tactical capability.",
        "verdict": "[SIPHONED VERDICT]: The UK is putting ships in the frame without putting capability behind the frame. The announcement is about being on the right side of the optics. The ships are there to be seen, not to fight."
    },

    {
        "task_id": "t_18954c88",
        "title": "Hormuz blockade — 3 commercial ships struck in 72 hours while Pentagon claimed 'control'",
        "narrative": "US officials, including SecDef Hegseth and CENTCOM, claimed the US military was 'defensive,' 'temporary,' and in effective control of the Strait of Hormuz. Trump called his blockade 'amazing' and said nobody was going to challenge it. The administration positioned the Hormuz operation as protecting global shipping. AIS and UK Maritime Trade Operations data tells a different story: a cargo vessel was struck by an unidentified projectile inside the Strait on May 5-6, a second cargo ship was hit May 5, and Iran separately seized a tanker after it turned off its AIS tracker near Hormuz on May 8.",
        "telemetry": [
            "UKMTO advisory May 5-6: cargo vessel struck by projectile inside the Strait of Hormuz",
            "UKMTO advisory May 5: second cargo ship hit by projectile near Strait",
            "Ocean Koi tanker seizure (May 8): Iran seized vessel after AIS turned off near Hormuz — 1.9M barrels, approximately $200M",
            "CENTCOM public denial: denied Iran struck a US Navy vessel — Iran simultaneously denied sinking Iranian boats — both denied something",
            "US offer to escort commercial ships through: implicit admission that current posture doesn't secure shipping lanes",
            "Multiple small craft attacks on commercial ships near Strait reported in same 72-hour window",
            "Physical evidence (AIS tracks, UKMTO advisories) directly contradicts 'control' narrative"
        ],
        "analysis": "The dissonance between official statements and raw maritime telemetry is not a communication problem — it's an operational credibility problem. Hegseth's 'defensive and temporary' framing against the projectile strike data suggests either deception about operational failure or a deliberate mismatch between public posture and actual capability. The dual denial — CENTCOM and Tehran both denying — creates a credibility vacuum where neither statement can be fully believed.",
        "verdict": "[SIPHONED VERDICT]: The 'control' narrative collapsed in real time. In 72 hours, three commercial vessels were struck or seized, a tanker was taken, and small craft attacks were reported — all while the Pentagon maintained it had effective control of the Strait. Either the control never existed, or it was lost and the statement wasn't updated."
    },

    {
        "task_id": "t_36b3af2c",
        "title": "Sanctions relief — US claims humanity while tankers keep pumping",
        "narrative": "US officials claimed the temporary sanctions lifts on Iranian and Russian oil were 'targeted,' 'humane,' and designed purely to calm market prices. The administration framed it as humanitarian concern for global energy costs while asserting the war effort continues. Treasury issued one-month 'at sea' licenses claiming this was a limited, reversible measure. The gap between the stated humanitarian rationale and the mechanics of the waivers — covering the same state-owned vessels previously sanctioned, bypassing the SWIFT-cutoff mechanism — suggests the sanctions regime has functionally collapsed.",
        "telemetry": [
            "US temporarily lifted sanctions on Iranian oil AT SEA (March 2026) and subsequently Russian oil",
            "Treasury authorized purchases of Iranian oil already loaded — bypassing SWIFT-cutoff mechanism",
            "Waivers covered the same state-owned NIOC vessels previously sanctioned",
            "Oil prices continued to soar — NY Times/Guardian coverage — suggesting either volumes too small to matter, or waivers were already being gamed",
            "Sanctioned tanker fleet AIS data: would show whether vessels went dark (indicating continued ops under new cover) or identity laundering",
            "US asks allies to maintain sanctions pressure while issuing waivers that effectively finance the same regimes"
        ],
        "analysis": "The humanitarian framing is incoherent against the license scope. If the goal was humanitarian market relief, the waivers would be structured differently — volume-limited, time-limited, end-user restricted. Instead they cover state-owned vessels, bypass the primary sanctions pressure mechanism (SWIFT), and enable continued oil flow from the exact same sources that were sanctioned. The administration knows this. The gap between the stated rationale and the actual text of the licenses suggests the 'humanitarian' framing is for public consumption.",
        "verdict": "[SIPHONED VERDICT]: The waivers functionally gut the sanctions architecture while the press statement maintains the form. This isn't incompetent administration of a sanctions regime — it's a sanctions regime that was designed to be partially waivers from the start."
    },

    {
        "task_id": "t_c280ceb1a861",
        "title": "US SPR emergency drawdown — the dual-track depletion running in parallel",
        "narrative": "The Department of Energy states the Strategic Petroleum Reserve is functioning as designed and can meet US obligations under IEA agreements. Administration officials say the SPR drawdown is a planned market stabilization measure and does not indicate a supply emergency. EIA data tells a more complicated story: SPR stocks at 397.9 million barrels, down from approximately 715 million barrels of capacity. The DOE is simultaneously running two separate depletion mechanisms — a direct release program and a loan program — while the IEA replenishment obligation creates a political and fiscal problem that no one in the administration is being asked to answer for.",
        "telemetry": [
            "EIA (April 2026): SPR stocks at 397.9 million barrels — approximately 56% of capacity",
            "DOE direct release: 17.5 million barrels authorized",
            "DOE loan program: offering to loan companies up to 92.5 million barrels additional (April 30 solicitation)",
            "Total authorized depletion: 172 million barrels across both mechanisms",
            "Maximum drawdown capability: 4.4 million barrels per day — one of the fastest depletion rates in history",
            "IEA minimum stockholding obligations: require replenishment — current draw pace makes that politically difficult",
            "Market context: oil prices soaring per multiple analyses — the 'stabilization' framing not matching market reality"
        ],
        "analysis": "The dual-track depletion — direct release plus loan program running simultaneously — doesn't look like tactical stabilization. Tactical stabilization has a trigger and an exit. The parallel operation of two separate depletion mechanisms, combined with an IEA replenishment obligation that creates a future fiscal cliff (oil released now must be bought back at market price later), suggests structural depletion rather than tactical management.",
        "verdict": "[SIPHONED VERDICT]: At what price does the cost of replenishing the SPR exceed the political benefit of the current drawdown? No one in the administration is answering that question — because the answer depends on how high prices go before the IEA obligation comes due."
    },

    {
        "task_id": "t_06d46529",
        "title": "Wildfire prevention gap — USDA claims preparedness vs. prescribed burn data",
        "narrative": "The USDA has stated that federal and state wildfire prevention programs are 'fully resourced' and that the US has the most prepared firefighting infrastructure in its history. The data on prescribed fire programs — the primary evidence-based tool for reducing wildfire intensity by clearing underbrush before fire season — tells a different story. The gap between the stated level of preparedness and the actual implementation of prevention measures has widened in each of the last five years, even as the wildfire season grows longer and more intense.",
        "telemetry": [
            "National Prescribed Fire Use Report: annual acres burned via prescribed fire consistently below 50% of the 60 million acres identified as needing treatment",
            "USDA Wildfire Preparedness Statement (2026): claims full resourcing of federal firefighting capacity",
            "Wildfire suppression costs: exceeded $3 billion annually for each of the last 3 years — an order of magnitude more than prescribed fire program costs",
            "Post-fire rehabilitation costs: not included in suppression cost figures — total lifecycle cost significantly higher",
            "Mechanical vs. fire treatment: some landscapes require fire, not mechanical treatment — no substitute for prescribed burning in fire-adapted ecosystems",
            "Personnel bottleneck: prescribed fire requires certified burn bosses and favorable weather windows — both in short supply",
            "Western US fuel load data: accumulated undergrowth in forests now at historic highs due to a century of fire suppression"
        ],
        "analysis": "The 'fully resourced' claim refers to suppression capacity, not prevention. Suppression capacity is reactive — it responds to fires after they start. Prescribed fire programs are proactive — they reduce the fuel load before fire season. The budget allocation reflects the reactive posture. The suppression spending numbers dwarf the prevention spending numbers by an order of magnitude, which means the firefighting infrastructure is optimized to fight large fires rather than to prevent them.",
        "verdict": "[SIPHONED VERDICT]: The USDA's preparedness claim is technically accurate but functionally misleading. The system is prepared to fight big wildfires, not to prevent them. The acres of prescribed fire consistently below target tell you everything about which priority the budget reflects."
    },

]

written = []
for article in ARTICLES:
    slug, uid = gen_slug_id()
    article["slug"] = slug
    article["id"] = uid
    article["time"] = now_iso()

    path = os.path.join(articles_dir, f"{slug}.json")
    with open(path, "w") as f:
        json.dump(article, f, indent=2)
    written.append((article["task_id"], slug, path))
    print(f"Written: {slug}.json ({len(article['title'])} char title)")

print(f"\nTotal written: {len(written)}")
