from flask import Blueprint, render_template, request, current_app
import util.map_util as mu

map_bp = Blueprint('map_bp', __name__)

menu = {'ho':0, 'us':0, 'cr':0, 'ma':1, 'cb':0, 'sc':0}

@map_bp.route('/station', methods=['GET','POST'])
def station():
    if request.method == 'GET':
        return render_template('map/station_form.html', menu=menu)
    else:
        stations = request.form.getlist('station')
        stations = [station for station in stations if len(station.strip()) != 0]
        mu.get_station_map(current_app.root_path, stations)     # static/img/station_map.html 파일
        return render_template('map/station_res.html', menu=menu)