# moDeL_DLproject

> Semantic segmentation 기술을 이용한 인물구도 추천 서비스






#### 아래 사진 클릭시 서비스 발표 영상으로 이동합니다 👀

[![Video Label](http://img.youtube.com/vi/xAwtfL2Er7o/0.jpg)](https://www.youtube.com/watch?v=xAwtfL2Er7o)



---


## 개발 필요성



  우리는 구도가 좋은 인물사진을 찍을 수 있도록 인물의 비율을 실시간으로 측정해 카메라를 조정할 수 있게 유도했다. 이를 위해 인물 전신의 비율을 실시간으로 측정하는 기술이 필요했고 **BodyPix** 모델을 사용했다.
  BodyPix는 구글이 공개한 실시간 person segmentation과 body-part segmentation을 하는 오픈소스 machine learning 모델이다. 이미지를 사람으로 인식된 픽셀(전경)과 안 된 픽셀(배경)로 분류하고, 나아가 사람으로 인식된 픽셀을 얼굴, 팔, 몸통 등 인체의 24개 파트로 나누어 분류한다. BodyPix의 가장 큰 특징은 특별한 장비 없이 웹캠이나 스마트폰 카메라로도 실시간 동작하는 것이다. 때문에 자바스크립트(JavaScript) 라이브러리인  tensorflow.js 기반으로 만들어졌고, 이 실시간성이 우리가 최종적으로 구현하고 싶은 앱과 맞닿아 있어 선택하게 됐다.

#### BodyPix 공식 blog: https://blog.tensorflow.org/2019/11/updated-bodypix-2.html

--- 


## 구현 기술 




  ### 1. BodyPix의 모델 학습 방법  
  BodyPix는 convolutional neural network(CNN) 알고리즘을 이용하는데 ResNet 모델과 MobileNet 모델을 둘 다 학습시켰다. ResNet 모델이 더 정확하지만 MobileNet 모델이 mobile device과 사용자들의 일반적인 컴퓨터에 더 효율적으로 작동한다.
  모든 training data를 annotate 해주는 것은 시간이 아주 오래걸리는 일이다. 그래서 구글은 컴퓨터 그래픽스를 이용해 ground truth body part segmentation annotation이 있는 images를 만들었다. 모델을 학습하기 위해, 이들은 rendered image와 실제 COCO images(instance segmentation annotation)를 동시에 이용했다.
  training data를 섞어 사용하는 점과 multi-task loss로, ResNet 모델은 simulated annotation만으로 24 body-part prediction capability를 학습할 수 있게 되었다.
![image01](https://user-images.githubusercontent.com/62318430/120515399-3c477d80-c409-11eb-8e09-93e3ecd80f8b.png)

  마지막으로 COCO 이미지에 대한 ResNet 모델(선생님 역할)의 prediction을 MobileNet(학생 역할)에 distill한다.
![image02](https://user-images.githubusercontent.com/62318430/120515429-42d5f500-c409-11eb-9f98-9b481267958d.png)


  ### 2. person segmentation, body segmentation
  person segmentation으로 사람인지 아닌지에 대한 픽셀 정보와 body-part segmentation으로 해당 신체부위가 맞는지 아닌지에 대한 픽셀정보를 취합해 사람이 아닌 픽셀은 -1, 그리고 사람으로 인식된 픽셀은 24가지 신체부위별로 각각 0-23 의 값을 가지며 output으로 나온다. 
 구체적으로, input image의 픽셀들은 MobileNet 모델과 sigmoid 함수를 거쳐 24개의 channel에서 0-1사이의 확률로 나타내어지고, threshold(임계점)을 기준으로 각 픽셀들은 (0과 1) binary한 값을 갖게 된다. 
이후 다음 표와 같이 신체를 24개로 분할해 0에서 23까지 part ID를 부여한다. 

![image03](https://user-images.githubusercontent.com/62318430/120515447-45d0e580-c409-11eb-9b3e-34122da92a41.png)
![image04](https://user-images.githubusercontent.com/62318430/120515466-49646c80-c409-11eb-87d5-4b6b7fab0673.png)
![image05](https://user-images.githubusercontent.com/62318430/120515470-4a959980-c409-11eb-8187-4ae2a7fb5cac.png)



  ### 3. BodyPix 기술의 사용
  코드 상의 output 형태를 보고 원하던 전신비율측정 방법을 생각할 수 있었다.
비율측정을 위해 머리로 인식된 가장 첫번째 픽셀과 가장 마지막 픽셀의 y좌표, 그리고 발로 인식된 가장 마지막 픽셀의 y좌표를 구해, 각각의 값을 아래의 수식에 넣어 비율을 계산하는 방법을 고안했다.

![image06](https://user-images.githubusercontent.com/62318430/120515472-4b2e3000-c409-11eb-97cb-71332bd8cf1e.png)

---
## 기대 효과 
  ### 1. 기존 앱과의 차별성
  현재 유사 어플로 인물 구도 전문 카메라 앱인 ‘SOVS’가 있다.  ‘SOVS’는 촬영하고 싶은 인물의 구도를 흰 색 가이드라인을 이용해 사용자가 직접 설정한다. 정해진 실루엣이 있고 사용자가 피사체를 실루엣 안으로 직접 맞춰 줘야한다.
  우리 서비스는 가이드라인을 사용자로 하여금 설정하는 것이 아닌 인공지능을 이용해 실시간으로 인물의 비율을 계산하여 카메라의 구도 설정을 도와준다는 점에서 차이가 있다. 초기 설정으로 본인이 만족하는 사진들을 입력하면, 그 이후에 또 다른 추가 설정을 하지 않고도 초기 입력된 사진들의 비율을 이용해 앱을 사용할 수 있다. 이런 차별점들이 시장에서의 경쟁력을 줄 것이다.

  ### 2. 보편적인 사용으로 인지도 상승
  이 서비스는 누구나 구도가 좋은 인물 사진을 찍을 수 있게 돕기 때문에 모든 사람들이 사용할 수 있다. 전신 비율 측정을 통해 좋은 사진을 찍는 점을 이용해, 모델이라는 직업과 연관지어 가상배경을 통해 런웨이에 있는 것처럼 사진을 찍어주는 체험부스를 패션위크에 진행할 수 있다.
  또, 노인들의 휴대기기를 활용한 사진 촬영 교실에 우리 서비스를 도입해 더 쉬운 촬영을 유도할 수 있다.   
더불어 사회적 공헌에 힘쓰는 기업과 함께 부모님이 자식을 찍어주는 ‘슬기로운 가족생활 챌린지’를 만들어 홍보함으로써 사용자 증가 및 수익 증대까지 기대해 볼 수 있다.

  ### 3. 수익모델
  자체 앱 내 광고 및 유료 어플을 통한 수익 창출 방법이 있다. 개인식별 기능과 같은 추후에 제공되는 기능들 몇 가지를 유료화할 예정이다. 먼 미래에는 우리 서비스를 스마트폰의 기본 카메라 기능에 도입하는 가능성도 있다고 생각한다. 
  우리 서비스는  특히 좋은 장소에 있을 때 풍경과 함께 사진을 찍고 싶은 상황에 수요가 더 있을 것이다. 이런 점을 이용해 다른 앱과의 협업을 통한 수익도 생각해봤다. 등산앱과의 협업으로 등정에 성공해 기념하는 과정에서 우리 앱을 이용해 더 좋은 사진을 촬영할 수 있게 한다. 또, 골프앱과의 협업으로 골프장에서 구도가 좋은 사진의 촬영을 도울 수 있다.  

 ### 4. 추후 발전 가능성
  추후에는 전신사진 촬영을 위해 비율 값 이외에도 수평 조정, 발 위치 조절, 역광 처리 등을 할 계획이 있다.
또한 개인 식별 기능을 구현하여 인식된 개인마다 각각에게 설정된 비율을 적용하고, 사용자가 입력한 사진을 축적하여 dataset 구성 후 사람들에게 이상적인 비율과 사진에서의 사람의 위치까지 제공하는 기능들을 생각하고 있다. 
현재 이미지 속 한명의 비율만 계산 할 수 있다는 점을 개선해 단체 사진에서도 적용가능한 비율 추천 서비스 어플을 출시할 계획이 있다.
