import cx_Oracle
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from datetime import datetime

# Hardcode credentials here
db_hostname = ''
db_port = ''
db_service_name = ''
db_username = ''
db_password = ''

smtp_server = ''
smtp_port = 25  # Adjust SMTP port if necessary
smtp_username = ''
smtp_password = ''


# Connect to Oracle database using EZConnect method
try:
    # Create the DSN using EZConnect method (hostname:port/service_name)
    db_dsn = f"{db_hostname}:{db_port}/{db_service_name}"

    # Connect to the Oracle database using the connection string (DSN)
    connection = cx_Oracle.connect(user=db_username, password=db_password, dsn=db_dsn)
    cursor = connection.cursor()

    # Query to retrieve recipient email, body, subject, attachment file path, cc and bcc, email_type, and email_date from the 'automate_mail_mgbl' table where sent_status is 0
    query = """
        SELECT recipient_email, email_body, email_subject, attachment_file_path, cc_emails, bcc_emails, email_type, email_date
        FROM ultimus.automate_mail_mgbl
        WHERE sent_status = 0
    """
    cursor.execute(query)

    # Fetch all rows from the result
    rows = cursor.fetchall()

    # Loop through each row and send the email
    for row in rows:
        recipient_email = row[0]
        email_body = row[1]
        email_subject = row[2]  # Get the dynamic subject from the database
        attachment_file_paths = row[3]  # Get the dynamic attachment file paths from the database
        cc_emails = row[4]  # Get the CC email addresses from the database
        bcc_emails = row[5]  # Get the BCC email addresses from the database
        email_type = row[6]  # Get the email_type from the database
        email_date = row[7]  # Get the email_date (not used directly, but can be used for logging or any additional checks)

        # Log the email_type for debugging or further logic
        print(f"Processing email for {recipient_email}, email_type: {email_type}")

        # If email_body is None or empty, skip sending the email and leave sent_status as 0
        if not email_body:
            print(f"Skipping email for {recipient_email} because the email body is empty or None.")
            continue

        # Ensure the email body is a string (handle cases where it's not a string)
        if not isinstance(email_body, str):
            email_body = str(email_body)

        # Define the bold_footer with HTML tags
        bold_footer = """
            <b>Thank's<br>CBS Team<br><br>This is an auto-generated email, please do not reply to this email.</b>
        """

        # Create the email message
        msg = MIMEMultipart('alternative')
        msg['From'] = smtp_username  # Use the hardcoded sender email (smtp_username)
        msg['To'] = recipient_email
        msg['Subject'] = email_subject if email_subject else 'No Subject'  # Set dynamic subject from the database

        # Add CC and BCC if available
        if cc_emails:
            msg['Cc'] = cc_emails  # Add CC field
        if bcc_emails:
            msg['Bcc'] = bcc_emails  # Add BCC field

        # Ensure that the line breaks are preserved in the plain text version by properly handling the email_body with "\n"
        # Add a plain text footer directly to ensure proper formatting
        plain_body = email_body + "\n\nThank's\nCBS Team\n\nThis is an auto-generated email, please do not reply to this email."

        # Create the HTML version of the email (with only the footer in HTML)
        html_body = email_body.replace("\n", "<br>") + "<br><br>" + bold_footer

        # Attach both plain text and HTML versions to the message
        msg.attach(MIMEText(plain_body, 'plain'))  # Add plain text part
        msg.attach(MIMEText(html_body, 'html'))    # Add HTML part

        # Add the dynamic attachments
        if attachment_file_paths:
            # Split the file paths if they are comma-separated
            attachment_paths = attachment_file_paths.split(',')

            for attachment_file_path in attachment_paths:
                attachment_file_path = attachment_file_path.strip()  # Remove any extra spaces

                if os.path.exists(attachment_file_path):
                    with open(attachment_file_path, "rb") as attachment:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(attachment.read())
                        encoders.encode_base64(part)
                        part.add_header(
                            'Content-Disposition',
                            f'attachment; filename={os.path.basename(attachment_file_path)}'
                        )
                        msg.attach(part)
                    print(f"Attachment added: {attachment_file_path}")
                else:
                    print(f"Attachment file not found: {attachment_file_path}")
        else:
            print("No attachment files provided.")

        try:
            # Connect to the SMTP server on port 25
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                all_recipients = [recipient_email] + (cc_emails.split(',') if cc_emails else []) + (
                    bcc_emails.split(',') if bcc_emails else [])
                server.sendmail(smtp_username, all_recipients,
                                msg.as_string())  # Send email to 'To', 'Cc', and 'Bcc' recipients
                print(f"Email successfully sent to {recipient_email}")

                # Update sent_status to 1 and email_date to current timestamp in the database after successful email send
                update_query = """
                    UPDATE ultimus.automate_mail_mgbl
                    SET sent_status = 1
                    WHERE recipient_email = :recipient_email and sent_status = 0
                """
                cursor.execute(update_query, {
                    'email_date': datetime.now(),  # Set the email sent date to the current timestamp
                    'recipient_email': recipient_email
                })
                connection.commit()  # Commit the changes
        except Exception as e:
            print(f"Failed to send email to {recipient_email}. Error: {e}")

    # Close the cursor and connection
    cursor.close()
    connection.close()

except cx_Oracle.DatabaseError as e:
    print(f"Database connection error: {e}")
