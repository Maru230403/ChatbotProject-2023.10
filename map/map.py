from flask import Blueprint, render_template, request, current_app
import util.map_util as mu

map_bp = Blueprint('map_bp', __name__)

menu = {'ho':0, 'us':0, 'cr':0, 'ma':1, 'cb':0, 'sc':0}

@map_bp.route('/realestate', methods=['GET','POST'])
def realestate():
    if request.method == 'GET':
        return render_template('map/real_form.html', menu=menu)
    else:
        realestates = request.form.getlist('realestate')
        realestates = [realestate for realestate in realestates if len(realestate.strip()) != 0]
        mu.get_realestate_map(current_app.root_path, realestates)     # static/img/station_map.html 파일
        return render_template('map/real_res.html', menu=menu)