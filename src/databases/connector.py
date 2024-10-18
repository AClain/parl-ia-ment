from models.ExportFormat import ExportFormat
from databases.mongo_connector import Mongo


class Connector:
    """
    Wrapper to connect to external export format.
    """

    def __init__(self, export_format: ExportFormat):
        if export_format.MONGO:
            self.client = Mongo()
