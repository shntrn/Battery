from flask import render_template, flash, redirect, url_for, request
from batteryapp import app, db, func, cast, Date, text
from batteryapp.models import Battery, Batterylog, Status
from datetime import datetime
from batteryapp.forms import NewBatteryForm, ChangeBatteryStatusForm


@app.route('/')
@app.route('/index')
def index():
    batteries = db.session.query(Battery, Battery.battery_num, Battery.capacity, Battery.room,
                               cast(Battery.last_update, Date).label('Date'), Status.status_name)\
        .outerjoin(Status, Battery.status_ref == Status.status_id).filter(Battery.status_ref != 7).all()
    return render_template('index.html', batteries=batteries, title='Home')


@app.route('/add_new', methods=['GET', 'POST'])
def add_new():
    form = NewBatteryForm()
    if form.validate_on_submit():
        battery = Battery(battery_num=form.battery_num.data, status_ref=1, capacity=2600)
        battery_id = Battery.query.filter_by(battery_num=form.battery_num.data).first()
        batterylog = Batterylog(battery_ref=battery_id.battery_id, capacity=2600, status_ref=1,
                                last_update=datetime.utcnow())
        db.session.add(battery)
        db.session.commit()
        db.session.add(batterylog)
        db.session.commit()
        flash('Congratulation! Battery is successfully added')
        return redirect(url_for('index'))
    return render_template('add_new.html', tittle='Add New Battery', form=form)


@app.route('/change_status', methods=['GET', 'POST'])
def change_status():
    form = ChangeBatteryStatusForm()
    if form.validate_on_submit():
        battery = Battery.query.filter_by(battery_num=form.battery_num.data).\
            update({'status_ref': form.status.data, 'room': form.room.data, 'capacity': form.capacity.data,
                    'last_update': datetime.utcnow()})
        battery_id = Battery.query.filter_by(battery_num=form.battery_num.data).first()
        batterylog = Batterylog(battery_ref=battery_id.battery_id, capacity=form.capacity.data,
                                room=form.room.data, status_ref=form.status.data, last_update=datetime.utcnow())
        db.session.add(batterylog)
        db.session.commit()
        flash('Congratulation! Battery status is successfully changed')
        return redirect(url_for('index'))
    return render_template('change_status.html', tittle='Change Battery Status', form=form)


#обновляем статус батарей кнопкой на сайте
@app.route('/update_status', methods=['GET', 'POST'])
def update_status():
    sql_refresh_status_break_in_45 = text('UPDATE battery SET status_ref = 10, last_update = current_timestamp \
                                    WHERE date(current_timestamp) - date(last_update) > 90 and status_ref != 7')
    sql_refresh_status_refresh_14 = text('UPDATE battery SET status_ref = 9, last_update = current_timestamp \
                                    WHERE date(current_timestamp) - date(last_update) > 14 and status_ref != 7')
    sql_refresh_status_break_30_cycles = text('UPDATE battery AS table1 \
                                            SET status_ref = 10 \
                                            FROM (SELECT COUNT(status_ref), battery_ref FROM batterylog \
                                                WHERE status_ref = 3 \
                                                GROUP BY battery_ref \
                                                HAVING COUNT(status_ref) % 30 = 0) AS table2 \
                                            WHERE table1.battery_id = table2.battery_ref')
    sql_refresh_status_refresh_10_cycles = text('UPDATE battery AS table1 \
                                                SET status_ref = 9 \
                                                FROM (SELECT COUNT(status_ref), battery_ref FROM batterylog \
                                                    WHERE status_ref = 3 \
                                                    GROUP BY battery_ref \
                                                    HAVING COUNT(status_ref) % 10 = 0) AS table2 \
                                                WHERE table1.battery_id = table2.battery_ref')

    update = db.engine.execute(sql_refresh_status_break_in_45)
    update = db.engine.execute(sql_refresh_status_refresh_14)
    update = db.engine.execute(sql_refresh_status_break_30_cycles)
    update = db.engine.execute(sql_refresh_status_refresh_10_cycles)

    db.session.commit()
    return redirect(url_for('index'))














