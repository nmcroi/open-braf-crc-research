# CD47 follow-up: separate cell context and intervention

12 September 2026 · TASK-0006 · exploratory source review, not treatment evidence.

## Findings and checked scope

1. **PMID 27473366 / PMC4967340:** full XML retrieved; introduction, abstract and relevant references inspected. The INDRA sentence is introductory background, not an experimental CD47/VEGF result from this study. The study measured circulating thrombospondin-1 in pulmonary hypertension. The exact sentence cites reference 9, PMID 23591719, a paper on self-renewal and stem-cell transcription factors. This citation is not automatically direct evidence for every pathway in the sentence. [Full source](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC4967340/fullTextXML).
2. **PMID 20923780, DOI 10.1074/jbc.M110.172304:** primary abstract and metadata independently retrieved via Europe PMC. In endothelial models, TSP1 engagement of CD47 inhibited VEGFR2 phosphorylation; suppressing or deleting CD47 removed that inhibitory effect. The abstract reports no inhibition of VEGF binding to its receptor. This distinguishes ligand, receptor and activation state. Full XML retrieval returned 404; doses, replicate counts and full figures were not independently checked. [Primary article](https://pubmed.ncbi.nlm.nih.gov/20923780/).
3. **PMID 25200950, DOI 10.4049/jimmunol.1303116:** primary abstract and metadata independently retrieved. Human Jurkat and primary murine T-cell experiments report context-dependent VEGF responses. CD47 ligation and CD47 loss can both reverse some inhibitory VEGF effects, while CD47 deficiency also changes VEGF/VEGFR2 expression. Abstract-level review only; full figures and concentrations remain unchecked. [Primary article](https://pubmed.ncbi.nlm.nih.gov/25200950/).

These experiments do not establish BRAF/MSS colorectal treatment benefit. Genetic deletion, TSP1 ligation, and a therapeutic antibody are different perturbations. The direction of a pathway effect cannot simply be transferred between them or between cell types.

## Concrete next experiment-comparison task

For the two primary papers, extract a table with cell type/species, ligand or drug, dose and exposure, CD47 perturbation, measured VEGFR2 phosphorylation, proliferation/TCR endpoint, controls and replicate counts. Distinguish CD47–TSP1 signaling from CD47–SIRPα blockade. Check whether any actual antibody experiment reproduces the genetic result before extrapolating to a proposed anti-CD47 approach.

A testable hypothesis is that the effect depends on cell compartment and perturbation. It would be weakened if matched experiments show the same direction across endothelial cells and T cells with the same intervention, exposure and endpoint. This is a proposed comparison, not an experiment performed here.

## Limitations and reproducibility

Search: “CD47 thrombospondin inhibits VEGFR2 phosphorylation Kaur 2010 primary study”. Primary metadata/abstracts queried using Europe PMC EXT_ID with SRC:MED. PMC browser pages returned a browser check; legitimate Europe PMC XML access succeeded for PMC4967340. The 2010 full XML returned 404. No restricted data accessed or experiments run. No exhaustive search claim. Remaining two inaccessible SHP2 articles in TASK-0006 are still open.
