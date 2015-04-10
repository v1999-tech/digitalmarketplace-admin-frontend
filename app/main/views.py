from flask import render_template, request, redirect, session
from . import main
from .helpers.validation_tools import Validate
from .helpers.content import ContentLoader
from .helpers.service import ServiceLoader
from .helpers.presenters import Presenters
from .helpers.s3 import S3
from .helpers.auth import check_auth, is_authenticated


content = ContentLoader(
    "app/section_order.yml",
    "bower_components/digital-marketplace-ssp-content/g6/"
)
presenters = Presenters()


@main.route('/')
def index():
    return render_template("index.html", **get_template_data())


@main.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template("login.html", **get_template_data({
            "previous_responses": None,
            "logged_out": "logged_out" in request.args
        }))

    if check_auth(
        request.form['username'],
        request.form['password'],
        main.config['PASSWORD_HASH']
    ):
        session['username'] = request.form['username']
        return redirect('/')

    return render_template("login.html", **get_template_data({
        "error": "Could not log in",
        "previous_responses": request.form
    }))


@main.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login?logged_out')


@main.route('/service')
def find():
    return redirect("/service/" + request.args.get("service_id"))


@main.route('/service/<service_id>')
def view(service_id):
    service_loader = ServiceLoader(
        main.config['API_URL'],
        main.config['API_AUTH_TOKEN'],
    )
    service_data = service_loader.get(service_id)
    presented_service_data = {}
    for key, value in service_data.items():
        presented_service_data[key] = presenters.present(
            value, content.get_question(key)
        )

    template_data = get_template_data({
        "sections": content.sections,
        "service_data": presented_service_data,
        "service_id": service_id
    })
    return render_template("view_service.html", **template_data)


@main.route('/service/<service_id>/edit/<section>')
def edit(service_id, section):
    service_loader = ServiceLoader(
        main.config['API_URL'],
        main.config['API_AUTH_TOKEN'],
    )

    template_data = get_template_data({
        "section": content.get_section(section),
        "service_data": service_loader.get(service_id)
    })
    return render_template("edit_section.html", **template_data)


@main.route('/service/<service_id>/edit/<section>', methods=['POST'])
def update(service_id, section):
    service_loader = ServiceLoader(
        main.config['API_URL'],
        main.config['API_AUTH_TOKEN'],
    )

    s3_uploader = S3(
        bucket_name=main.config['S3_DOCUMENT_BUCKET'],
    )

    service = service_loader.get(service_id)
    posted_data = dict(
        list(request.form.items()) + list(request.files.items())
    )

    # Turn responses which have multiple parts into lists
    for key in request.form:
        item_as_list = request.form.getlist(key)
        if len(item_as_list) > 1:
            posted_data[key] = [
                list_item for list_item in item_as_list if list_item.strip()
            ]

    form = Validate(content, service, posted_data, s3_uploader)
    update = {}

    for question_id in posted_data:
        if question_id not in form.errors:
            if question_id in form.clean_data:
                update[question_id] = form.clean_data[question_id]
            else:
                update[question_id] = posted_data[question_id]

    if form.clean_data is not None:
        for question_id in form.clean_data:
            if question_id not in form.errors and question_id not in update:
                update[question_id] = form.clean_data[question_id]

    if update:
        api_response = service_loader.post(
            service['id'],
            update,
            session['username'],
            'admin app'
        )
        if not api_response.ok:
            try:
                return api_response.json()['error']
            except TypeError:
                return str(api_response.content)

    if form.errors:
        service.update(form.dirty_data)
        return render_template("edit_section.html", **get_template_data({
            "section": content.get_section(section),
            "service_data": service,
            "service_id": service_id,
            "errors": form.errors
        }))
    else:
        return redirect("/service/" + service_id)


def get_template_data(merged_with={}):
    template_data = dict(main.config['BASE_TEMPLATE_DATA'], **merged_with)
    template_data["authenticated"] = is_authenticated()
    return template_data
