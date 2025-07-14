"""
Utils: Narrative logging, Markdown folds, serialization, helpers.
"""
import datetime

def narrative_log(log, message):
    timestamp = datetime.datetime.now().isoformat()
    log.append(f"- {timestamp}: {message}")

# Markdown fold helpers
def markdown_fold(title, content):
    return f"<details><summary>{title}</summary>\n{content}\n</details>"
