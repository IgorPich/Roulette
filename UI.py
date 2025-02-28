import streamlit as st
import time
import random  # used for simulating spinning numbers
from main import spin_wheel, check_win, color_map
import microtransactions  # import modułu z mikrotransakcjami

# ------------------------------------------------------------------
# Session State Initialization
# Initialize required session variables once. Note that 'balance'
# is saved between games and starts at 1000 credits.
# ------------------------------------------------------------------
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
if "balance" not in st.session_state:
    st.session_state.balance = 1000  # starting balance (persists between games)
if "bet_amount" not in st.session_state:
    st.session_state.bet_amount = 0

# Title for the Streamlit app
st.title("MEGA BIG WIN ONLY CASINO")

# ------------------------------------------------------------------
# Stage 1: Welcome Screen
# Display a welcome message along with the user's current balance.
# Clicking the button moves to the bet placement stage.
# ------------------------------------------------------------------
if st.session_state.step == 1:
    st.write("Welcome to the place where money lies on a floor!")

    
    # Button to move to the bet placement stage
    if st.button("Begin the game!"):
        st.session_state.step = 2
        # IMPORTANT: rerun the app so that the UI updates immediately
        st.rerun()

# ------------------------------------------------------------------
# Stage 2: Bet Placement
# The player selects the bet amount (validated against their balance),
# chooses a bet type (number or color), and then specifies the bet value.
# The user can also go to microtransactions shop at any time.
# ------------------------------------------------------------------
elif st.session_state.step == 2:
    st.write("Place your bet!")
    st.write(f"Your account is : {st.session_state.balance} credits")
    
    # Button to top up balance. Goes immediately to microtransactions.
    if st.button("Recharge your account"):
        st.session_state.step = "microtransactions"
        st.rerun()

    # Input for bet amount; the input is restricted to available balance.
    # If the user has 0 balance, they can only bet 1 if they top up first
    # or reduce the bet. Otherwise, they can press "Doładuj konto."
    st.session_state.bet_amount = st.number_input(
        "Place your bet amount:", 
        min_value=1, 
        max_value=st.session_state.balance, 
        step=1
    )
    
    # Let the user choose the type of bet.
    bet_type = st.radio("Choose bet type:", ["Number", "Color"])
    
    # Depending on bet type, present the corresponding input field.
    if bet_type == "Number":
        st.session_state.bet_type = "number"
        st.session_state.bet_value = st.number_input(
            "Choose number from (0-36)", 
            min_value=0, 
            max_value=36, 
            step=1
        )
    else:
        st.session_state.bet_type = "color"
        st.session_state.bet_value = st.radio(
            "Choose color:", 
            ["Red", "Black", "Green"]
        )
    
    # Confirm the bet; extra validation ensures the bet amount does not exceed the balance.
    if st.button("Let's roll the wheel!"):
        if st.session_state.bet_amount > st.session_state.balance:
            st.error("Nuh uh. You don't have enough money!")
        else:
            # Move to the spinning stage
            st.session_state.step = 3
            st.rerun()

# ------------------------------------------------------------------
# Stage 3: Spin the Wheel and Process Result
# Simulate the roulette spinning with a visual effect. The displayed
# numbers change over a few seconds. After simulation, perform the
# actual spin, update the balance (ensuring it never goes negative),
# and then automatically return to the bet placement stage (Stage 2).
# ------------------------------------------------------------------
elif st.session_state.step == 3:
    st.write("🔄 Kręcimy kołem ruletki...")

    # Wyświetlenie animowanej ruletki (upewnij się, że plik 'roulette.gif' istnieje)
    roulette_animation = st.empty()
    roulette_animation.image("roulette.gif", use_container_width =True)
    # Animacja będzie wyświetlana przez 3 sekundy (możesz dostosować czas)
    time.sleep(3)
    # Usuwamy animację
    roulette_animation.empty()

    try:
        # Po animacji wykonujemy prawdziwy spin
        st.session_state.result_number = spin_wheel()
    except Exception as e:
        st.error(f"Błąd przy losowaniu: {e}")
        st.stop()

    # Pobranie koloru dla wylosowanego numeru
    result_color = color_map.get(st.session_state.result_number, "N/A")
    st.write(f"Wylosowany numer: {st.session_state.result_number} ({result_color})")

    try:
        st.session_state.game_message, is_win = check_win(
            st.session_state.bet_type, 
            st.session_state.bet_value, 
            st.session_state.result_number
        )
    except Exception as e:
        st.error(f"Błąd przy sprawdzaniu wyniku: {e}")
        st.stop()

    if is_win:
        if st.session_state.bet_type == "number":
            payout = st.session_state.bet_amount * 35
        elif st.session_state.bet_type == "color":
            if st.session_state.bet_value.lower() == "green":
                payout = st.session_state.bet_amount * 17
            else:
                payout = st.session_state.bet_amount
        st.session_state.balance += payout
        st.success(f"{st.session_state.game_message} Wygrałeś {payout} kredytów!")
    else:
        st.session_state.balance = max(0, st.session_state.balance - st.session_state.bet_amount)
        st.error(f"{st.session_state.game_message} Straciłeś {st.session_state.bet_amount} kredytów!")

    st.write(f"Nowe saldo: {st.session_state.balance} kredytów")

    if st.session_state.balance <= 0:
        st.error("Brak środków! Gra zakończona.")
        if st.button("Recharge your account"):
            st.session_state.step = "microtransactions"
            st.rerun()
    else:
        st.success("Za chwilę wrócisz do ekranu zakładu...")
        time.sleep(3)
        st.session_state.step = 2
        st.session_state.bet_type = None
        st.session_state.bet_value = None
        st.session_state.result_number = None
        st.session_state.game_message = ""
        st.rerun()


# ------------------------------------------------------------------
# Stage "microtransactions": Top-up Shop
# Here we show the user the shop from microtransactions.py
# After purchase, it sets step = 2 and re-runs automatically.
# ------------------------------------------------------------------
elif st.session_state.step == "microtransactions":
    # This function will display the microtransactions screen,
    # let the user buy credits, and then return them to stage 2.
    microtransactions.show_microtransactions()
