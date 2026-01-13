import streamlit as st
import pandas as pd

# ==========================================
# 1. 核心數據層 (Layer 1: Data Kernel)
# ==========================================
# 將 PDF 數據結構化
schedule = {
    "W1 (基礎累積)": {
        "D1": [
            {"Lift": "深蹲 (Squat)", "Weight": "50-65 kg", "Sets": 5, "Reps": 5, "RPE": "6-7", "Note": "節奏穩定"},
            {"Lift": "臥推 (Bench)", "Weight": "25-27.5 kg", "Sets": 5, "Reps": 5, "RPE": "6", "Note": "停頓確實"},
            {"Lift": "輔項: 死蟲式", "Weight": "自重", "Sets": 3, "Reps": "15", "RPE": "-", "Note": "核心抗伸展"},
            {"Lift": "輔項: 保加利亞蹲", "Weight": "自重/輕負重", "Sets": 3, "Reps": "10", "RPE": "-", "Note": "單腳穩定"},
        ],
        "D2": [
            {"Lift": "硬舉 (Deadlift)", "Weight": "50-65 kg", "Sets": 5, "Reps": 4, "RPE": "6-7", "Note": "背部張力"},
            {"Lift": "臥推 (Bench)", "Weight": "20-27.5 kg", "Sets": 6, "Reps": 4, "RPE": "6", "Note": "推速度"},
            {"Lift": "輔項: 棒式", "Weight": "自重", "Sets": 3, "Reps": "1 min", "RPE": "-", "Note": "核心張力"},
            {"Lift": "輔項: 窄握臥推", "Weight": "RPE 7", "Sets": 3, "Reps": "8", "RPE": "7", "Note": "三頭肌"},
        ],
        "D3": [
            {"Lift": "深蹲 (Squat)", "Weight": "55-70 kg", "Sets": 5, "Reps": 3, "RPE": "7", "Note": "專注發力"},
            {"Lift": "臥推 (Bench)", "Weight": "27.5-30 kg", "Sets": 5, "Reps": 3, "RPE": "7", "Note": "路徑一致"},
            {"Lift": "輔項: 側棒式", "Weight": "自重", "Sets": 3, "Reps": "45s", "RPE": "-", "Note": "抗側向位移"},
            {"Lift": "輔項: 早安運動", "Weight": "輕", "Sets": 3, "Reps": "10", "RPE": "-", "Note": "後側鏈"},
        ]
    },
    "W2 (負荷高峰)": {
        "D1": [
            {"Lift": "深蹲 (Squat)", "Weight": "60-75 kg", "Sets": "2+4", "Reps": "5/3", "RPE": "7-8", "Note": "強度提升"},
            {"Lift": "臥推 (Bench)", "Weight": "25-30 kg", "Sets": "2+4", "Reps": "5/3", "RPE": "7-8", "Note": "控制離心"},
            {"Lift": "輔項: 鳥狗式", "Weight": "自重", "Sets": 3, "Reps": "12", "RPE": "-", "Note": "對角線穩定"},
            {"Lift": "輔項: 啞鈴划船", "Weight": "RPE 8", "Sets": 3, "Reps": "12", "RPE": "-", "Note": "上背肌群"},
        ],
        "D2": [
            {"Lift": "硬舉 (Deadlift)", "Weight": "60-75 kg", "Sets": "3+4", "Reps": "5/4", "RPE": "8", "Note": "注意下背"},
            {"Lift": "臥推 (Bench)", "Weight": "20-25 kg", "Sets": "3+4", "Reps": "5/5", "RPE": "7", "Note": "累積容量"},
            {"Lift": "輔項: 懸吊舉腿", "Weight": "自重", "Sets": 3, "Reps": "12", "RPE": "-", "Note": "腹直肌"},
            {"Lift": "輔項: 臉拉", "Weight": "輕", "Sets": 3, "Reps": "15", "RPE": "-", "Note": "肩膀健康"},
        ],
        "D3": [
            {"Lift": "深蹲 (Squat)", "Weight": "60-80 kg", "Sets": "2/2/2/4", "Reps": "4/4/3/3", "RPE": "8-9", "Note": "金字塔組"},
            {"Lift": "臥推 (Bench)", "Weight": "25-30 kg", "Sets": "2+5", "Reps": "5/3", "RPE": "8-9", "Note": "重量適應"},
            {"Lift": "輔項: 高箱深蹲", "Weight": "RPE 8", "Sets": 3, "Reps": "8", "RPE": "-", "Note": "動作控制"},
            {"Lift": "輔項: 俄羅斯轉體", "Weight": "藥球", "Sets": 3, "Reps": "20", "RPE": "-", "Note": "旋轉核心"},
        ]
    },
    "W3 (技術精煉)": {
        "D1": [
            {"Lift": "臥推 (Bench) - 1", "Weight": "20-27.5 kg", "Sets": "2+4", "Reps": "5/3", "RPE": "7", "Note": "第一輪推"},
            {"Lift": "深蹲 (Squat)", "Weight": "65-80 kg", "Sets": "3+4", "Reps": "5/3", "RPE": "8-9", "Note": "大重量組"},
            {"Lift": "臥推 (Bench) - 2", "Weight": "22.5-25 kg", "Sets": "2+4", "Reps": "5/5", "RPE": "7", "Note": "疲勞下控管"},
            {"Lift": "輔項: 俯臥撐", "Weight": "自重", "Sets": 3, "Reps": "AMRAP", "RPE": "10", "Note": "力竭組"},
            {"Lift": "輔項: 負重棒式", "Weight": "+5-10kg", "Sets": 3, "Reps": "45s", "RPE": "-", "Note": "加強核心"},
        ],
        "D2": [
            {"Lift": "硬舉 (Deadlift)", "Weight": "65-80 kg", "Sets": "3+5", "Reps": "5/4", "RPE": "8-9", "Note": "技術極限前奏"},
            {"Lift": "臥推 (Bench)", "Weight": "20-25 kg", "Sets": "2+5", "Reps": "5/5", "RPE": "7", "Note": "恢復性訓練"},
            {"Lift": "輔項: 屈體划船", "Weight": "RPE 8", "Sets": 3, "Reps": "10", "RPE": "-", "Note": "保持腹內壓"},
            {"Lift": "輔項: 抗旋轉", "Weight": "繩索/彈力帶", "Sets": 3, "Reps": "12", "RPE": "-", "Note": "核心穩定"},
        ],
        "D3": [
            {"Lift": "深蹲 (Squat)", "Weight": "60-75 kg", "Sets": "3+5", "Reps": "4/3", "RPE": "8", "Note": "最後重訓日"},
            {"Lift": "臥推 (Bench)", "Weight": "22.5-30 kg", "Sets": "2+6", "Reps": "5/2", "RPE": "8-9", "Note": "強度適中"},
            {"Lift": "輔項: 啞鈴飛鳥", "Weight": "輕", "Sets": 3, "Reps": "12", "RPE": "-", "Note": "胸大肌伸展"},
            {"Lift": "輔項: 超人式", "Weight": "自重", "Sets": 3, "Reps": "15", "RPE": "-", "Note": "下背耐力"},
        ]
    },
    "W4 (減量/測驗)": {
        "D1": [
            {"Lift": "深蹲 (Squat)", "Weight": "45-55 kg", "Sets": "3+3", "Reps": "4/3", "RPE": "5", "Note": "Deload 輕鬆蹲"},
            {"Lift": "臥推 (Bench)", "Weight": "20 kg", "Sets": 3, "Reps": 3, "RPE": "5", "Note": "Deload 輕鬆推"},
            {"Lift": "輔項", "Weight": "-", "Sets": "-", "Reps": "-", "RPE": "-", "Note": "主動恢復 (滾筒/伸展)"},
        ],
        "D2": [
            {"Lift": "深蹲 (Squat)", "Weight": "40 kg", "Sets": 2, "Reps": 2, "RPE": "4", "Note": "極輕重量"},
            {"Lift": "臥推 (Bench)", "Weight": "15 kg", "Sets": 2, "Reps": 2, "RPE": "4", "Note": "極輕重量"},
             {"Lift": "輔項", "Weight": "-", "Sets": "-", "Reps": "-", "RPE": "-", "Note": "準備測驗"},
        ],
        "D3 (測驗日)": [
            {"Lift": "深蹲 (Squat) 1RM", "Weight": "MAX", "Sets": "-", "Reps": "1", "RPE": "9-10", "Note": "目標: 100+"},
            {"Lift": "臥推 (Bench) 1RM", "Weight": "MAX", "Sets": "-", "Reps": "1", "RPE": "9-10", "Note": "目標: 37.5+"},
            {"Lift": "硬舉 (Deadlift) 1RM", "Weight": "MAX", "Sets": "-", "Reps": "1", "RPE": "9-10", "Note": "目標: 100+"},
        ]
    }
}

# ==========================================
# 2. 介面層 (Layer 0: UI/UX Shell)
# ==========================================
st.set_page_config(page_title="書嫻 Powerlifting Log", page_icon="🏋️‍♀️", layout="centered")

# CSS 優化：加大手機上的字體與按鈕
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        height: 3em;
        font-weight: bold;
        border-radius: 10px;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        border-left: 5px solid #ff4b4b;
    }
    h1 {
        text-align: center;
        color: #0e1117;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏋️‍♀️ 書嫻一月備賽日誌")

# --- 選擇器 ---
col1, col2 = st.columns(2)
with col1:
    selected_week = st.selectbox("選擇週次", list(schedule.keys()))
with col2:
    selected_day = st.selectbox("選擇訓練日", ["D1", "D2", "D3"])

# --- 數據讀取 ---
todays_workout = schedule[selected_week][selected_day]

# --- 顯示訓練卡片 ---
st.markdown(f"### 📅 {selected_week} - {selected_day}")
st.markdown("---")

# 進度條 (視覺化當日進度)
progress = 0
total_exercises = len(todays_workout)

for i, exercise in enumerate(todays_workout):
    # 使用 Container 模擬卡片效果
    with st.container():
        # 標題區
        st.subheader(f"🔹 {exercise['Lift']}")
        
        # 核心數據區 (三欄布局)
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("重量 (kg)", exercise['Weight'])
        with c2:
            st.metric("組數", exercise['Sets'])
        with c3:
            st.metric("次數", exercise['Reps'])
        
        # 附加資訊
        st.caption(f"🎯 RPE: {exercise['RPE']} | 📝 Note: {exercise['Note']}")
        
        # 互動區：組數追蹤
        # 如果組數是數字，生成對應數量的 Checkbox
        if isinstance(exercise['Sets'], int):
            cols = st.columns(exercise['Sets'])
            for j in range(exercise['Sets']):
                key = f"{selected_week}_{selected_day}_{exercise['Lift']}_set_{j}"
                cols[j].checkbox(f"Set {j+1}", key=key)
        else:
            # 如果組數是文字 (如 "2+4")，給一個簡單的完成按鈕
            st.checkbox("✅ 完成所有組數", key=f"{selected_week}_{selected_day}_{exercise['Lift']}_done")
            
    st.markdown("---")

# --- 底部筆記區 ---
st.text_area("訓練後筆記 (感受度/疼痛/調整)", height=100)

if st.button("💾 儲存今日訓練 (模擬)"):
    st.success("訓練記錄已保存！(Layer 1: Data Persisted)")
    st.balloons()