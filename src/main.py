import argparse
import logging
from models.ExportFormat import ExportFormat
from scrapers.pipelines.questions_from_search_tool import questions_from_search_tool


parser = argparse.ArgumentParser(
    prog="download-questions", description="'Legislature' number."
)
parser.add_argument("-l", "--legislature", help="'Legislature' number.")
parser.add_argument("-p", "--path", help="Path to destination file.")
parser.add_argument("-e", "--export", help="Data export format.")
parser.add_argument("-q", "--questions-per-page", help="Number of questions per page.")
parser.add_argument(
    "-log", "--logging-level", help="Define the logging level of the script."
)
parser.add_argument(
    "-lq", "--log-question", help="Log the ID of each question scraped."
)
parser.add_argument("-u", "--url", help="Define the URL from which to start scraping.")
args = parser.parse_args()

# Technical args
logging_level = logging.getLevelName(args.logging_level)
if type(logging_level) is int:
    logging.basicConfig(level=logging_level, force=True)
else:
    raise TypeError(
        "'logging-level' parameter should be one of the following : "
        "'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'."
    )

# Content args
try:
    args.legislature = int(args.legislature)
    if args.url:
        questions = questions_from_search_tool(
            legislature=args.legislature,
            export_format=ExportFormat(args.export),
            questions_per_page=args.questions_per_page,
            log_question_ids=args.log_question,
            url=args.url,
        )
    else:
        questions = questions_from_search_tool(
            legislature=args.legislature,
            export_format=ExportFormat(args.export),
            questions_per_page=args.questions_per_page,
            log_question_ids=args.log_question,
        )
except TypeError as e:
    logging.error(e)
    logging.error("'legislature' parameter is not an integer.")
