import streamlit as st
import pandas as pd
from datetime import datetime

# ==========================================
# 0. 系統核心 (Layer 0: Session State Kernel)
# ==========================================
st.set_page_config(page_title="書嫻訓練日誌", page_icon="🏋️‍♀️")

# 初始化：確保記憶體裡有一個 DataFrame 可以存資料
if 'log_df' not in st.session_state:
    st.session_state['log_df'] = pd.DataFrame(columns=["Date", "Week", "Day", "Type", "Squat", "Bench", "Deadlift", "Note"])

# ==========================================
# 1. 側邊欄：存檔與讀檔區 (File I/O)
# ==========================================
with st.sidebar:
    st.header("📂 檔案管理中心")
    st.info("💡 邏輯：每次練完請「下載」保存；下次要練時請先「上傳」舊檔。")
    
    # --- A. 讀取舊檔 ---
    uploaded_file = st.file_uploader("1️⃣ 上傳上次的 CSV (讀檔)", type=["csv"])
    if uploaded_file is not None:
        try:
            # 讀取上傳的檔案並更新到記憶體
            uploaded_df = pd.read_csv(uploaded_file)
            st.session_state['log_df'] = uploaded_df
            st.success(f"✅ 成功讀取！包含 {len(uploaded_df)} 筆歷史紀錄。")
        except Exception as e:
            st.error("⚠️ 檔案格式錯誤，請確認是正確的 CSV。")

    st.markdown("---")

    # --- B. 下載新檔 ---
    # 將目前的記憶體轉成 CSV
    csv_data = st.session_state['log_df'].to_csv(index=False).encode('utf-8')
    
    st.download_button(
        label="2️⃣ 下載最新紀錄 (存檔)",
        data=csv_data,
        file_name="gym_history.csv",
        mime="text/csv",
        type="primary"  # 讓按鈕變顯眼
    )

# ==========================================
# 2. 寫入資料函數 (更新 Session State)
# ==========================================
def save_to_session(week, day, type_of_day, sq_val, bp_val, dl_val, note):
    new_entry = pd.DataFrame([{
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "Week": week,
        "Day": day,
        "Type": type_of_day,
        "Squat": sq_val,
        "Bench": bp_val,
        "Deadlift": dl_val,
        "Note": note
    }])
    
    # 將新資料合併到 Session State
    st.session_state['log_df'] = pd.concat([st.session_state['log_df'], new_entry], ignore_index=True)

# ==========================================
# 3. 課表數據 (完整保留)
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
# 4. 介面層
# ==========================================

st.title("🏋️‍♀️ 書嫻一月備賽日誌")
st.caption("M1 47kg Class | Road to April 4th")

# 建立分頁
tab1, tab2 = st.tabs(["🔥 今日訓練", "📜 歷史數據 (請定期下載)"])

# --- Tab 1: 今日訓練 ---
with tab1:
    c1, c2 = st.columns([2, 1])
    with c1:
        selected_week = st.selectbox("選擇週次", list(schedule.keys()))
    with c2:
        selected_day = st.selectbox("選擇訓練日", ["D1", "D2", "D3"])

    todays_data = schedule[selected_week][selected_day]

    # 教練備註
    if "Day_Note" in todays_data:
        st.info(f"💡 教練備註：{todays_data['Day_Note']}")
    
    st.divider()

    # 邏輯分歧：測驗日 vs 訓練日
    if "IsTestDay" in todays_data and todays_data["IsTestDay"]:
        st.header("🏆 測驗日 (Testing Day)")
        st.warning("今天是大日子！請注意安全。")

        with st.form("test_day_form"):
            st.subheader("🔴 深蹲 (Squat)")
            c1, c2 = st.columns(2)
            sq_result = c1.number_input("成績 (kg)", min_value=0.0, value=100.0, key="sq")
            c2.markdown("**目標: 100+**")
            
            st.subheader("🔵 臥推 (Bench Press)")
            c3, c4 = st.columns(2)
            bp_result = c3.number_input("成績 (kg)", min_value=0.0, value=37.5, key="bp")
            c4.markdown("**目標: 37.5+**")
            
            st.subheader("🟡 硬舉 (Deadlift)")
            c5, c6 = st.columns(2)
            dl_result = c5.number_input("成績 (kg)", min_value=0.0, value=100.0, key="dl")
            c6.markdown("**目標: 100+**")
            
            note_test = st.text_area("測驗心得")

            st.divider()
            submitted = st.form_submit_button("🚀 儲存測驗成績")
            
            if submitted:
                save_to_session(selected_week, selected_day, "Testing", sq_result, bp_result, dl_result, note_test)
                st.balloons()
                st.success("🎉 成績已暫存！請記得按側邊欄的「下載」按鈕來保存檔案。")

    else:
        # 一般訓練日
        exercises = todays_data["Exercises"]
        for ex in exercises:
            st.subheader(f"🔹 {ex['Lift']}")
            c1, c2, c3 = st.columns(3)
            c1.metric("重量 (kg)", ex['Weight'])
            c2.metric("組數", ex['Sets'])
            c3.metric("次數", ex['Reps'])
            st.caption(f"🎯 RPE: {ex['RPE']} | 📝 {ex['Note']}")
            
            if isinstance(ex['Sets'], int):
                cols = st.columns(ex['Sets'])
                for j in range(ex['Sets']):
                    cols[j].checkbox(f"Set {j+1}", key=f"{selected_week}_{selected_day}_{ex['Lift']}_{j}")
            else:
                st.checkbox("✅ 完成", key=f"{selected_week}_{selected_day}_{ex['Lift']}_all")
            st.divider()

        user_note = st.text_area("訓練筆記", height=100, placeholder="紀錄一下...")
        
        if st.button("💾 儲存今日訓練"):
            save_to_session(selected_week, selected_day, "Training", "-", "-", "-", user_note)
            st.success("✅ 紀錄已暫存！請記得按側邊欄的「下載」按鈕來保存檔案。")

# --- Tab 2: 歷史紀錄 ---
with tab2:
    st.header("📊 目前的紀錄數據")
    st.caption("這裡顯示的是您「目前讀取中」的資料。")
    
    if not st.session_state['log_df'].empty:
        st.dataframe(st.session_state['log_df'].iloc[::-1], use_container_width=True)
    else:
        st.info("目前沒有資料。請上傳舊檔，或開始新的訓練紀錄。")
