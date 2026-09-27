import json
import logging
import time

_log = logging.getLogger("audit")


class AuditTrail:
    """Structured audit logging; each call to execute() records one action."""

    def __init__(self, actor):
        self.actor = actor

    def execute(self, action, detail=None):
        record = {"ts": time.time(), "actor": self.actor, "action": action, "detail": detail}
        _log.info(json.dumps(record, default=str))
        return record
