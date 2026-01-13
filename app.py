import streamlit as st
import pandas as pd

# ==========================================
# 1. 核心數據層 (Layer 1: Data Kernel) - v2.0 修正版
# ==========================================
schedule = {
    "W1 (基礎累積)": {
        "D1": {
            "Day_Note": "重點：適應頻率。核心動作節奏要一致，單腳蹲注意穩定。",
            "Exercises": [
                {"Lift": "深蹲 (Squat)", "Weight": "50-65 kg", "Sets": 5, "Reps": 5, "RPE": "6-7", "Note": "節奏穩定"},
                {"Lift": "臥推 (Bench)", "Weight": "25-27.5 kg", "Sets": 5, "Reps": 5, "RPE": "6", "Note": "停頓確實"},
                {"Lift": "輔項: 死蟲式", "Weight": "自重", "Sets": 3, "Reps": "15", "RPE": "-", "Note": "重點在於動作節奏一致"},
                {"Lift": "輔項: 保加利亞蹲", "Weight": "自重", "Sets": 3, "Reps": "10", "RPE": "-", "Note": "臥推收肩胛穩定"},
            ]
        },
        "D2": {
            "Day_Note": "重點：背部張力與三頭肌強化。",
            "Exercises": [
                {"Lift": "硬舉 (Deadlift)", "Weight": "50-65 kg", "Sets": 5, "Reps": 4, "RPE": "6-7", "Note": "背部張力"},
                {"Lift": "臥推 (Bench)", "Weight": "20-27.5 kg", "Sets": 6, "Reps": 4, "RPE": "6", "Note": "推速度"},
                {"Lift": "輔項: 棒式", "Weight": "自重", "Sets": 3, "Reps": "1 min", "RPE": "-", "Note": "硬舉保持背部張力"},
                {"Lift": "輔項: 窄握臥推", "Weight": "RPE 7", "Sets": 3, "Reps": "8", "RPE": "7", "Note": "強化三頭肌撐起力量"},
            ]
        },
        "D3": {
            "Day_Note": "重點：對抗側向位移，強化後側鏈。",
            "Exercises": [
                {"Lift": "深蹲 (Squat)", "Weight": "55-70 kg", "Sets": 5, "Reps": 3, "RPE": "7", "Note": "專注發力"},
                {"Lift": "臥推 (Bench)", "Weight": "27.5-30 kg", "Sets": 5, "Reps": 3, "RPE": "7", "Note": "路徑一致"},
                {"Lift": "輔項: 側棒式", "Weight": "自重", "Sets": 3, "Reps": "45s", "RPE": "-", "Note": "核心對抗側向位移"},
                {"Lift": "輔項: 早安運動", "Weight": "輕", "Sets": 3, "Reps": "10", "RPE": "-", "Note": "強化後側鏈穩定"},
            ]
        }
    },
    "W2 (負荷高峰)": {
        "D1": {
            "Day_Note": "重點：增加強度與組數，增加上背穩定度。",
            "Exercises": [
                {"Lift": "深蹲 (Squat)", "Weight": "60-75 kg", "Sets": "2+6", "Reps": "5/3", "RPE": "7-8", "Note": "強度提升"},
                {"Lift": "臥推 (Bench)", "Weight": "25-30 kg", "Sets": "2+4", "Reps": "5/3", "RPE": "7-8", "Note": "控制離心"},
                {"Lift": "輔項: 鳥狗式", "Weight": "自重", "Sets": 3, "Reps": "12", "RPE": "-", "Note": "負荷高峰週開始"},
                {"Lift": "輔項: 啞鈴划船", "Weight": "RPE 8", "Sets": 3, "Reps": "12", "RPE": "-", "Note": "增加上背穩定度"},
            ]
        },
        "D2": {
            "Day_Note": "重點：硬舉鎖定與保護肩關節。",
            "Exercises": [
                {"Lift": "硬舉 (Deadlift)", "Weight": "60-75 kg", "Sets": "3+4", "Reps": "5/4", "RPE": "8", "Note": "注意下背"},
                {"Lift": "臥推 (Bench)", "Weight": "20-25 kg", "Sets": "3+4", "Reps": "5/5", "RPE": "7", "Note": "累積容量"},
                {"Lift": "輔項: 懸吊舉腿", "Weight": "自重", "Sets": 3, "Reps": "12", "RPE": "-", "Note": "硬舉至膝蓋停頓 1秒"},
                {"Lift": "輔項: 臉拉 (Facepull)", "Weight": "輕", "Sets": 3, "Reps": "15", "RPE": "-", "Note": "保護肩關節穩定"},
            ]
        },
        "D3": {
            "Day_Note": "重點：高強度金字塔組，挑戰支撐。",
            "Exercises": [
                # 修正：詳細列出每一層的重量
                {"Lift": "深蹲 (Squat)", "Weight": "60 / 67.5 / 75 / 80 kg", "Sets": "2/2/2/4", "Reps": "4/4/3/3", "RPE": "8-9", "Note": "金字塔加重 (Pyramid)"},
                {"Lift": "臥推 (Bench)", "Weight": "25-30 kg", "Sets": "2+5", "Reps": "5/3", "RPE": "8-9", "Note": "重量適應"},
                {"Lift": "輔項: 高箱深蹲", "Weight": "RPE 8", "Sets": 3, "Reps": "8", "RPE": "-", "Note": "(坐姿)挑戰較高強度支撐"},
                {"Lift": "輔項: 俄羅斯轉體", "Weight": "藥球", "Sets": 3, "Reps": "20", "RPE": "-", "Note": "強化旋轉抗力"},
            ]
        }
    },
    "W3 (技術精煉)": {
        "D1": {
            "Day_Note": "重點：三明治訓練 (推-蹲-推)。模擬疲勞。",
            "Exercises": [
                {"Lift": "臥推 (Bench) - 1", "Weight": "20-27.5 kg", "Sets": "2+4", "Reps": "5/3", "RPE": "7", "Note": "第一輪推"},
                {"Lift": "深蹲 (Squat)", "Weight": "65-80 kg", "Sets": "3+4", "Reps": "5/3", "RPE": "8-9", "Note": "大重量組"},
                {"Lift": "臥推 (Bench) - 2", "Weight": "22.5-25 kg", "Sets": "2+4", "Reps": "5/5", "RPE": "7", "Note": "疲勞下控管"},
                {"Lift": "輔項: 俯臥撐", "Weight": "自重", "Sets": 3, "Reps": "Max", "RPE": "10", "Note": "拆分訓練"},
                {"Lift": "輔項: 負重棒式", "Weight": "+5-10kg", "Sets": 3, "Reps": "45s", "RPE": "-", "Note": "先推再蹲，模擬疲勞"},
            ]
        },
        "D2": {
            "Day_Note": "重點：保持腹內壓穩定，強化硬舉鎖定。",
            "Exercises": [
                {"Lift": "硬舉 (Deadlift)", "Weight": "65-80 kg", "Sets": "3+5", "Reps": "5/4", "RPE": "8-9", "Note": "技術極限前奏"},
                {"Lift": "臥推 (Bench)", "Weight": "20-25 kg", "Sets": "2+5", "Reps": "5/5", "RPE": "7", "Note": "恢復性訓練"},
                {"Lift": "輔項: 屈體划船", "Weight": "RPE 8", "Sets": 3, "Reps": "10", "RPE": "-", "Note": "全程保持腹內壓穩定"},
                {"Lift": "輔項: 核心抗旋轉", "Weight": "繩索/彈力帶", "Sets": 3, "Reps": "12", "RPE": "-", "Note": "強化硬舉鎖定穩定"},
            ]
        },
        "D3": {
            "Day_Note": "重點：動作規格化檢視，下背耐力。",
            "Exercises": [
                {"Lift": "深蹲 (Squat)", "Weight": "60-75 kg", "Sets": "3+5", "Reps": "4/3", "RPE": "8", "Note": "最後重訓日"},
                {"Lift": "臥推 (Bench)", "Weight": "22.5-30 kg", "Sets": "2+6", "Reps": "5/2", "RPE": "8-9", "Note": "強度適中"},
                {"Lift": "輔項: 啞鈴飛鳥", "Weight": "輕", "Sets": 3, "Reps": "12", "RPE": "-", "Note": "臥推動作規格化檢視"},
                {"Lift": "輔項: 超人式", "Weight": "自重", "Sets": 3, "Reps": "15", "RPE": "-", "Note": "下背與核心耐力"},
            ]
        }
    },
    "W4 (減量/測驗)": {
        "D1": {
            "Day_Note": "Deload：極輕重量，維持手感，準備測驗。",
            "Exercises": [
                {"Lift": "深蹲 (Squat)", "Weight": "45-55 kg", "Sets": "3+3", "Reps": "4/3", "RPE": "5", "Note": "Deload 輕鬆蹲"},
                {"Lift": "臥推 (Bench)", "Weight": "20 kg", "Sets": 3, "Reps": 3, "RPE": "5", "Note": "Deload 輕鬆推"},
            ]
        },
        "D2": {
            "Day_Note": "Deload：極輕重量，準備測驗。",
            "Exercises": [
                {"Lift": "深蹲 (Squat)", "Weight": "40 kg", "Sets": 2, "Reps": 2, "RPE": "4", "Note": "極輕重量"},
                {"Lift": "臥推 (Bench)", "Weight": "15 kg", "Sets": 2, "Reps": 2, "RPE": "4", "Note": "極輕重量"},
            ]
        },
        # W4-D3 特殊處理：測驗日
        "D3": {
            "Day_Note": "🔥 測驗日！催~~~~~蕊！目標：SQ 100+ / BP 37.5+ / DL 100+",
            "IsTestDay": True  # 標記為測驗日
        }
    }
}

# ==========================================
# 2. 介面層 (Layer 0: UI/UX Shell)
# ==========================================
st.set_page_config(page_title="書嫻 Powerlifting Log", page_icon="🏋️‍♀️", layout="centered")

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
    .note-box {
        background-color: #e8f4f8;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #b3e0ff;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏋️‍♀️ 書嫻一月備賽日誌 v2.0")

# --- 選擇器 ---
col1, col2 = st.columns(2)
with col1:
    selected_week = st.selectbox("選擇週次", list(schedule.keys()))
with col2:
    selected_day = st.selectbox("選擇訓練日", ["D1", "D2", "D3"])

# --- 數據讀取 ---
todays_data = schedule[selected_week][selected_day]

# --- 顯示每日備註 (Day Note) ---
if "Day_Note" in todays_data:
    st.markdown(f'<div class="note-box">💡 <b>本日教練備註：</b>{todays_data["Day_Note"]}</div>', unsafe_allow_html=True)

st.markdown("---")

# --- 邏輯分歧：一般訓練日 vs 測驗日 ---

# 情況 A: W4-D3 測驗日 (Test Day Logic)
if "IsTestDay" in todays_data and todays_data["IsTestDay"]:
    st.header("🏆 測驗日 (Testing Day)")
    st.info("今天是大日子！請填寫妳測到的最大重量。注意安全，不要受傷！")
    
    with st.form("test_day_form"):
        c1, c2 = st.columns(2)
        with c1:
            sq_result = st.number_input("深蹲 (Squat) 成績", min_value=0.0, value=100.0, step=2.5)
        with c2:
            st.caption("目標: 100+")
            
        c3, c4 = st.columns(2)
        with c3:
            bp_result = st.number_input("臥推 (Bench) 成績", min_value=0.0, value=37.5, step=1.25)
        with c4:
            st.caption("目標: 37.5+")
            
        c5, c6 = st.columns(2)
        with c5:
            dl_result = st.number_input("硬舉 (Deadlift) 成績", min_value=0.0, value=100.0, step=2.5)
        with c6:
            st.caption("目標: 100+")
            
        notes = st.text_area("測驗心得 / 身體狀況", placeholder="例如：深蹲起得來但有點前傾...")
        
        submitted = st.form_submit_button("🚀 送出測驗成績")
        
        if submitted:
            st.success(f"成績已記錄！總和: {sq_result + bp_result + dl_result} kg")
            st.balloons()
            # 這裡可以加入儲存邏輯

# 情況 B: 一般訓練日 (Normal Training Logic)
else:
    todays_workout = todays_data["Exercises"]
    
    # 進度條 (視覺化當日進度)
    progress = 0
    
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
        st.success("訓練記錄已保存！")
