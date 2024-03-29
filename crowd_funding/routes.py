from flask import Blueprint, request, jsonify, redirect, url_for
from crowd_funding.service import create_project, get_all_projects, get_projects_by_category, get_project_details, \
    get_all_investors, make_investment, get_investment_details_by_project_id, get_investor_dashboard, submit_feedback

crowd_funding_bp = Blueprint('crowd_funding', __name__)


@crowd_funding_bp.route("/project", methods=["POST"])
def create_project_func():
    print("POST rule /project")
    project, status_code = create_project(request)
    return jsonify(project), status_code


@crowd_funding_bp.route("/project", methods=["GET"])
def get_all_projects_func():
    print("GET rule /project")
    projects, status_code = get_all_projects()

    if not projects:
        return {"success": "false", "message": "No projects found for funding"}, 404

    return jsonify(projects), status_code


@crowd_funding_bp.route("/project?category={category}", methods=["GET"])
def get_projects_by_category_func():
    print("GET rule /project?category={category}")
    category = request.args.get("category")

    if category is None:
        return {"success": "false", "message": "No category was found in query"}, 404

    projects, status_code = get_projects_by_category(category)

    if not projects:
        return {"success": "false", "message": "The project was not found in the specified category."}, 404

    return jsonify(projects), status_code


@crowd_funding_bp.route("/project/<project_id>", methods=["GET"])
def get_project_details_func(project_id):
    print("GET rule /project/<project_id>")

    project, status_code = get_project_details(project_id)

    if not project:
        return {"success": "false", "message": f"No project with project id {project_id} found"}, 404

    return jsonify(project), status_code


@crowd_funding_bp.route("/investor/", methods=["GET"])
def get_all_investors_func():
    print("GET rule /investor")
    investors, status_code = get_all_investors()

    if not investors:
        return {"success": "false", "message": "Investor  not found."}, 404

    return jsonify(investors), status_code


@crowd_funding_bp.route("/investor/investment", methods=["POST"])
def make_investment_func():
    print("POST rule /investor/investment")
    investment, status_code = make_investment(request)

    return jsonify(investment), status_code


@crowd_funding_bp.route("/project/<int:project_id>/investments", methods=["GET"])
def get_investment_details_by_project_id_func(project_id):
    print("GET rule /project/<int:project_id>/investments")

    project_investment, status_code = get_investment_details_by_project_id(project_id)

    return jsonify(project_investment), status_code


@crowd_funding_bp.route("/investor/dashboard", methods=["GET"])
def get_investor_dashboard_func():
    print("GET rule /investor/dashboard?investorId={investor_id}")
    investor_id = request.args.get("investorId")

    if not investor_id:
        print("No InvestorId provided", request.args)
        return jsonify("No InvestorId found in query"), 400

    investor, status_code = get_investor_dashboard(investor_id)

    if investor is None:
        return {"success": "false", "message": f"No project with project id {investor_id} found"}, 404

    return jsonify(investor), status_code


@crowd_funding_bp.route("/investor/<int:project_id>/feedback", methods=["POST"])
def submit_feedback_func(project_id):
    feedback,status_code = submit_feedback(project_id,request)
    return jsonify(feedback),status_code
