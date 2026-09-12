# B6H12 functional experiment and available data

12 September 2026 · TASK-0006 · preclinical, scoped source review.

## Article check

[PMID26840086 / DOI10.18632/oncotarget.7100](https://pmc.ncbi.nlm.nih.gov/articles/PMC4891109/): full XML retrieved; relevant results, methods and figure legends inspected, not raw images or supplements independently validated.

B6H12 was a functional intervention at 1 µg/mL with an isotype control. Breast cancer stem-like populations derived from MDA-MB-231 and T47D showed reduced proliferation, whereas MCF7 and MCF10A showed increased DNA synthesis. Thus even within breast models the direction is not uniform.

For acute EGFR experiments, Figure 6 specifies 15-minute antibody pretreatment and 5-minute EGF stimulation; methods also describe a 7-minute stimulation. Preserve this discrepancy when reproducing. Figure 6 reports three experiments; that count must not be assigned to every figure. The article reports inhibition at EGFR Y1068, not Y992. This is not the VEGFR2 endpoint from the earlier papers.

The methods link expression data to GSE67966. These findings support testing a direct signaling effect of this particular antibody. They do not show that all CD47 blockers share it, or demonstrate BRAF/MSS colorectal benefit. A CD47-loss/rescue specificity experiment was not verified in this review.

## Dataset check — actual download

[GSE67966](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE67966) lists 12 arrays on GPL570. Downloaded processed matrix: 54,675 probe-set rows; four groups of three named replicates. Sample titles and characteristics agree on suspension cells, attached cells, B6H12-treated suspension cells, and isotype-treated suspension cells. Treated samples specify 36 hours. Replicate independence still needs verification.

The series summary includes extracellular-vesicle/T-cell material inconsistent with its title and these sample labels. Do not classify this dataset from that summary alone. Metadata names RMA/Expression Console; the paper describes a Partek workflow. Processing equivalence needs checking before attempting exact reproduction.

[Direct matrix](https://ftp.ncbi.nlm.nih.gov/geo/series/GSE67nnn/GSE67966/matrix/GSE67966_series_matrix.txt.gz): 2,410,201 bytes; SHA256 `29d35292efae5a599793700ed2e925b4c081c24607e3abb29d96fd20bb04f21d`.

## Next bounded analysis

Compare B6H12 with isotype within suspension cells (three versus three), separately from suspension versus attached cells. Verify scale, probe annotation, replicate independence and processing first. Check EGFR/KLF4 and predefined exploratory genes without treating a selected positive result as independent validation. No differential-expression results are reported yet. Raw CEL files have not been downloaded.
