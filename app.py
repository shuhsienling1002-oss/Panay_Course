import streamlit as st
import pandas as pd
from datetime import date

# ==========================================
# 0. 全局設定與核彈級 CSS (Layer 0: Total Blackout UI)
# ==========================================
st.set_page_config(page_title="PWR-LIFT | 書嫻專屬", page_icon="⚡", layout="centered")

# 注入 CSS：強制覆蓋所有元件內部的顏色
st.markdown("""
    <style>
    /* 1. 網頁總背景：純黑 */
    .stApp {
        background-color: #000000 !important;
    }
    
    /* 2. 所有文字：強制純白 */
    h1, h2, h3, h4, h5, h6, p, label, span, div {
        color: #FFFFFF !important;
    }
    
    /* 3. 輸入框 (Input/Number/Text) 內部構造修正 */
    /* 針對輸入框容器 */
    div[data-baseweb="input"] {
        background-color: #1E1E1E !important;
        border-color: #444444 !important;
        color: white !important;
    }
    /* 針對輸入框內的文字 */
    input.st-ai, textarea.st-ai {
        color: #FFFFFF !important; 
    }
    
    /* 4. 下拉選單 (Selectbox) 修正 */
    div[data-baseweb="select"] > div {
        background-color: #1E1E1E !important;
        color: white !important;
        border-color: #444444 !important;
    }
    /* 下拉後的選單項目 (這是最難改的，必須抓特定層級) */
    ul[data-baseweb="menu"] {
        background-color: #1E1E1E !important;
    }
    li[data-baseweb="option"] {
        color: white !important;
    }
    
    /* 5. 數字輸入框 (Number Input) 的加減按鈕 */
    button[kind="secondary"] {
        background-color: #333333 !important;
        color: white !important;
        border: 1px solid #555 !important;
    }

    /* 6. 訓練卡片 (Card) */
    .workout-card {
        background-color: #111111;
        border: 1px solid #333;
        border-left: 6px solid #00C6FF; /* 藍色亮條 */
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(255, 255, 255, 0.05);
    }
    
    /* 7. 數據顯色 */
    .stat-label {
        color: #888888 !important;
        font-size: 0.8rem;
        letter-spacing: 1px;
    }
    .stat-value {
        color: #00C6FF !important; /* 螢光藍 */
        font-size: 1.6rem;
        font-weight: 900;
    }
    .stat-value-secondary {
        color: #FF4B4B !important; /* 螢光紅 */
        font-size: 1.6rem;
        font-weight: 900;
    }
    
    /* 8. 備註區塊 (紅黑高對比) */
    .note-box {
        background-color: #2b0c0c; /* 深紅黑 */
        border: 1px solid #ff4b4b;
        color: #ffffff !important;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    
    /* 9. 按鈕 (Button) */
    .stButton > button {
        background-color: #00C6FF !important;
        color: #000000 !important;
        font-weight: bold;
        border-radius: 8px;
        border: none;
    }
    .stButton > button:hover {
        background-color: #ffffff !important;
        box-shadow: 0 0 10px #00C6FF;
    }
    
    /* 10. Checkbox */
    .stCheckbox label span {
        color: #dddddd !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 1. 核心數據層 (保持完整)
# ==========================================
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
        },
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
# 2. 介面層：全黑化現代佈局 (Layer 0: Total Dark Mode UI)
# ==========================================

# --- 頂部 Header ---
st.markdown("<h1 style='text-align: center; color: #00C6FF !important;'>⚡ PWR-LIFT LOG</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888888 !important;'>M1 47kg Class | Road to April 4th</p>", unsafe_allow_html=True)

# 比賽倒數計算
target_date = date(2026, 4, 4)
today = date.today()
days_left = (target_date - today).days

# 儀表板
col1, col2, col3 = st.columns(3)
col1.metric("Days Out", f"{days_left}")
col2.metric("Target", "240+ kg")
col3.metric("BW", "49.0 kg")

st.markdown("---")

# --- 選擇器 (已經過 CSS 強力修正為黑底白字) ---
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
        <strong style="color: #FF4B4B;">💡 COACH'S NOTE:</strong><br>
        {todays_data["Day_Note"]}
    </div>
    ''', unsafe_allow_html=True)

# --- 邏輯分歧：測驗日 vs 訓練日 ---
if "IsTestDay" in todays_data and todays_data["IsTestDay"]:
    st.markdown('<h2 style="text-align:center; color:#FF4B4B !important;">🏆 TESTING DAY</h2>', unsafe_allow_html=True)
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
            st.balloons()
            st.success(f"🎉 TOTAL: {total} kg! Data Logged.")

else:
    # --- 訓練卡片渲染 Loop ---
    exercises = todays_data["Exercises"]
    
    # 完成度
    st.caption("WORKOUT PROGRESS")
    st.progress(0)
    
    for i, ex in enumerate(exercises):
        # 動作標題卡
        st.markdown(f"""
        <div class="workout-card">
            <div style="font-size: 1.3rem; font-weight: bold; color: white;">{ex['Lift']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # 數據區
        c1, c2, c3 = st.columns([1.5, 1, 1])
        with c1:
            st.markdown(f"<div class='stat-label'>WEIGHT</div><div class='stat-value'>{ex['Weight']}<span style='font-size:1rem; color:#888;'>kg</span></div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div class='stat-label'>SETS</div><div class='stat-value-secondary'>{ex['Sets']}</div>", unsafe_allow_html=True)
        with c3:
            st.markdown(f"<div class='stat-label'>REPS</div><div class='stat-value-secondary'>{ex['Reps']}</div>", unsafe_allow_html=True)
            
        st.markdown(f"<div style='color:#CCCCCC; margin-top:5px; margin-bottom:10px;'>🎯 RPE: {ex['RPE']} | 📝 {ex['Note']}</div>", unsafe_allow_html=True)
        
        # Checkbox 互動區
        if isinstance(ex['Sets'], int):
            cols = st.columns(ex['Sets'])
            for j in range(ex['Sets']):
                cols[j].checkbox(f"S{j+1}", key=f"{selected_week}_{selected_day}_{ex['Lift']}_{j}")
        else:
             st.checkbox("✅ ALL SETS DONE", key=f"{selected_week}_{selected_day}_{ex['Lift']}_all")
        
        st.markdown("<div style='margin-bottom: 25px;'></div>", unsafe_allow_html=True)

    # --- 底部筆記 ---
    st.markdown("---")
    st.markdown("### 📝 SESSION LOG")
    st.text_area("筆記區 (Note)", height=100, placeholder="紀錄一下今天的 RPE 或哪裡痠痛...")
    
    if st.button("💾 SAVE WORKOUT"):
        st.success("SESSION SAVED.")
        st.balloons()
