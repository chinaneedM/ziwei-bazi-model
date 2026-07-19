# Preblind staged access

The clean-blind runtime is split into two machine-gated stages.

## PREBLIND

The model may read only the frozen chart facts, question stems, preblind skeletons, method packet, and source excerpts selected from question stems plus frozen chart facts. Option letters, option text, option-derived source routing, pairwise templates, prior predictions, reveals, and answers are withheld.

Each question must produce an independently hashed Ziwei blind-axis model and Bazi blind-axis model. The seal bundle must state that no option payload was accessed before both seals passed.

## POSTBLIND_OPTION_CHALLENGE

A deterministic release command validates the dual-track seal bundle and creates a `POSTBLIND-ACCESS-RECEIPT-V1`. Only then may the model read option text, the option-aware source packet, and the postblind adjudication template.

Any premature option visibility invalidates the group run. It cannot be repaired by ignoring the visible text; a new group run ID is required.
