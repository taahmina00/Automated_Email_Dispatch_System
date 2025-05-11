# 📧 Automated Email Dispatch System

A Python-based standalone application designed to automate the process of sending emails based on dynamic data stored in an Oracle database. This system ensures efficient email communication while updating the database with delivery status and logs.

---

## 📌 Overview

This project automates email dispatch by fetching recipient details and content from an Oracle database. The system sends emails—including CC, BCC, and attachments—and updates the database with delivery status and timestamps, reducing manual effort and ensuring accountability.

---

## ⚙️ Features

- 📬 **Automated Email Sending:** Sends emails using dynamically retrieved data including recipient, subject, body, CC, BCC, and attachments.
- 🧠 **Python-Based Control:** Developed using Python and libraries like `smtplib` and `cx_Oracle` for email and database operations.
- 🔄 **Database Integration:** Interacts directly with Oracle DB to fetch unsent emails and update sent status and delivery timestamp.
- ✅ **Status Logging:** Updates `sent_status` (0 → 1) and logs `email_date` upon successful delivery to maintain accurate records.
- ⚙️ **Standalone Execution:** Converted the script into an executable for easy deployment and use without requiring Python installation.

---

## 🧰 Technologies Used

- Python  
- Oracle Database
- Oracle Instant Client (for enabling Oracle database interaction) 
- cx_Oracle (Python-Oracle DB connector)  
- smtplib (SMTP email handling)  
- email.mime (for constructing email content)  
- pyinstaller (for creating standalone executable)

---

## 🛠️ Implementation Details

- Script fetches all pending emails from the Oracle database where `sent_status = 0`.
- Constructs and sends the email using Python’s `smtplib` and `email.mime` libraries.
- Upon successful send, updates the database to mark the email as sent and logs the date and time of dispatch in the `email_date` column.
- Packaged the script as an executable `.exe` file using `pyinstaller` for ease of use.

---

## 🖥️ Development Environment

- **IDE Used:** VS Code
