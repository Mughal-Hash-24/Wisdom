# Fiqh Ruling Card

## Goal
Present the complete Hanafi / Maliki / Shafi'i / Hanbali position on a fiqh question. The output is a structured legal brief — ruling first, then the full derivation from source to conclusion. The derivation is the core deliverable, not a footnote.

## Output Requirements

Follow the madhab file structure from your agent instructions exactly. All sections are mandatory:
1. **Ruling** — dominant position, clear and unambiguous. One of: permissible, impermissible, obligatory, recommended, disliked, or neutral.
2. **Usul al-Fiqh** — full derivation chain using the appropriate source branch (Quran / Sunnah / Ijma / Qiyas).
3. **Internal Dissent** — the most significant minority within this school, with the usul reason for divergence.

## Quality Signals
- Ruling is stated in the first sentence — no preamble
- The Usul al-Fiqh section shows the *how*, not just the *what*
- Every source branch appropriate to the derivation is populated
- The Usul-Level Disputes field genuinely engages with where other schools diverge — not a generic "the other schools have different views"
- Internal dissent is specific and attributed, not vague ("some scholars say...")
- Citations are marked (VERIFIED) or (UNCERTAIN) — no unmarked claims

## Anti-Patterns
- DO NOT give the ruling without the derivation
- DO NOT assert ijma without specifying which generation of scholars and approximately when
- DO NOT use a qiyas template if a direct Quran or Sunnah source is available
- DO NOT write "scholars differ" without identifying the specific methodological point of divergence
- DO NOT leave Nasikh/Mansukh blank for Quranic derivations — always state the abrogation status explicitly
- DO NOT fabricate hadith citations — if uncertain, describe the class of evidence instead
