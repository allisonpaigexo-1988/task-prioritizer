import streamlit as st

st.title("AI Task Prioritizer for Administrative Professionals")

# Task input
st.header("Add a Task")
task = st.text_input("Task description")
deadline = st.text_input("Deadline (e.g. tomorrow, in 3 days, next week)")
importance = st.selectbox("Importance", ["High", "Medium", "Low"])

if "tasks" not in st.session_state:
    st.session_state["tasks"] = []

if st.button("Add Task"):
    st.session_state["tasks"].append({"task": task, "deadline": deadline, "importance": importance})
    st.success(f"Added: {task}")

# Show and prioritize tasks
st.header("Prioritized Task List")
if st.session_state["tasks"]:
    # Sort: high → medium → low
    priority_order = {"High": 1, "Medium": 2, "Low": 3}
    sorted_tasks = sorted(st.session_state["tasks"], key=lambda x: priority_order[x["importance"]])
    
    for t in sorted_tasks:
        st.write(f"**{t['task']}** — Deadline: {t['deadline']} — Importance: {t['importance']}")
else:
    st.write("No tasks yet! Add one above.")
