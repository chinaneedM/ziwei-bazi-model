# Method releases

Each child directory is an immutable promoted prediction-method release. A run is valid only when its method packet resolves to the exact active or explicitly shadow-bound method release and every mandatory stage cites a rule from that packet.

No release is edited in place. Promotion creates a receipt and advances `method/active-release.json`; rollback creates a separate receipt and moves the pointer to a prior validated release. Method validation and interface completion never count as prediction-accuracy improvement by themselves.
