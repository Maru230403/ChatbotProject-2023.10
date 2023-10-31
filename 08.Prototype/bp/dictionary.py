from flask import Blueprint, render_template, current_app, request
import util.crawl_util as cu


dictionary_bp = Blueprint('dictionary_bp', __name__)

menu = {'ho':0, 'us':0, 'cr':1, 'ma':0,'cb':0,  'sc':0}

@dictionary_bp.route('/jeonse')
def jeonse():
    print(current_app.root_path)       #bp module에서는 app 대신에 current_app을 사용
    return render_template('/dictionary/jeonse.html',  menu=menu)

@dictionary_bp.route('/wolse')
def wolse():
    print(current_app.root_path)
    return render_template('/dictionary/wolse.html',  menu=menu)


@dictionary_bp.route('/tip')
def tip():    
    print(current_app.root_path)
    return render_template('/dictionary/tip.html',  menu=menu)


@dictionary_bp.route('/siksin', methods=['GET','POST'])
def siksin():
    print(current_app.root_path)
    if request.method == 'GET':
        return render_template('/crawling/siksin.html', menu=menu)
    else:
        print(current_app.root_path)
        place = request.form['place']
        rest_list = cu.get_restaurant_list(place)        
        return render_template('/crawling/08.siksin.html', menu=menu, place=place, rest_list=rest_list)


