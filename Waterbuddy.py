import streamlit as st
from datetime import datetime
import random
 
# Page configuration
st.set_page_config(
    page_title="Water Buddy - Your Hydration Companion",
    page_icon="💧",
    layout="wide"
)
 
# Custom CSS to match the original design
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@300;400;600;700;800&display=swap" rel="stylesheet">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@300;400;600;700;800&display=swap');
    
    * {
        font-family: 'Nunito', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f3e7f5 0%, #fce4ec 50%, #e8eaf6 100%);
    }
    
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #9333ea 0%, #ec4899 50%, #6366f1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .subtitle {
        font-size: 1.5rem;
        font-weight: 600;
        color: #374151;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .card {
        background: white;
        border-radius: 1.5rem;
        padding: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
    }
    
    .card-title {
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    .progress-container {
        text-align: center;
        padding: 2rem;
    }
    
    .buddy-container {
        width: 160px;
        height: 240px;
        border: 4px solid #93c5fd;
        border-radius: 0 0 80px 80px;
        background: linear-gradient(to top, #eff6ff, #cffafe);
        position: relative;
        overflow: hidden;
        margin: 0 auto;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .water-level {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        background: linear-gradient(to top, #60a5fa, #22d3ee);
        border-radius: 0 0 80px 80px;
        transition: height 0.8s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .buddy-face {
        font-size: 2.5rem;
        position: absolute;
        top: 1rem;
        left: 50%;
        transform: translateX(-50%);
        z-index: 10;
    }
    
    .intake-display {
        font-size: 2rem;
        font-weight: 800;
        color: #1e40af;
        margin-top: 1rem;
    }
    
    .progress-text {
        font-size: 1.1rem;
        font-weight: 600;
        color: #4b5563;
    }
    
    .motivation-text {
        font-size: 0.9rem;
        font-weight: 500;
        color: #9333ea;
        margin-top: 0.5rem;
    }
    
    .log-entry {
        background: linear-gradient(90deg, #eff6ff 0%, #ecfeff 100%);
        border-left: 4px solid #60a5fa;
        border-radius: 1rem;
        padding: 1rem;
        margin-bottom: 0.75rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .tip-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 1rem;
        margin-bottom: 1rem;
    }
    
    .tip-emoji {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    
    .tip-text {
        font-size: 1.1rem;
        font-weight: 600;
    }
    
    div[data-testid="stButton"] button {
        border-radius: 1rem;
        font-weight: 700;
        font-size: 1rem;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s;
    }
    
    .stNumberInput input {
        border-radius: 1rem;
        font-weight: 600;
        font-size: 1.1rem;
    }
    
    .stTextArea textarea {
        border-radius: 1rem;
        font-weight: 500;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)
 
# Initialize session state
if 'onboarding_complete' not in st.session_state:
    st.session_state.onboarding_complete = False
    st.session_state.current_step = 1
    st.session_state.selected_age = None
    st.session_state.selected_gender = None
    st.session_state.selected_activity = None
    st.session_state.age_emoji = '💪'
    st.session_state.standard_goal = 2500
    st.session_state.daily_goal = 2500
    st.session_state.current_intake = 0
    st.session_state.log_entries = []
    st.session_state.user_rating = 0
 
# Hydration tips
HYDRATION_TIPS = [
    "💧 Start your day with a big glass of water - your body loses water while you sleep!",
    "🍋 Add lemon, cucumber, or mint to make water more exciting and tasty!",
    "⏰ Set reminders every hour to take a few sips - small amounts throughout the day work best!",
    "🥤 Keep a water bottle with you always - if you see it, you'll drink it!",
    "🍉 Eat water-rich foods like watermelon, cucumber, and oranges for extra hydration!",
    "🌡️ Drink more water when it's hot outside or when you're exercising!",
    "☕ For every cup of coffee or tea, drink an extra glass of water!",
    "🎯 Use apps or mark your bottle to track your daily water intake!",
    "🧊 Ice-cold water can be more refreshing and encourage you to drink more!",
    "🏃‍♀️ Drink water before, during, and after exercise to stay properly hydrated!",
    "😴 Keep water by your bed for nighttime sips and morning hydration!",
    "🥗 Soups, smoothies, and herbal teas all count toward your daily water goal!"
]
 
MOTIVATIONAL_MESSAGES = [
    "You're doing amazing! 🌟",
    "Keep splashing! 💦",
    "Hydration hero in action! 🦸‍♀️",
    "You're on fire! 🔥",
    "Water warrior! ⚔️",
    "Fantastic progress! 🎉",
    "You're crushing it! 💪",
    "Splash-tastic! 🌊"
]
 
# Helper functions
def get_buddy_face_and_motivation(percentage):
    if percentage >= 100:
        return '🤩', "GOAL CRUSHED! You're a hydration legend! 🏆", '#10b981'
    elif percentage >= 75:
        return '😄', "Almost there, superstar! 🌟", '#60a5fa'
    elif percentage >= 50:
        return '😊', random.choice(MOTIVATIONAL_MESSAGES), '#22d3ee'
    elif percentage >= 25:
        return '🙂', "Great start! Keep the momentum going! 🚀", '#22d3ee'
    elif percentage > 0:
        return '😌', "Nice first splash! Let's keep going! 💧", '#22d3ee'
    else:
        return '😊', "Let's get started! 💪", '#22d3ee'
 
def add_water(amount):
    st.session_state.current_intake += amount
    time = datetime.now().strftime("%I:%M %p")
    fun_messages = ['Splash!', 'Glug glug!', 'Refreshing!', 'Hydrated!', 'Awesome!', 'Perfect!']
    message = random.choice(fun_messages)
    st.session_state.log_entries.insert(0, {'time': time, 'amount': amount, 'message': message})
    
    # Check goal achievement
    if st.session_state.current_intake >= st.session_state.daily_goal:
        st.balloons()
 
def reset_day():
    st.session_state.current_intake = 0
    st.session_state.log_entries = []
 
def restart_journey():
    st.session_state.onboarding_complete = False
    st.session_state.current_step = 1
    st.session_state.current_intake = 0
    st.session_state.log_entries = []
    st.session_state.user_rating = 0
 
# Onboarding Flow
if not st.session_state.onboarding_complete:
    st.markdown('<h1 class="main-title">💧 Water Buddy</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Your Fun Hydration Companion!</p>', unsafe_allow_html=True)
    
    # Step 1: Welcome
    if st.session_state.current_step == 1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div style="text-align: center; font-size: 4rem;">🌟</div>', unsafe_allow_html=True)
        st.markdown('<h2 style="text-align: center; color: #9333ea; font-size: 2rem; font-weight: 700;">Hey there, future hydration hero!</h2>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #4b5563;">Ready to make drinking water the most fun part of your day? Let\'s get to know you better!</p>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("Let's Start! 🚀", use_container_width=True, type="primary"):
                st.session_state.current_step = 2
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Step 2: Age Selection
    elif st.session_state.current_step == 2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div style="text-align: center; font-size: 4rem;">🎂</div>', unsafe_allow_html=True)
        st.markdown('<h2 style="text-align: center; color: #6366f1; font-size: 2rem; font-weight: 700;">What\'s your age group, buddy?</h2>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #4b5563;">This helps me suggest the perfect daily water goal for you!</p>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("🧒 6-12 years\nLittle Explorer", use_container_width=True):
                st.session_state.selected_age = '6-12'
                st.session_state.standard_goal = 1600
                st.session_state.age_emoji = '🧒'
                st.session_state.current_step = 3
                st.rerun()
        
        with col2:
            if st.button("🧑‍🎓 13-18 years\nTeen Champion", use_container_width=True):
                st.session_state.selected_age = '13-18'
                st.session_state.standard_goal = 2000
                st.session_state.age_emoji = '🧑‍🎓'
                st.session_state.current_step = 3
                st.rerun()
        
        with col3:
            if st.button("💪 19-50 years\nHydration Hero", use_container_width=True):
                st.session_state.selected_age = '19-50'
                st.session_state.standard_goal = 2500
                st.session_state.age_emoji = '💪'
                st.session_state.current_step = 3
                st.rerun()
        
        with col4:
            if st.button("🌟 65+ years\nWise Warrior", use_container_width=True):
                st.session_state.selected_age = '65+'
                st.session_state.standard_goal = 2200
                st.session_state.age_emoji = '🌟'
                st.session_state.current_step = 3
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Step 3: Gender Selection
    elif st.session_state.current_step == 3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div style="text-align: center; font-size: 4rem;">👥</div>', unsafe_allow_html=True)
        st.markdown('<h2 style="text-align: center; color: #9333ea; font-size: 2rem; font-weight: 700;">How do you identify?</h2>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #4b5563;">This helps me fine-tune your hydration recommendations!</p>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("👩 Female", use_container_width=True):
                st.session_state.selected_gender = 'female'
                st.session_state.standard_goal = round(st.session_state.standard_goal * 0.9)
                st.session_state.current_step = 4
                st.rerun()
        
        with col2:
            if st.button("👨 Male", use_container_width=True):
                st.session_state.selected_gender = 'male'
                st.session_state.standard_goal = round(st.session_state.standard_goal * 1.1)
                st.session_state.current_step = 4
                st.rerun()
        
        with col3:
            if st.button("🌈 Other", use_container_width=True):
                st.session_state.selected_gender = 'other'
                st.session_state.current_step = 4
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Step 4: Activity Level
    elif st.session_state.current_step == 4:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div style="text-align: center; font-size: 4rem;">🏃‍♀️</div>', unsafe_allow_html=True)
        st.markdown('<h2 style="text-align: center; color: #10b981; font-size: 2rem; font-weight: 700;">How active are you?</h2>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #4b5563;">More activity means more hydration needed!</p>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🛋️ Chill Mode\nMostly sitting/relaxing", use_container_width=True):
                st.session_state.selected_activity = 'low'
                st.session_state.standard_goal = round(st.session_state.standard_goal * 1.0)
                st.session_state.daily_goal = st.session_state.standard_goal
                st.session_state.onboarding_complete = True
                st.rerun()
        
        with col2:
            if st.button("🚶‍♀️ Active Life\nRegular walks/exercise", use_container_width=True):
                st.session_state.selected_activity = 'moderate'
                st.session_state.standard_goal = round(st.session_state.standard_goal * 1.2)
                st.session_state.daily_goal = st.session_state.standard_goal
                st.session_state.onboarding_complete = True
                st.rerun()
        
        with col3:
            if st.button("🏃‍♀️ Fitness Fanatic\nDaily intense workouts", use_container_width=True):
                st.session_state.selected_activity = 'high'
                st.session_state.standard_goal = round(st.session_state.standard_goal * 1.4)
                st.session_state.daily_goal = st.session_state.standard_goal
                st.session_state.onboarding_complete = True
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
 
# Main App
else:
    # Header
    st.markdown('<h1 class="main-title">💧 Water Buddy</h1>', unsafe_allow_html=True)
    st.markdown(f'<p class="subtitle">{st.session_state.age_emoji} Welcome back, hydration hero! Let\'s make today splash-tastic!</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔄 Start Over", use_container_width=True):
            restart_journey()
            st.rerun()
    
    # Goals and Converter Section
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<h3 class="card-title" style="color: #9333ea;">🎯 Your Hydration Goals</h3>', unsafe_allow_html=True)
        st.markdown(f'<div style="background: linear-gradient(90deg, #f3e8ff, #fce7f3); padding: 1rem; border-radius: 1rem; margin-bottom: 1rem;"><strong style="color: #9333ea;">Recommended:</strong> <span style="color: #7c3aed; font-weight: 800; font-size: 1.2rem; float: right;">{st.session_state.standard_goal} ml</span></div>', unsafe_allow_html=True)
        
        st.session_state.daily_goal = st.number_input(
            "Your Goal (ml):",
            min_value=500,
            max_value=5000,
            value=st.session_state.standard_goal,
            step=100,
            key="goal_input"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<h3 class="card-title" style="color: #6366f1;">🔄 Magic Converter</h3>', unsafe_allow_html=True)
        
        ml_value = st.number_input("Milliliters (ml):", min_value=0, value=0, step=50, key="ml_converter")
        cups_value = ml_value / 236.588 if ml_value > 0 else 0
        st.markdown(f'<div style="text-align: center; font-size: 1.5rem; margin: 1rem 0;">⇅</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="background: #e0e7ff; padding: 1rem; border-radius: 1rem; text-align: center;"><strong style="color: #6366f1;">Cups:</strong> <span style="font-weight: 800; font-size: 1.2rem; color: #4f46e5;">{cups_value:.2f}</span></div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Progress Visualization
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<h3 class="card-title" style="color: #1e40af;">🌊 Your Splash Progress</h3>', unsafe_allow_html=True)
    
    percentage = min((st.session_state.current_intake / st.session_state.daily_goal) * 100, 100)
    face, motivation, color = get_buddy_face_and_motivation(percentage)
    
    # Water Buddy Visualization
    st.markdown(f'''
    <div class="progress-container">
        <div class="buddy-container">
            <div class="water-level" style="height: {percentage}%; background: linear-gradient(to top, {color}, #22d3ee);"></div>
            <div class="buddy-face">{face}</div>
        </div>
        <div class="intake-display">{st.session_state.current_intake} ml</div>
        <div class="progress-text">{round(percentage)}% of goal</div>
        <div class="motivation-text">{motivation}</div>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Logging Section
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<h3 class="card-title" style="color: #10b981;">💧 Add Your Splash!</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Quick Splash Buttons**")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("+250 ml 🥤", use_container_width=True):
                add_water(250)
                st.rerun()
            if st.button("+750 ml 🧴", use_container_width=True):
                add_water(750)
                st.rerun()
        with c2:
            if st.button("+500 ml 🍶", use_container_width=True):
                add_water(500)
                st.rerun()
            if st.button("+1000 ml 🍼", use_container_width=True):
                add_water(1000)
                st.rerun()
    
    with col2:
        st.markdown("**Custom Splash**")
        custom_amount = st.number_input("Enter ml:", min_value=1, max_value=2000, value=250, step=50, key="custom_amount")
        if st.button("Add! 🎉", use_container_width=True, type="primary"):
            add_water(custom_amount)
            st.rerun()
    
    if st.button("🔄 Reset Today's Adventure", use_container_width=True):
        reset_day()
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Hydration Tips
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<h3 class="card-title" style="color: #9333ea;">💡 Buddy\'s Hydration Tips</h3>', unsafe_allow_html=True)
    
    if 'current_tip' not in st.session_state:
        st.session_state.current_tip = random.choice(HYDRATION_TIPS)
    
    st.markdown(f'''
    <div class="tip-card">
        <div class="tip-emoji">💧</div>
        <p class="tip-text">{st.session_state.current_tip}</p>
    </div>
    ''', unsafe_allow_html=True)
    
    if st.button("🎲 Get New Tip!", use_container_width=True):
        st.session_state.current_tip = random.choice(HYDRATION_TIPS)
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Hydration Log
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<h3 class="card-title" style="color: #6366f1;">📝 Today\'s Splash Log</h3>', unsafe_allow_html=True)
    
    if len(st.session_state.log_entries) == 0:
        st.markdown('<p style="text-align: center; color: #9ca3af; padding: 2rem; font-size: 1.1rem;">No splashes yet! Start your hydration journey! 🌊</p>', unsafe_allow_html=True)
    else:
        for entry in st.session_state.log_entries[:10]:  # Show last 10 entries
            st.markdown(f'''
            <div class="log-entry">
                <div>
                    <span style="color: #4b5563; font-weight: 600;">{entry['time']}</span>
                    <span style="margin-left: 0.5rem; color: #2563eb; font-weight: 700;">{entry['message']}</span>
                </div>
                <span style="font-weight: 800; color: #2563eb; font-size: 1.1rem;">+{entry['amount']} ml 💧</span>
            </div>
            ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Feedback Form
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<h3 class="card-title" style="color: #ec4899;">💌 Tell Water Buddy How We\'re Doing!</h3>', unsafe_allow_html=True)
    
    st.markdown("**How's your experience? ⭐**")
    rating = st.slider("", 0, 5, st.session_state.user_rating, key="rating_slider")
    st.session_state.user_rating = rating
    
    if rating > 0:
        st.markdown(f'<div style="font-size: 2rem; text-align: center;">{"🌟" * rating}{"⭐" * (5-rating)}</div>', unsafe_allow_html=True)
    
    feedback_text = st.text_area("Share your thoughts! 💭", placeholder="Tell us what you love or what we can improve...", key="feedback_text")
    
    if st.button("Send Feedback! 🚀", use_container_width=True, type="primary"):
        if rating == 0:
            st.warning("Please give us a star rating! ⭐")
        else:
            st.success(f"🎉 Thank you for your {rating}-star feedback! Water Buddy loves hearing from you! 💙")
            st.session_state.user_rating = 0
    
    st.markdown('</div>', unsafe_allow_html=True)
 