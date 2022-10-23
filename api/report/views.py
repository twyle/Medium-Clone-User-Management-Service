# -*- coding: utf-8 -*-
"""This module contains all the routes used to report offensive reports and reports."""
from flasgger import swag_from
from flask import Blueprint, request
from .controller import handle_report_author, handle_get_reports, token_required

report = Blueprint("report", __name__)

@report.route("/author", methods=["POST"])
@token_required
@swag_from(
    "./docs/report_author.yml", endpoint="report.report_author", methods=["POST"]
)
def report_author():
    """Report Author with given id."""
    return handle_report_author(request.args.get('reporter id'), request.args.get('reportee id'), request.json)


@swag_from(
    "./docs/get_reports.yml", endpoint="report.get_reports", methods=["GET"]
)
@report.route("/reports", methods=["GET"])
def get_reports():
    """Get an author's reports."""
    return handle_get_reports(request.args.get('author id'))