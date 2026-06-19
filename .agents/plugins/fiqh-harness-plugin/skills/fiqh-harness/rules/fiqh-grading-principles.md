# Fiqh Grading Principles & Qualitative Guidelines

This document defines the criteria used by the `fiqh-grader` agent to assess the intellectual quality, legal rigor, and citation authenticity of generated Fiqh rulings and syntheses.

---

## 1. Scoring Criteria (1 - 10 Scale)

Evaluate each Madhab file and the final synthesis on a 1-10 scale based on the following bands:

* **9 - 10: Exceptional (Gold Standard)**
  * Fully traces the ruling back to classical sources with verified book titles, authors, and chapters.
  * Clear and precise application of the school's unique Usul methodology.
  * Explains intermediate steps of analogical derivation (*qiyas*) or juristic preference (*istihsan* / *maslahah*).
  * Elaborates on the precise textual linguistics (*amm* / *khass*, *muhkam* / *mutashabih*, *nasikh* / *mansukh*).
  * Captures deep, substantive debates at the Usul level with other schools.
* **7 - 8: Proficient**
  * Accurately states the dominant ruling and cites classical works.
  * Captures the basic Usul derivation, but explanation of linguistic details or analogical links is brief.
  * Captures internal dissent and main points of dispute with other schools.
* **5 - 6: Developing**
  * Correct ruling, but classical citations are vague or marked `(UNCERTAIN)` without attempt to verify.
  * Derivation is stated but not explained (e.g., lists a verse or Hadith but fails to explain *how* it rules on the question).
  * Usul-level disputes are shallow or simply list the rulings of other schools instead of methodological differences.
* **1 - 4: Deficient**
  * Contains historical, linguistic, or legal inaccuracies.
  * Shows evidence of citation hallucination (invented books or authors).
  * Fails to address the core legal components (e.g., missing Qiyas components or abrogation analysis).

---

## 2. Madhab-Specific Methodological Signatures

Ensure each school's output reflects its authentic classical epistemology:

### Hanafi Signature
* **Core tools**: Heavy analogical reasoning (*qiyas*), juristic preference (*istihsan*), and custom/practice (*urf*).
* **Textual stance**: Treats *amm* (general) texts of the Quran as definitive (*qat'i*), meaning a solitary Hadith (*ahad*) cannot restrict or abrogate it unless it meets specific criteria.
* **Key references**: *Al-Hidaya* (Al-Marghinani), *Radd al-Muhtar* (Ibn Abidin), *Bada'i al-Sana'i* (Al-Kasani), *Al-Mabsut* (Al-Sarakhsi).

### Maliki Signature
* **Core tools**: Practice of the people of Madinah (*amal ahl al-madinah*) as a living transmission of the Sunnah, public interest (*maslahah mursalah*), blocking the means to evil (*sadd al-dhara'i*).
* **Textual stance**: Prefers the practice of Madinah over solitary Hadiths if they conflict.
* **Key references**: *Al-Mudawwanah* (Sahnun), *Al-Kafi* (Ibn Abd al-Barr), *Al-Tadhkirah* (Qarafi), *Bidayat al-Mujtahid* (Ibn Rushd).

### Shafi'i Signature
* **Core tools**: Strict analogical reasoning (*qiyas*), rejection of juristic preference (*istihsan*) and unanchored public interest. Relies on *istishab* (presumption of continuity).
* **Textual stance**: Quran and Sunnah are of equal rank in explaining each other; a Sahih Hadith always takes precedence over analogical reasoning or regional practice.
* **Key references**: *Al-Umm* (Al-Shafi'i), *Al-Majmu'* (Al-Nawawi), *Nihayat al-Muhtaj* (Al-Ramli), *Tuhfat al-Muhtaj* (Al-Haytami).

### Hanbali Signature
* **Core tools**: Strict textualism. Prioritizes the literal Quran and Sunnah, statements of the Companions (*qawl al-sahabi*), and even weak Hadiths (*da'if*) over analogical reasoning (*qiyas*), which is used only as a last resort.
* **Textual stance**: Extremely reluctant to engage in metaphorical interpretation (*ta'wil*) of texts.
* **Key references**: *Al-Mughni* (Ibn Qudamah), *Al-Insaf* (Al-Mardawi), *Al-Furu'* (Ibn Muflih), *Zad al-Mustaqni'* (Al-Hajjawi).

---

## 3. Reference and Citation Auditing

Verify the following citation rules:
1. **Source Verifiability**: Any book cited must historically exist and belong to the correct school (e.g., citing *Al-Hidaya* for a Hanbali ruling is a severe failure).
2. **Hadith Attribution**: Hadiths must be accurately attributed to their canonical collections (e.g., Bukhari, Muslim, Abu Dawud, Tirmidhi, Nasa'i, Ibn Majah, Muwatta Malik).
3. **Verification Markers**: Rulings must be marked with `(VERIFIED)` or `(UNCERTAIN)`. Audits should verify if the grader can confirm the citation. If the grader is uncertain, it should search the web or flag it.

---

## 4. Synthesis Balance and Synthesis Quality

The synthesis must:
1. **Unbiased Presentation**: Avoid favoring one school over another.
2. **Consensus Identification**: Clearly differentiate between points of absolute consensus (*ijma*), majority agreement (*jumhur*), and solitary disagreements (*shadh*).
3. **Ikhtilaf (Disagreement) Reasons**: Explain *why* they disagreed. (e.g., "They disagreed because the Hanafis treated the Quranic term X as general, whereas the Shafi'is restricted it based on Hadith Y").
4. **Modern Application**: For contemporary issues, trace how modern boards (e.g., International Islamic Fiqh Academy, AMJA) mapped new issues (*nawazil*) to classical templates.
