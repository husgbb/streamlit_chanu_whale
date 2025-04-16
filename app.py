import streamlit as st
import google.generativeai as genai
import os

################################################################################
################################################################################
#### 페이지 설정 
st.set_page_config(
    page_title="분자생물학 장인 찬우고래",
    page_icon="🐋",
    layout="centered"
)

################################################################################
################################################################################
#### API KEY 등록

try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except KeyError:
    st.error("Gemini API 키 설정 필요. Streamlit Cloud의 Secrets에 'GEMINI_API_KEY' 추가 요망.")
    st.stop()
except Exception as e:
    st.error(f"API 키 설정 중 오류 발생: {e}")
    st.stop()


################################################################################
################################################################################
#### model setting

system_prompt = """
You are a chatbot that speaks like 찬우고래 who speaks in korean. 
You should adhere to 찬우고래's unique way of speaking.
  1.  Use these sentence endings: "고래", "왈왈", "고롸롸롸", "알파카", "애옹"[cite: 1, 2, 3, 4, 5].
  2.  Use these fillers: 으, 음, 어, 허허[cite: 10, 14, 21].
  3.  Use Konglish such as 'Gogo'[cite: 88].
  4.  Use slang or abbreviations: ㄷㄷ, 깝, 욜로, 흠[cite: 10, 108, 15, 64].
  5.  Use emoticons appropriately: 이모티콘[cite: 1, 2, 3, 4, 5].
  6.  Make up words by adding letters: 냠냠, 쩝쩝, 츄릅[cite: 2, 9, 86].
  7.  Use hashtags: #샵검색[cite: 3, 4, 9, 10].
  8.  Use ㅇ as a placeholder: 읍, 읍니다[cite: 10, 3].
  9.  Elongate vowels: 넹, 넹넹, 넵[cite: 9, 9, 9].
 10.  Use interjections: 앗, 잌, 헐[cite: 21, 42, 55].
 11.  Refer to yourself in the third person: 본인[cite: 213].
 12.  Forget to complete your sentences: 오늘 날씨가[cite: 10, 67, 12, 90].
"""


model = genai.GenerativeModel(
    'gemini-2.0-flash', 
    system_instruction=system_prompt
)
chat = model.start_chat(history=[])




################################################################################
################################################################################
#### streamlit setting
if "messages" not in st.session_state:
    st.session_state.messages = [] # 메시지 기록 초기화

# 앱 제목
st.title("🐋분자생물학 장인 찬우고래")
st.write("과탑 정찬우와 함께하는 분자생물학 공부!")

# 이전 대화 내용 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 사용자 입력 처리 ---
if prompt := st.chat_input("찬우고래에게 분자생물학 관련 질문을 물어보세요!"):
    # 사용자 메시지 표시 및 기록
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gemini API 호출 및 응답 처리
    try:
        with st.spinner('찬우고래는 생각 중...'):
            response = chat.send_message(prompt)
        # AI 응답 표시 및 기록
        assistant_response = response.text
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        with st.chat_message("assistant"):
            st.markdown(assistant_response)
    except Exception as e:
        st.error(f"Gemini API 호출 중 오류 발생: {e}")