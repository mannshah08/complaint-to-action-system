Complaint to Action System 🚨

AI-powered complaint management & prioritization platform

📌 Overview

Complaint to Action System is a web-based application that allows users to submit complaints, automatically classifies them using AI, and helps administrators prioritize and manage issues efficiently. The system supports Google OAuth authentication, admin-only access, and community visibility for public complaints.

This project was built as an MVP for hackathon / academic evaluation, focusing on functionality, clarity, and deployment readiness.

🎯 Problem Statement

Organizations receive a large number of complaints daily, making it difficult to:

Prioritize urgent issues

Separate public vs private complaints

Ensure only authorized admins can access sensitive data

Maintain transparency with the community

💡 Solution

This system:

Uses AI-based text classification to categorize complaints and assign urgency

Supports Google OAuth login for secure authentication

Restricts admin panel access to authenticated users only

Allows users to make complaints public or private

Displays public complaints in a community-driven view

✨ Key Features
🔐 Authentication

Google OAuth 2.0 login

Login status reflected across all pages

Logout clears session and redirects to home

Admin panel accessible only after Google login

📝 Complaint Submission

User role selection (Student / Visitor / Staff)

Public or Private visibility option

Automatic classification into:

Category

Urgency (High / Medium / Low)

🧠 AI Classification

Complaint text analyzed using a rule-based / ML classifier

Urgency used to prioritize admin actions

🧑‍💼 Admin Panel

View all complaints

Filter complaints by urgency (High / Medium / Low)

Update complaint status

Secure access control

🌍 Community Pulse

Public complaints visible to all users

Sorted by number of upvotes

Encourages transparency and community feedback

🔮 Future Enhancements

Role-based admin permissions

Email notifications for high-priority complaints

Analytics dashboard

Cloud database (PostgreSQL / Firestore)

NLP model upgrade
