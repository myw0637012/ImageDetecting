# OpenCV를 이용하여 부적합품 검출 및 Qt Desiner을 이용한 UI의 제작과 연결

## 1. 목적
- 제품의 Product Quality 강화를 위해 OpenCV Vision을 사용하여 적합/부적합품 100% 검출 
- 구현된 코드를 Qt Desiner을 이용하여 UI의 제작/연결 후 작업자들이 쉽게 사용 가능 실현

## 2. OpenCV 사용하여 제품 판정 코드 설명
- 검사 하고자 하는 Product의 Image를 load 한다.
<br>
<img src="https://user-images.githubusercontent.com/60453719/88246787-8d112480-ccd6-11ea-8c45-703fe749c9be.JPG">

- 검사 부위 별(left, middle, right)로 이진화 처리를 한다.
<br>
<img src="https://user-images.githubusercontent.com/60453719/88246975-22141d80-ccd7-11ea-8ef8-47c31de78bc3.JPG">

- left와 right part의 전체 도형 넓이와 원이 넓이 및 middle part의 도형의 넓이를 구한다.
    
    - < Left/Right >
    <br>
    <img src="https://user-images.githubusercontent.com/60453719/88247003-348e5700-ccd7-11ea-9629-969ebda55056.JPG">
    <br>

    - < Middle >
    <br>
    <img src="https://user-images.githubusercontent.com/60453719/88247021-3d7f2880-ccd7-11ea-9f24-2ce0b23c35f0.JPG">
    
- 각각의 부위 별로 적합 품의 넓의 기준을 설정하여 Detecting을 하도록 한다.
    - < Left/Right >
    <br>
    <img src="https://user-images.githubusercontent.com/60453719/88247031-496aea80-ccd7-11ea-992e-b93cee102d02.JPG">
    - < Middle >
    <br>
    <img src="https://user-images.githubusercontent.com/60453719/88247040-4ff96200-ccd7-11ea-9ec6-f302b984b118.JPG">

- 제품의 적합/부적합을 화면에 표시를 해준다.
    <br>
    <img src="https://user-images.githubusercontent.com/60453719/88247053-58519d00-ccd7-11ea-98f3-6a3debe9c37c.JPG">
    <br>

## 3. Qt Desiner을 이용한 UI의 제작과 연결
- Qt Desiner를 통해 UI를 제작하여 검사원들이 쉽게 부적합을 판정할 수 있을 뿐만 아니라, Vision 기술을 사용하여 검출력을 100% 까지 향상 시켜 Zero Defect를 환경 조성. 
- GUI 프로그램 환경 구축
    <br>
    <img src="https://user-images.githubusercontent.com/60453719/88247057-5ee01480-ccd7-11ea-8210-5a7f48a64abf.JPG">
    <br>

- Processing Image 함수에 Jupyter code를 Python 환경에 맞게 INPUT

- 사진을 출력할수 있는 DisplayOutputImage 함수를 구현
    <br>
    <img src="https://user-images.githubusercontent.com/60453719/88247066-66072280-ccd7-11ea-978b-1f4461be0bc3.JPG">
    <br>
- cv2.imread가 한글 지원하지 않으므로 새로운 방식으로 파일 조합
    <br>
    <img src="https://user-images.githubusercontent.com/60453719/88247073-6dc6c700-ccd7-11ea-97fd-a4f3c65a9654.JPG">
    <br>
- load된 사진의 이진화 처리
    <br>
    <img src="https://user-images.githubusercontent.com/60453719/88247087-75866b80-ccd7-11ea-8210-6ef2e7f4aba2.JPG">
    <br>
- load버튼 클릭 시 사진 로드 되도록 구현
    <br>
    <https://user-images.githubusercontent.com/60453719/88247098-7f0fd380-ccd7-11ea-8f69-96feab079af3.JPG">
    <br>
    <https://user-images.githubusercontent.com/60453719/88247105-8505b480-ccd7-11ea-80a1-cc982e55ffbe.JPG">
    <br>

## 4. 개발 언어
- Python 
- Qt Desiner
- Jupyter
