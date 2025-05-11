-- Create table
create table AUTOMATE_MAIL_MGBL
(
  recipient_email      VARCHAR2(255),
  email_body           VARCHAR2(4000),
  email_subject        VARCHAR2(255),
  attachment_file_path VARCHAR2(255),
  sent_status          NUMBER(1),
  cc_emails            VARCHAR2(4000),
  bcc_emails           VARCHAR2(4000),
  email_date           DATE,
  email_type           VARCHAR2(100) not null
)
