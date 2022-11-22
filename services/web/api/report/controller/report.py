# -*- coding: utf-8 -*-
"""This module contains all the bussiness logic for reporting authors and articles."""
from flask import jsonify
from ...author.model import Author
from ..models import Report, report_schema, reports_schema
from ...extensions import db


def report_author(reporter_id: str, reportee_id: str, reason: str):
    if not reporter_id:
        raise ValueError('The reporting author id must be provided')
    if not reportee_id:
        raise ValueError('The reported author id must be provided')
    if reporter_id == reportee_id:
        raise ValueError('You cannot report yourself!')
    if not reason:
        raise ValueError('The reason must be provided')
    if not isinstance(reason, dict):
        raise TypeError('The reason must be a dictionary!')
    if not reason['reason']:
        raise ValueError('The reason must be provided')
    if not isinstance(reason['reason'], str):
        raise TypeError('The reason must be a string')
    if not isinstance(reporter_id, str):
        raise TypeError('The reprter id must be a string')
    if not isinstance(reportee_id, str):
        raise TypeError('The reportee id must be a string')
    if not Author.user_with_id_exists(int(reporter_id)):
        raise ValueError(f'The author with id {reporter_id} does not exist!')
    if not Author.user_with_id_exists(int(reportee_id)):
        raise ValueError(f'The author with id {reportee_id} does not exist!')
    
    report = Report(reporter_id=reporter_id, reportee_id=reportee_id, reason=reason['reason'])
    # db.session.add(report)
    # db.session.commit()
    
    return report_schema.dump(report), 201

def handle_report_author(reporter_id: str, reportee_id: str, reason: str):
    """Report an author."""
    try:
        report = report_author(reporter_id, reportee_id, reason)
    except (ValueError, TypeError) as e:
        return jsonify({'error': str(e)}), 400
    else:
        return report
    
def get_reports(author_id: str):
    """Get reports"""
    if author_id:
        if not isinstance(author_id, str):
            raise TypeError('The author id has to be a string')
        if not Author.user_with_id_exists(int(author_id)):
            raise ValueError(f'There is not author with id {author_id}')
    if author_id:
        reports = Report.query.filter_by(reportee_id=int(author_id)).all()
        return reports_schema.dump(reports), 200
    reports = Report.query.all()
    return reports_schema.dump(reports), 200
        
    
def handle_get_reports(author_id: str):
    """Get reports"""
    try:
        reports = get_reports(author_id)
    except (ValueError, TypeError) as e:
        return jsonify({'error': str(e)})
    else:
        return reports
    