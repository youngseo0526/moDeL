# moDeL_DLproject

> Semantic segmentation 기술을 이용한 인물구도 추천 서비스
- 사용 기술

[[Updated] BodyPix: Real-time Person Segmentation in the Browser with TensorFlow.js](https://blog.tensorflow.org/2019/11/updated-bodypix-2.html)

[tensorflow/tfjs-models](https://github.com/tensorflow/tfjs-models/tree/body-pix-v2.0.4/body-pix)

---
## 초기 settings  

<pre>
python -m venv venv

cd venv

Scripts\activate.bat

cd .. 

pip install -r requirements.txt

python manage.py makemigrations

python manage.py migrate
 
python manage.py createsuperuser

python manage.py runserver
</pre>