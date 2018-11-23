from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user

from application import app, db
from application.series.models import Series
from application.series.forms import SeriesForm
from application.userseries.models import UserSeries

from sqlalchemy import text

@app.route("/series", methods=["GET"])
def series_index():
    return render_template("series/list.html", series = Series.query.all())

@app.route("/series/new/")
@login_required
def series_form():
    return render_template("series/new.html", form = SeriesForm())

@app.route("/series/<series_id>/", methods=["POST"])
@login_required
def series_set_episodes_total(series_id):
    s = Series.query.get(series_id)
    s.episodes_total += 1
    db.session().commit()

    return redirect(url_for("series_index"))

@app.route("/series/addtolist/<series_id>/", methods=["POST"])
@login_required
def series_add_to_userseries(series_id):
    us = UserSeries()
    us.series_id = series_id
    us.account_id = current_user.id

    db.session().add(us)
    db.session().commit()

    return redirect(url_for("series_index"))

@app.route("/series/delete/<series_id>/", methods=["POST"])
@login_required
def series_delete(series_id):
    stmt = text("DELETE FROM user_series WHERE series_id = :id").params(id=series_id)
    db.engine.execute(stmt)
    stmt = text("DELETE FROM series WHERE id = :id").params(id=series_id)
    db.engine.execute(stmt)
    db.session().commit()

    return redirect(url_for("series_index"))

@app.route("/series/", methods=["POST"])
@login_required
def series_create():
    form = SeriesForm(request.form)

    if not form.validate():
        return render_template("series/new.html", form = form)

    s = Series(form.name.data)
    s.episodes_total = form.episodes_total.data
    s.account_id = current_user.id

    db.session().add(s)
    db.session().commit()
  
    return redirect(url_for("series_index"))
