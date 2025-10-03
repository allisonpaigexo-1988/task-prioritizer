import streamlit as st
import pandas as pd
from datetime import datetime
import dateparser

# ---------- Functions ----------
def parse_deadline(deadline_text):
    if deadline_text:
        return dateparser.parse(deadline_text, settings={"PREFER_DATES_FROM": "future"})
    return None

def assign_priority(deadline, importance):
    now = datetime.now()
    if deadline:
        days_left = (deadline - now).days
    else:
        days_left = 999  # No deadline

    # Basic rules
    if days_left <= 1:
        return "Urgent"
    elif days_left <= 3:
        return "High"
    elif days_left <= 7:
        return "Medium"
    else:
        return "Low" if importance == "low" else "Medium"

# ---------- Streamlit UI ----------
st.set_page_config(page_title="AI Task Prioritizer", page_icon="✅")
st.title("AI Task Prioritizer for Administrative Professionals")

st.write("Enter tasks below with deadlines and importance. The app will suggest priorities.")

# Input form
task_list = []
with st.form("task_form", clear_on_submit=True):
    task_name = st.text_input("Task")
    deadline = st.text_input("Deadline (e.g., 'tomorrow', 'Oct 5', 'in 2 weeks')")
    importance = st.selectbox("Importance", ["high", "medium", "low"])
    submitted = st.form_submit_button("Add Task")
    if submitted and task_name:
        task_list.append({"task": task_name, "deadline": deadline, "importance": importance})

# Save tasks persistently in session
if "tasks" not in st.session_state:
    st.session_state["tasks"] = []

if task_list:
    st.session_state["tasks"].extend(task_list)

# Process tasks
if st.session_state["tasks"]:
    for task in st.session_state["tasks"]:
        task["parsed_deadline"] = parse_deadline(task["deadline"])
        task["priority"] = assign_priority(task["parsed_deadline"], task["importance"])

    df = pd.DataFrame(st.session_state["tasks"])
    priority_order = {"Urgent": 1, "High": 2, "Medium": 3, "Low": 4}
    df["priority_rank"] = df["priority"].map(priority_order)
    df = df.sort_values(by="priority_rank")

    st.subheader("📋 Prioritized Task List")
    st.dataframe(df[["task", "deadline", "importance", "priority"]], use_container_width=True)

    # Optional: Suggested daily plan
    st.subheader("🗓️ Suggested Daily Plan")
    urgent_tasks = df[df["priority"] == "Urgent"]["task"].tolist()
    high_tasks = df[df["priority"] == "High"]["task"].tolist()
    medium_tasks = df[df["priority"] == "Medium"]["task"].tolist()

    if urgent_tasks:
        st.write("**Morning:** " + ", ".join(urgent_tasks))
    if high_tasks:
        st.write("**Afternoon:** " + ", ".join(high_tasks))
    if medium_tasks:
        st.write("**Later this week:** " + ", ".join(medium_tasks))

# Reset button
if st.button("Reset All Tasks"):
    st.session_state["tasks"] = []
