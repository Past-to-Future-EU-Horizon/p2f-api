# Local libraries
# Third Party Libraries
# Batteries included libraries
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class FA:  # function annotations
    def __init__(self):
        # run level
        self.web = "🕸️"
        self.service = "🚌"
        self.data = "💾"
        self.background = "🌄"
        # CRUD operation
        self.get = "🔎"
        self.list = "📃"
        self.create = "🆕"
        self.update = "✏️"
        self.delete = "🗑️"
        self.assign = "↔️"
        self.remove = "🔙"
        # Other
        self.auth = "🔐"


fa = FA()
