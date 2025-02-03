import streamlit as st
from main import spin_wheel, check_win, color_map

# Inicjalizacja sesji
if "step" not in st.session_state:
    st.session_state.step = 1
if "bet_type" not in st.session_state:
    st.session_state.bet_type = None
if "bet_value" not in st.session_state:
    st.session_state.bet_value = None
if "result_number" not in st.session_state:
    st.session_state.result_number = None
if "game_message" not in st.session_state:
    st.session_state.game_message = ""

st.title("🎰 Ruletka Online")

# Etap 1: Powitanie
if st.session_state.step == 1:
    st.write("Witaj w grze w ruletkę!")
    if st.button("🎲 Rozpocznij grę"):
        st.session_state.step = 2
        st.rerun()

# Etap 2: Wybór zakładu
elif st.session_state.step == 2:
    st.write("🃏 Postaw swój zakład!")
    bet_type = st.radio("Wybierz typ zakładu:", ["Liczba", "Kolor"])

    if bet_type == "Liczba":
        st.session_state.bet_type = "number"
        st.session_state.bet_value = st.number_input("🎯 Wybierz liczbę (0-36)", min_value=0, max_value=36, step=1)
    else:
        st.session_state.bet_type = "color"
        st.session_state.bet_value = st.radio("🎨 Wybierz kolor:", ["red", "black", "green"])

    if st.button("✅ Zatwierdź zakład"):
        st.session_state.step = 3
        st.rerun()

# Etap 3: Losowanie i wynik
elif st.session_state.step == 3:
    st.write("🔄 Kręcimy kołem ruletki...")
    
    st.session_state.result_number = spin_wheel()
    st.session_state.game_message, is_win = check_win(
        st.session_state.bet_type, st.session_state.bet_value, st.session_state.result_number
    )

    if is_win:
        st.success(st.session_state.game_message)
    else:
        st.error(st.session_state.game_message)
    
    if st.button("🔁 Zagraj ponownie"):
        st.session_state.step = 1
        st.session_state.bet_type = None
        st.session_state.bet_value = None
        st.session_state.result_number = None
        st.session_state.game_message = ""
        st.rerun()
