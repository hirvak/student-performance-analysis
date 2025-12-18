import streamlit as st
import pandas as pd

# ------------------ PAGE TITLE ------------------
st.title("🎓 Student Performance Analysis System")

# ------------------ LOAD DATA ------------------
df = pd.read_csv("cleaned_data.csv")

# Add Total column if not present
if "Total" not in df.columns:
    df["Total"] = df["Maths"] + df["Science"] + df["English"]

# Add Rank column
df["Rank"] = df["Total"].rank(ascending=False, method="dense").astype(int)

# Add RollNo if not present
if "RollNo" not in df.columns:
    df.insert(0, "RollNo", range(1, len(df) + 1))

# ------------------ SIDEBAR MENU ------------------
st.sidebar.title("Menu")
option = st.sidebar.selectbox(
    "Choose an option",
    (
        "Show all students",
        "Show topper",
        "Subject-wise analysis",
        "Class performance",
        "Student-wise result"
    )
)

# ------------------ MENU FEATURES ------------------

# 1. Show all students
if option == "Show all students":
    st.subheader("All Student Records")
    st.dataframe(df)
    st.write("**Total number of students:**", len(df))

# 2. Show topper
elif option == "Show topper":
    st.subheader("Class Topper")

    highest_marks = df["Total"].max()
    topper = df[df["Total"] == highest_marks].iloc[0]

    st.success(f"Topper: {topper['Name']}")
    col1, col2, col3 = st.columns(3)

    col1.metric("Maths", topper["Maths"])
    col2.metric("Science", topper["Science"])
    col3.metric("English", topper["English"])

    st.write("**Total Marks:**", topper["Total"])
    st.write("**Rank:**", topper["Rank"])

# 3. Subject-wise analysis
elif option == "Subject-wise analysis":
    st.subheader("Subject-wise Analysis")

    subjects = ["Maths", "Science", "English"]
    for sub in subjects:
        st.markdown(f"### {sub}")
        st.write("Average:", df[sub].mean())
        st.write("Highest:", df[sub].max())
        st.write("Lowest :", df[sub].min())

    st.subheader("Average Marks Comparison")
    st.bar_chart(df[["Maths", "Science", "English"]].mean())

# 4. Class performance
elif option == "Class performance":
    st.subheader("Class Performance")

    class_avg = df["Total"].mean()

    st.write("**Average Total Score:**", class_avg)
    st.write("**Students above average:**", (df["Total"] > class_avg).sum())
    st.write("**Students below average:**", (df["Total"] < class_avg).sum())

# 5. Student-wise result
elif option == "Student-wise result":
    st.subheader("Student-wise Result")

    roll = st.number_input(
        "Enter Roll Number",
        min_value=1,
        max_value=int(df["RollNo"].max()),
        step=1
    )

    if st.button("Show Result"):
        student = df[df["RollNo"] == roll]

        if student.empty:
            st.error("Student not found!")
        else:
            student = student.iloc[0]

            st.success("Result Found")
            st.write("**Roll No:**", student["RollNo"])
            st.write("**Name:**", student["Name"])

            col1, col2, col3 = st.columns(3)
            col1.metric("Maths", student["Maths"])
            col2.metric("Science", student["Science"])
            col3.metric("English", student["English"])

            st.write("**Total Marks:**", student["Total"])
            st.write("**Rank:**", student["Rank"])

# ------------------ FOOTER ------------------
st.markdown("---")
st.caption("Built using Python, Pandas & Streamlit")
