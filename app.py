import streamlit as st
import pyodbc

# DATABASE CONNECTION
conn = pyodbc.connect(
'DRIVER={ODBC Driver 17 for SQL Server};'
'SERVER=DESKTOP-F68V2GL;'
'DATABASE=Exam;'
'Trusted_Connection=yes;'
)

cursor = conn.cursor()

# SESSION LOGIN
if "admin_login" not in st.session_state:
    st.session_state.admin_login = False

st.title("Smart Examination Seating Arrangement System")

menu = ["Admin Login","Student Login"]
choice = st.sidebar.selectbox("Select Login",menu)

# ================= ADMIN LOGIN =================

if choice == "Admin Login":

    if st.session_state.admin_login == False:

        st.subheader("Admin Login")

        username = st.text_input("Username")
        password = st.text_input("Password",type="password")

        if st.button("Login"):

            cursor.execute(
            "SELECT * FROM Admin1 WHERE username=? AND password=?",
            username,password)

            data = cursor.fetchone()

            if data:
                st.session_state.admin_login = True
                st.success("Login Successful")
                st.rerun()
            else:
                st.error("Invalid Login")

# ================= ADMIN DASHBOARD =================

    else:

        st.sidebar.success("Admin Logged In")

        if st.sidebar.button("Logout"):
            st.session_state.admin_login = False
            st.rerun()

        admin_menu = [
        "Add Room",
        "Add Student",
        "Generate Seating",
        "View Seating",
        "Delete Student",
        "Delete Room"
        ]

        option = st.sidebar.selectbox("Admin Menu",admin_menu)

# -------- ADD ROOM --------

        if option == "Add Room":

            st.subheader("Add Room")

            room_name = st.text_input("Room Name")
            capacity = st.number_input("Capacity",min_value=1)

            if st.button("Add Room"):

                cursor.execute(
                "INSERT INTO Rooms1(room_name,capacity) VALUES (?,?)",
                room_name,capacity)

                conn.commit()

                st.success("Room Added Successfully")

# -------- ADD STUDENT --------

        elif option == "Add Student":

            st.subheader("Add Student")

            sid = st.number_input("Student ID",step=1)
            name = st.text_input("Student Name")
            dept = st.text_input("Department")

            cursor.execute("SELECT room_id FROM Rooms1")
            rooms = cursor.fetchall()

            room_list = [r[0] for r in rooms]

            room_id = st.selectbox("Select Room",room_list)

            if st.button("Add Student"):

                # check capacity
                cursor.execute(
                "SELECT capacity FROM Rooms1 WHERE room_id=?",
                room_id)

                cap = cursor.fetchone()[0]

                cursor.execute(
                "SELECT COUNT(*) FROM Students2 WHERE room_id=?",
                room_id)

                count = cursor.fetchone()[0]

                if count >= cap:

                    st.error("Room Capacity Full")

                else:

                    cursor.execute(
                    "INSERT INTO Students2 VALUES (?,?,?,?)",
                    sid,name,dept,room_id)

                    conn.commit()

                    st.success("Student Added")

# -------- GENERATE SEATING --------

        elif option == "Generate Seating":

            st.subheader("Generate Seating")

            if st.button("Generate"):

                cursor.execute("DELETE FROM Seating1")
                conn.commit()

                cursor.execute(
                "SELECT student_id,room_id FROM Students2 ORDER BY room_id")

                students = cursor.fetchall()

                seat = 1

                for s in students:

                    cursor.execute(
                    "INSERT INTO Seating1 VALUES (?,?,?)",
                    s[0],s[1],seat)

                    seat += 1

                conn.commit()

                st.success("Seating Generated")

# -------- VIEW SEATING --------

        elif option == "View Seating":

            st.subheader("Seating Arrangement")

            cursor.execute("""
            SELECT 
            s.student_id,
            s.name,
            s.department,
            r.room_name,
            se.seat_number
            FROM Students2 s
            JOIN Seating1 se ON s.student_id = se.student_id
            JOIN Rooms1 r ON r.room_id = se.room_id
            """)

            data = cursor.fetchall()

            for row in data:

                st.write(
                "ID:",row[0],
                "| Name:",row[1],
                "| Dept:",row[2],
                "| Room:",row[3],
                "| Seat:",row[4]
                )

# -------- DELETE STUDENT --------

        elif option == "Delete Student":

            st.subheader("Delete Student")

            sid = st.number_input("Student ID",step=1)

            if st.button("Delete"):

                cursor.execute(
                "DELETE FROM Seating1 WHERE student_id=?",
                sid)

                cursor.execute(
                "DELETE FROM Students2 WHERE student_id=?",
                sid)

                conn.commit()

                st.success("Student Deleted")

# -------- DELETE ROOM --------

        elif option == "Delete Room":

            st.subheader("Delete Room")

            cursor.execute("SELECT room_id,room_name FROM Rooms1")
            rooms = cursor.fetchall()

            room_list = [f"{r[0]} - {r[1]}" for r in rooms]

            selected = st.selectbox("Select Room",room_list)

            if st.button("Delete Room"):

                rid = int(selected.split(" - ")[0])

                cursor.execute(
                "DELETE FROM Rooms1 WHERE room_id=?",
                rid)

                conn.commit()

                st.success("Room Deleted")

# ================= STUDENT LOGIN =================

elif choice == "Student Login":

    st.subheader("Student Login")

    sid = st.number_input("Student ID",step=1)
    name = st.text_input("Student Name")

    if st.button("Check Seating"):

        cursor.execute("""
        SELECT 
        s.student_id,
        s.name,
        s.department,
        r.room_name,
        se.seat_number
        FROM Students2 s
        JOIN Seating1 se ON s.student_id = se.student_id
        JOIN Rooms1 r ON r.room_id = se.room_id
        WHERE s.student_id=? AND s.name=?
        """,sid,name)

        data = cursor.fetchone()

        if data:

            st.success("Seat Found")

            st.write("Student ID:",data[0])
            st.write("Name:",data[1])
            st.write("Department:",data[2])
            st.write("Room:",data[3])
            st.write("Seat Number:",data[4])

        else:

            st.error("Seat Not Found")