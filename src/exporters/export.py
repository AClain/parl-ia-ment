from errors.NoExportDestinationException import NoExportDestinationException
from models.ExportFormat import ExportFormat
from models.Question import Question
from exporters.export_to_csv import export_to_csv
from exporters.export_to_json import export_to_json
from exporters.export_to_mongo import export_to_mongo


def export_question(
    export_format: ExportFormat,
    question: Question,
    filename: str | None = None
):
    """
    Export a question to a given format.

    Parameters
    ----------
    export_format: ExportFormat
        The export format.
    question: Question
        The question and its associated metadata.
    filename: str | None, default=None
        Destination of the exported file.
    """
    if export_format.MONGO:
        export_to_mongo(question)
    elif export_format.JSON:
        export_to_json(question)
    elif export_format.CSV:
        if filename:
            export_to_csv(question, filename)
        else:
            raise NoExportDestinationException
    else:
        raise TypeError("Export format not supported.")
