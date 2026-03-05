---
tags:
- field/science
- subject/biology
- concept/genetics
---

[[T.O.C (Biology)|Up to Biology]]

# Biology - CRISPR-Cas9 Mechanism

## The Molecular Scalpel
How does a protein tell one specific stretch of DNA apart from three billion others? In a crowded nucleus, it seems impossible. Yet CRISPR-Cas9 manages this feat with staggering precision. It is a bacterial immune system repurposed as a surgical tool. The process begins with a search.

### The Search: Scouting for the PAM
The Cas9 protein does not just wander aimlessly. It is a surveyor. It carries a short piece of RNA, the single guide RNA (sgRNA), which acts as a molecular "wanted" poster. But the protein doesn't check the DNA sequence first. It looks for a marker called the PAM (Protospacer Adjacent Motif). 

Think of the PAM as a safety lock. It is a short, specific sequence (usually NGG for the common Cas9) that must be present before the protein even attempts to unzip the double helix. If the PAM isn't there, Cas9 bounces off. This prevents the system from accidentally chopping up the bacterium's own CRISPR array, which lacks these PAM markers. It is a fail-safe.

### The Unzipping: Forming the R-Loop
Once it finds a PAM, Cas9 latches on. It forces the DNA strands apart. This is the moment of truth. The guide RNA attempts to bind with the exposed DNA strand. If the sequences match, the RNA zips up with the DNA, creating a stable structure known as an R-loop. 

This isn't a loose fit. It is a rigorous base-pairing match. Every nucleotide must align. If they don't, the tension of the mismatched strands pulls the RNA away, and Cas9 releases its grip. But if the match is perfect, the protein undergoes a radical shift in shape. It prepares to strike.

### The Strike: Dual Blades
The Cas9 protein is equipped with two molecular blades: the RuvC and HNH nuclease domains. They are not blunt instruments. They are precise. When the R-loop is fully formed, these domains swing into position. 

The HNH domain cuts the DNA strand that is bound to the RNA. Simultaneously, the RuvC domain slices the opposite strand. The result is a clean, blunt-ended break in the double helix. The target gene is now severed. The protein's work is done, but the cell's crisis has just begun.

### The Repair: Genetic Editing
A broken chromosome is a lethal event for a cell. Its repair machinery rushes to the site immediately. This is where the actual "editing" happens. 

In most cases, the cell uses Non-Homologous End Joining (NHEJ). It simply jams the broken ends back together. This process is messy. It often adds or deletes a few nucleotides, which shifts the reading frame and effectively "knocks out" the gene. The gene is silenced. 

However, if we provide the cell with a repair template—a piece of DNA that looks like the target site but carries a desired change—the cell might use Homology Directed Repair (HDR). It copies the information from the template to fix the break. This is how we "knock in" a new gene or correct a mutation. We don't edit the DNA ourselves; we trick the cell into doing it for us.