from flask import Blueprint, render_template, request, current_app, jsonify
import json, os
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

chatbot_bp = Blueprint('chatbot_bp', __name__)

menu = {'ho':0, 'ol':1, 'ba':0, 'fr':0, 'mp':0 }




@chatbot_bp.before_app_first_request
def before_app_first_request():
    global model, wdf
    model = SentenceTransformer('jhgan/ko-sroberta-multitask')
    filename = os.path.join(current_app.static_folder, 'data/1030_0355data.csv')
    wdf = pd.read_csv(filename)
    wdf.embedding = wdf.embedding.apply(json.loads)
    print('Wellness initialization is done.')

@chatbot_bp.route('/counsel', methods=['GET','POST'])
def counsel():
    if request.method == 'GET':
        
        return render_template('chatbot/counsel.html', menu=menu)
    
    else:
        user_input = request.form['userInput']
        embedding = model.encode(user_input)
        wdf['유사도'] = wdf.embedding.map(lambda x: cosine_similarity([embedding],[x]).squeeze())
 # 최종점수를 유사도와 동일하게 설정

        answer = wdf.loc[wdf.유사도.idxmax()]

        result = {
            'category': answer.구분,
            'user': user_input,
            'chatbot': answer.챗봇,
            'similarity': answer.유사도,
            'final_score': answer.유사도  # 최종점수를 유사도와 동일하게 설정
        }
    

        return json.dumps(result)
    
@chatbot_bp.route('/get_welcome_message', methods=['GET'])
def get_welcome_message():
    # 챗봇의 초기 환영 메시지 생성
    if request.method == 'GET':
        welcome_message = "안녕하세요. 챗봇 올림입니다!^^ 부동산에 관해서 궁금한 사항이 있으시면 질문해주세요."
        result = {
            'message': welcome_message
        }


    # JSON 형식으로 반환
        return json.dumps(result)

@chatbot_bp.route('/get_info_from_index', methods=['POST'])
def get_info_from_index():
    data = request.get_json()
    index = data.get('index')
    print('Received index:', index)
    
    # 데이터 프레임에서 해당 인덱스의 데이터를 조회하는 코드
    # 예시: result = df.loc[index]
    
    # 조회한 데이터를 응답으로 돌려주기
    return jsonify({'data': 'some data'})
    


@chatbot_bp.route('/bard', methods=['GET','POST'])
def bard():
    pass

@chatbot_bp.route('/genImg', methods=['GET','POST'])
def gen_img():
    pass