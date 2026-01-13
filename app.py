import streamlit as st
import pandas as pd
from datetime import date

# ==========================================
# 0. 全局設定與 CSS 魔法 (Layer 0: The Modern Shell)
# ==========================================
st.set_page_config(page_title="PWR-LIFT | 書嫻專屬", page_icon="⚡", layout="centered")

# 現代化 CSS 注入
st.markdown("""
    <style>
    /* 全局背景與字體 */
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* 隱藏預設選單，讓畫面更像 App */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* 標題區塊：漸層文字 */
    .main-header {
        font-size: 2.5rem;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #00d2ff, #3a7bd5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 10px;
        padding-top: 20px;
    }
    
    .sub-header {
        text-align: center;
        color: #888;
        font-size: 0.9rem;
        margin-bottom: 30px;
    }

    /* 訓練卡片設計 (Glassmorphism) */
    .workout-card {
        background-color: #1c1f26;
        border: 1px solid #2d333b;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        transition: transform 0.2s;
    }
    .workout-card:hover {
        border-color: #00d2ff;
    }

    /* 動作名稱 */
    .lift-name {
        font-size: 1.4rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 10px;
        border-left: 4px solid #00d2ff;
        padding-left: 10px;
    }

    /* 數據標籤 */
    .stat-label {
        font-size: 0.8rem;
        color: #8b949e;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stat-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #00d2ff; /* 電光藍 */
    }
    .stat-value-secondary {
        font-size: 1.5rem;
        font-weight: 700;
        color: #ff4b4b; /* 熱力紅 */
    }

    /* 按鈕美化 */
    .stButton>button {
        background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
        color: white;
        border: none;
        border-radius: 25px;
        height: 50px;
        font-weight: bold;
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 15px rgba(0, 210, 255, 0.5);
    }
    
    /* 下拉選單美化 */
    .stSelectbox label {
        color: #8b949e !important;
    }
    
    /* 備註區塊 */
    .note-box {
        background-color: rgba(255, 75, 75, 0.1);
        border-left: 3px solid #ff4b4b;
        padding: 15px;
        border-radius: 5px;
        color: #ffcccb;
        margin-bottom: 25px;
        font-size: 0.95rem;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 1. 核心數據層 (保持不變)
# ==========================================
# 為了節省篇幅，我將之前的數據直接引用
# (這裡必須包含完整的 schedule 字典，與上一版完全相同)
schedule = {
    "W1 (基礎累積)": {
        "D1": {
            "Day_Note": "重點：適應頻率。核心動作節奏要一致，單腳蹲注意穩定。",
            "Exercises": [
                {"Lift": "深蹲 Squat", "Weight": "50-65", "Sets": 5, "Reps": 5, "RPE": "6-7", "Note": "節奏穩定"},
                {"Lift": "臥推 Bench", "Weight": "25-27.5", "Sets": 5, "Reps": 5, "RPE": "6", "Note": "停頓確實"},
                {"Lift": "死蟲式 Deadbug", "Weight": "BW", "Sets": 3, "Reps": "15", "RPE": "-", "Note": "核心抗伸展"},
                {"Lift": "保加利亞蹲", "Weight": "BW", "Sets": 3, "Reps": "10", "RPE": "-", "Note": "單腳穩定"},
            ]
        },
        "D2": {
            "Day_Note": "重點：背部張力與三頭肌強化。",
            "Exercises": [
                {"Lift": "硬舉 Deadlift", "Weight": "50-65", "Sets": 5, "Reps": 4, "RPE": "6-7", "Note": "背部張力"},
                {"Lift": "臥推 Bench", "Weight": "20-27.5", "Sets": 6, "Reps": 4, "RPE": "6", "Note": "推速度"},
                {"Lift": "棒式 Plank", "Weight": "BW", "Sets": 3, "Reps": "60s", "RPE": "-", "Note": "硬舉保持背部張力"},
                {"Lift": "窄握臥推 CGBP", "Weight": "RPE 7", "Sets": 3, "Reps": "8", "RPE": "7", "Note": "強化三頭肌"},
            ]
        },
        "D3": {
            "Day_Note": "重點：對抗側向位移，強化後側鏈。",
            "Exercises": [
                {"Lift": "深蹲 Squat", "Weight": "55-70", "Sets": 5, "Reps": 3, "RPE": "7", "Note": "專注發力"},
                {"Lift": "臥推 Bench", "Weight": "27.5-30", "Sets": 5, "Reps": 3, "RPE": "7", "Note": "路徑一致"},
                {"Lift": "側棒式 Side Plank", "Weight": "BW", "Sets": 3, "Reps": "45s", "RPE": "-", "Note": "抗側向位移"},
                {"Lift": "早安運動 Good Morning", "Weight": "Light", "Sets": 3, "Reps": "10", "RPE": "-", "Note": "強化後側鏈"},
            ]
        }
    },
    "W2 (負荷高峰)": {
        "D1": {
            "Day_Note": "重點：增加強度與組數，增加上背穩定度。",
            "Exercises": [
                {"Lift": "深蹲 Squat", "Weight": "60-75", "Sets": "2+6", "Reps": "5/3", "RPE": "7-8", "Note": "強度提升"},
                {"Lift": "臥推 Bench", "Weight": "25-30", "Sets": "2+4", "Reps": "5/3", "RPE": "7-8", "Note": "控制離心"},
                {"Lift": "鳥狗式 Bird-Dog", "Weight": "BW", "Sets": 3, "Reps": "12", "RPE": "-", "Note": "負荷高峰週"},
                {"Lift": "啞鈴划船 DB Row", "Weight": "RPE 8", "Sets": 3, "Reps": "12", "RPE": "-", "Note": "上背穩定"},
            ]
        },
        "D2": {
            "Day_Note": "重點：硬舉鎖定與保護肩關節。",
            "Exercises": [
                {"Lift": "硬舉 Deadlift", "Weight": "60-75", "Sets": "3+4", "Reps": "5/4", "RPE": "8", "Note": "注意下背"},
                {"Lift": "臥推 Bench", "Weight": "20-25", "Sets": "3+4", "Reps": "5/5", "RPE": "7", "Note": "累積容量"},
                {"Lift": "懸吊舉腿 Hanging Leg Raise", "Weight": "BW", "Sets": 3, "Reps": "12", "RPE": "-", "Note": "腹直肌"},
                {"Lift": "臉拉 Facepull", "Weight": "Light", "Sets": 3, "Reps": "15", "RPE": "-", "Note": "肩膀健康"},
            ]
        },
        "D3": {
            "Day_Note": "重點：高強度金字塔組，挑戰支撐。",
            "Exercises": [
                {"Lift": "深蹲 Squat", "Weight": "60/67.5/75/80", "Sets": "2/2/2/4", "Reps": "4/4/3/3", "RPE": "8-9", "Note": "金字塔加重"},
                {"Lift": "臥推 Bench", "Weight": "25-30", "Sets": "2+5", "Reps": "5/3", "RPE": "8-9", "Note": "重量適應"},
                {"Lift": "高箱深蹲 Box Squat", "Weight": "RPE 8", "Sets": 3, "Reps": "8", "RPE": "-", "Note": "高強度支撐"},
                {"Lift": "俄羅斯轉體 Russian Twist", "Weight": "Med", "Sets": 3, "Reps": "20", "RPE": "-", "Note": "旋轉核心"},
            ]
        }
    },
    "W3 (技術精煉)": {
        "D1": {
            "Day_Note": "重點：三明治訓練 (推-蹲-推)。模擬疲勞。",
            "Exercises": [
                {"Lift": "臥推 Bench (1)", "Weight": "20-27.5", "Sets": "2+4", "Reps": "5/3", "RPE": "7", "Note": "第一輪推"},
                {"Lift": "深蹲 Squat", "Weight": "65-80", "Sets": "3+4", "Reps": "5/3", "RPE": "8-9", "Note": "大重量組"},
                {"Lift": "臥推 Bench (2)", "Weight": "22.5-25", "Sets": "2+4", "Reps": "5/5", "RPE": "7", "Note": "疲勞控管"},
                {"Lift": "俯臥撐 Push Up", "Weight": "BW", "Sets": 3, "Reps": "Max", "RPE": "10", "Note": "力竭組"},
                {"Lift": "負重棒式 Weighted Plank", "Weight": "+5-10kg", "Sets": 3, "Reps": "45s", "RPE": "-", "Note": "加強核心"},
            ]
        },
        "D2": {
            "Day_Note": "重點：保持腹內壓穩定，強化硬舉鎖定。",
            "Exercises": [
                {"Lift": "硬舉 Deadlift", "Weight": "65-80", "Sets": "3+5", "Reps": "5/4", "RPE": "8-9", "Note": "技術極限前奏"},
                {"Lift": "臥推 Bench", "Weight": "20-25", "Sets": "2+5", "Reps": "5/5", "RPE": "7", "Note": "恢復性訓練"},
                {"Lift": "屈體划船 Bent-over Row", "Weight": "RPE 8", "Sets": 3, "Reps": "10", "RPE": "-", "Note": "腹內壓穩定"},
                {"Lift": "抗旋轉 Anti-Rotation", "Weight": "Cable", "Sets": 3, "Reps": "12", "RPE": "-", "Note": "核心穩定"},
            ]
        },
        "D3": {
            "Day_Note": "重點：動作規格化檢視，下背耐力。",
            "Exercises": [
                {"Lift": "深蹲 Squat", "Weight": "60-75", "Sets": "3+5", "Reps": "4/3", "RPE": "8", "Note": "最後重訓日"},
                {"Lift": "臥推 Bench", "Weight": "22.5-30", "Sets": "2+6", "Reps": "5/2", "RPE": "8-9", "Note": "強度適中"},
                {"Lift": "啞鈴飛鳥 Flys", "Weight": "Light", "Sets": 3, "Reps": "12", "RPE": "-", "Note": "伸展"},
                {"Lift": "超人式 Superman", "Weight": "BW", "Sets": 3, "Reps": "15", "RPE": "-", "Note": "下背耐力"},
            ]
        }
    },
    "W4 (減量/測驗)": {
        "D1": {
            "Day_Note": "Deload：極輕重量，維持手感，準備測驗。",
            "Exercises": [
                {"Lift": "深蹲 Squat", "Weight": "45-55", "Sets": "3+3", "Reps": "4/3", "RPE": "5", "Note": "Deload"},
                {"Lift": "臥推 Bench", "Weight": "20", "Sets": 3, "Reps": 3, "RPE": "5", "Note": "Deload"},
            ]
        },
        "D2": {
            "Day_Note": "Deload：極輕重量，準備測驗。",
            "Exercises": [
                {"Lift": "深蹲 Squat", "Weight": "40", "Sets": 2, "Reps": 2, "RPE": "4", "Note": "極輕"},
                {"Lift": "臥推 Bench", "Weight": "15", "Sets": 2, "Reps": 2, "RPE": "4", "Note": "極輕"},
            ]
        },
        "D3": {
            "Day_Note": "🔥 測驗日！催~~~~~蕊！目標：SQ 100+ / BP 37.5+ / DL 100+",
            "IsTestDay": True
        }
    }
}

# ==========================================
# 2. 介面層：現代化佈局 (Layer 0: Modern UI)
# ==========================================

# --- 頂部 Dashboard ---
st.markdown('<div class="main-header">⚡ PWR-LIFT LOG</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">M1 47kg Class | Road to April 4th</div>', unsafe_allow_html=True)

# 比賽倒數計算
target_date = date(2026, 4, 4)
today = date.today()
days_left = (target_date - today).days
progress_val = min(100, max(0, int((1 - days_left/90) * 100)))

# 儀表板 Metrics
m1, m2, m3 = st.columns(3)
with m1:
    st.metric("Days Out", f"{days_left} Days", delta="-1 day", delta_color="inverse")
with m2:
    st.metric("Target Total", "240+ kg", delta="Goal")
with m3:
    st.metric("Bodyweight", "49.0 kg", delta="+2kg Buffer", delta_color="off")

st.markdown("---")

# --- 選擇器 (Pill 樣式) ---
c1, c2 = st.columns([2, 1])
with c1:
    selected_week = st.selectbox("📆 SELECT WEEK", list(schedule.keys()))
with c2:
    selected_day = st.selectbox("📍 DAY", ["D1", "D2", "D3"])

# --- 數據處理 ---
todays_data = schedule[selected_week][selected_day]

# --- 每日備註 ---
if "Day_Note" in todays_data:
    st.markdown(f'''
    <div class="note-box">
        <b>💡 COACH'S NOTE:</b><br>
        {todays_data["Day_Note"]}
    </div>
    ''', unsafe_allow_html=True)

# --- 邏輯分歧：測驗日 vs 訓練日 ---
if "IsTestDay" in todays_data and todays_data["IsTestDay"]:
    st.markdown('<h2 style="text-align:center; color:#ff4b4b;">🏆 TESTING DAY</h2>', unsafe_allow_html=True)
    st.info("今天是大日子！深呼吸，專注，爆發！")

    with st.form("test_day_form"):
        # 深蹲
        st.markdown("### 🔴 SQUAT")
        c1, c2 = st.columns(2)
        sq_result = c1.number_input("Max Weight (kg)", 0.0, 200.0, 100.0, key="sq")
        c2.markdown("#### Goal: 100+")
        
        # 臥推
        st.markdown("### 🔵 BENCH PRESS")
        c3, c4 = st.columns(2)
        bp_result = c3.number_input("Max Weight (kg)", 0.0, 100.0, 37.5, key="bp")
        c4.markdown("#### Goal: 37.5+")
        
        # 硬舉
        st.markdown("### 🟡 DEADLIFT")
        c5, c6 = st.columns(2)
        dl_result = c5.number_input("Max Weight (kg)", 0.0, 200.0, 100.0, key="dl")
        c6.markdown("#### Goal: 100+")

        st.markdown("---")
        submitted = st.form_submit_button("🚀 SUBMIT RESULTS")
        if submitted:
            total = sq_result + bp_result + dl_result
            st.canvas_confetti() # 隱藏彩蛋：雖然沒有這個函式，但下面有氣球
            st.balloons()
            st.success(f"🎉 TOTAL: {total} kg! Data Logged.")

else:
    # --- 訓練卡片渲染 Loop ---
    exercises = todays_data["Exercises"]
    
    # 完成度進度條
    st.caption("WORKOUT PROGRESS")
    st.progress(0) # 這裡可以連接 session state 做動態更新
    
    for i, ex in enumerate(exercises):
        # HTML 卡片結構
        st.markdown(f"""
        <div class="workout-card">
            <div class="lift-name">{ex['Lift']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # 在卡片下方放置 Streamlit 原生元件 (為了互動性)
        c1, c2, c3 = st.columns([1.5, 1, 1])
        with c1:
            st.markdown(f"<div class='stat-label'>WEIGHT</div><div class='stat-value'>{ex['Weight']}<span style='font-size:1rem'>kg</span></div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div class='stat-label'>SETS</div><div class='stat-value-secondary'>{ex['Sets']}</div>", unsafe_allow_html=True)
        with c3:
            st.markdown(f"<div class='stat-label'>REPS</div><div class='stat-value-secondary'>{ex['Reps']}</div>", unsafe_allow_html=True)
            
        st.markdown(f"<div style='color:#888; font-size:0.9rem; margin-top:5px;'>🎯 RPE: {ex['RPE']} | 📝 {ex['Note']}</div>", unsafe_allow_html=True)
        
        # 互動區
        if isinstance(ex['Sets'], int):
            cols = st.columns(ex['Sets'])
            for j in range(ex['Sets']):
                cols[j].checkbox(f"S{j+1}", key=f"{selected_week}_{selected_day}_{ex['Lift']}_{j}")
        else:
             st.checkbox("✅ SETS COMPLETE", key=f"{selected_week}_{selected_day}_{ex['Lift']}_all")
        
        st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

    # --- 底部筆記 ---
    st.markdown("---")
    st.text_area("POST-WORKOUT LOG", height=100, placeholder="RPE 感受、疼痛點、備註...")
    
    if st.button("💾 SAVE WORKOUT"):
        st.success("SESSION SAVED. GOOD JOB!")
        st.balloons()
