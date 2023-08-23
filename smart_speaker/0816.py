import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import os, time
import threading
# from fingerprint_simpletest import get_fingerprint, get_num
import time
import board
import busio
from digitalio import DigitalInOut, Direction
import adafruit_fingerprint

answer_is_speaking = False
listen_after_speak = False
confidence_threshold = 0.7

def speak(text):
    global answer_is_speaking
    global listen_after_speak
    answer_is_speaking = True
    tts = gTTS(text=text, lang='ko')
    print('[인공지능] ' + text)
    tts.save("response.mp3")
    playsound("response.mp3")
    os.remove("response.mp3")
    answer_is_speaking = False
    listen_after_speak = True


def listen(recognizer, audio):
    global is_speaking
    if not answer_is_speaking:
        try:
            result = recognizer.recognize_google(audio, language="ko-KR", show_all=True)
            
            if not result:
                raise sr.UnknownValueError

            text = None
            for alternative in result['alternative']:
                if alternative['confidence'] >= confidence_threshold:
                    text = alternative['transcript']
                    break
            
            if text:
                is_speaking = True
                print('[사용자] ' + text)
                answer(text)
                print("대답 완료")
                is_speaking = False
            else:
                print("인식 실패")
        except sr.UnknownValueError:
            print("인식 실패")
        except sr.RequestError as e:
            print("요청 실패 : {0}".format(e))

def answer(input_text):
    global is_speaking
    print("answer_is_speaking=True",is_speaking)
    answer_text = ' '

    if '안녕' in input_text:
        is_speaking = True  # 스피커 음성이 나오는 동안 음성 인식 중지
        print("안녕")
        answer_text = '안녕하세요? 반갑습니다.'
        speak(answer_text)
        # is_speaking = False
    elif '등록' in input_text: # mqtt X()
        is_speaking = True  # 스피커 음성이 나오는 동안 음성 인식 중지
        # 지문 등록을 이전에 해야함
        # DB에 등록된 지문이랑 매칭 후 매칭이 되면 아래와 같은 멘트 출력
        answer_text = '사용자 등록이 완료되었습니다.'
        speak(answer_text)
        # is_speaking = False
    elif '손잡이' in input_text: # mqtt 앱에서 인식
        is_speaking = True  # 스피커 음성이 나오는 동안 음성 인식 중지
        answer_text = '지능형 카트의 손잡이를 인식 되었습니다.'
        speak(answer_text)
    elif '목적지 설정' in input_text: # 처음 목적지 지정
        is_speaking = True  # 스피커 음성이 나오는 동안 음성 인식 중지
        answer_text = '음성으로 목적지를 설정해주세요.'
        speak(answer_text)
    elif '목적지' in input_text:
        is_speaking = True  # 스피커 음성이 나오는 동안 음성 인식 중지
        answer_text = '목적지로 출발합니다. 카트 출발!!'
        speak(answer_text)
        # 여기에서 카트를 출발시키는 코드 추가
        
    elif '속도 조절' in input_text:
        is_speaking = True  # 스피커 음성이 나오는 동안 음성 인식 중지
        # 사용자가 속도 조절을 요청한 경우 -> 아두이노로
        answer_text = '속도를 조절합니다. 얼마로 해드릴까요?'
        speak(answer_text)
    elif '장애물' in input_text:
        is_speaking = True  # 스피커 음성이 나오는 동안 음성 인식 중지
        # 사용자에게 장애물 거리 정보 제공
        # 여기에서 장애물 거리에 따라 카트 조절하는 코드 추가
        answer_text = '주변에 장애물이 있습니다. 조심하세요.'
        speak(answer_text)
    elif '맛집' in input_text:
        is_speaking = True  # 스피커 음성이 나오는 동안 음성 인식 중지
        # 주변 맛집 정보 제공
        answer_text = '주변 맛집정보를 안내해 드릴게요.'
        speak(answer_text)
    elif '쇼핑 정보' in input_text:
        # 주변 쇼핑 정보 제공
        is_speaking = True  # 스피커 음성이 나오는 동안 음성 인식 중지
        answer_text = '주변 쇼핑정보를 안내해 드릴게요.'  
        speak(answer_text) 
    elif '환타' in input_text:
        is_speaking = True  # 스피커 음성이 나오는 동안 음성 인식 중지
        answer_text = '환타' #환타 맞아?
        speak(answer_text)
    elif '콜라' in input_text:
        is_speaking = True  # 스피커 음성이 나오는 동안 음성 인식 중지
        answer_text = '콜라'
        speak(answer_text)
    elif '사이다' in input_text:
        is_speaking = True  # 스피커 음성이 나오는 동안 음성 인식 중지
        answer_text = '사이다'
        speak(answer_text)
    elif '뭐야' in input_text:
        # 카메라로 객체 인식 후 구매하려는 물품 정보 음성 안내
        #answer_text = '인식된 물품은 {}입니다.' <- mqtt
        is_speaking = True  # 스피커 음성이 나오는 동안 음성 인식 중지
        answer_text = '사이다'
        speak(answer_text)
    elif '짐칸 열어' in input_text or '열어' in input_text :
        # 짐칸을 개폐하는 코드 추가
        is_speaking = True  # 스피커 음성이 나오는 동안 음성 인식 중지
        answer_text = '짐칸을 개폐합니다. 개폐 완료하였습니다.'
        speak(answer_text)
    elif '짐칸 닫아' in input_text or '닫아' in input_text:
        # 짐칸을 개폐하는 코드 추가
        is_speaking = True  # 스피커 음성이 나오는 동안 음성 인식 중지
        answer_text = '짐칸을 개폐합니다. 닫았습니다.'
        speak(answer_text)
    elif '출발지' in input_text or '돌아가' in input_text:
        # 카트를 출발지로 복귀시키는 코드 추가
        is_speaking = True  # 스피커 음성이 나오는 동안 음성 인식 중지
        answer_text = '출발지로 복귀합니다. 카트 종료 멘트!'
        speak(answer_text)
    elif '목적지 도착' in input_text: # mqtt
        is_speaking = True  # 스피커 음성이 나오는 동안 음성 인식 중지
        answer_text = '목적지에 도착했습니다. 음성알림을 드립니다.'
        speak(answer_text)
    else:
        is_speaking = True  # 스피커 음성이 나오는 동안 음성 인식 중지
        answer_text = '다시 한 번 말씀해주시겠어요?'
        speak(answer_text)
        # is_speaking = False
    is_speaking = False # 음성인식이 완료되면 False로 설정
    print("answer_is_speaking=False",is_speaking)
    print("test")
    
def listen_thread():
    global answer_is_speaking
    global listen_after_speak
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)

    while True:
        if not answer_is_speaking:
            if listen_after_speak:
                time.sleep(0.8)
                listen_after_speak = False

            with microphone as source:
                print("대기 중...")
                audio = recognizer.listen(source)
                listen(recognizer, audio)

def main():
    global answer_is_speaking
    speak('무엇을 도와드릴까요?')
    print(" 무엇을 도와드릴까요?")
    threading.Thread(target=listen_thread).start()

if __name__ == "__main__":
    main()
