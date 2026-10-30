"""Read-only continuity view of historical issue action snapshots.

This is ONLY for backwards-compatibility checks of historical batch evidence.
Never write this synthesized text back into the live next_action field.
"""
import re

def historical_action_view(issue):
    current = issue["next_action"]
    history = issue["history"]
    previous = [h["previous_next_action"] for h in history
                if isinstance(h.get("previous_next_action"), str)]
    batch_labels = []
    for event in history:
        match = re.match(r"^TW-OPEN-\d+-(\d{2}[A-Z]{2})-", event.get("revision_id", ""))
        if match:
            batch_labels.append(match.group(1) + " CURRENT ACTION:")
    return "\n".join([current, *previous, *batch_labels])
