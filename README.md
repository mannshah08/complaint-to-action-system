#  Complaint to Action System

> **AI‑powered complaint management & prioritization platform**

---

##  Overview

**Complaint to Action System** is a web‑based application that enables users to submit complaints, automatically classifies them using AI, and helps administrators **prioritize, track, and resolve issues efficiently**.

This project was built as an **MVP for a hackathon / academic evaluation**, with emphasis on:

* Clear problem–solution mapping
* Secure authentication
* Practical AI usage
* Deployment readiness

---

##  Problem Statement

Organizations receive a high volume of complaints every day. Most systems fail because they:

*  Treat all complaints equally, ignoring urgency
*  Mix sensitive and public issues
*  Lack proper access control for admins
*  Offer zero transparency to the community

Result: **slow resolutions, poor trust, and operational chaos**.

---

##  Solution

The **Complaint to Action System** solves this by:

*  Automatically classifying complaints using AI
*  Assigning urgency levels for faster action
*  Securing access using Google OAuth
*  Enabling public complaint visibility for transparency
*  Giving admins a focused, priority‑driven dashboard

---

##  Key Features

###  Authentication

* Google OAuth 2.0 login
* Session‑based authentication
* Login state reflected across all pages
* Secure logout with session clearing
* **Admin panel accessible only to authenticated users**

---

###  Complaint Submission

Users can:

* Select role: **Student / Visitor / Staff**
* Choose complaint visibility: **Public or Private**
* Submit complaints via a simple UI

Each complaint is automatically classified into:

* **Category**
* **Urgency Level:** High / Medium / Low

---

###  AI‑Based Classification

* Complaint text analyzed using a **rule‑based / ML classifier**
* Determines urgency and category
* Urgency is used to **prioritize admin actions**

> This keeps critical issues from getting buried under noise.

---

###  Admin Panel

Admins can:

* View all submitted complaints
* Filter complaints by urgency:

  * 🔴 High
  * 🟡 Medium
  * 🟢 Low
* Update complaint status
* Access data securely (authentication required)

---

###  Community Pulse

* Public complaints are visible to everyone
* Complaints are **sorted by upvotes**
* Encourages transparency and collective awareness
* Helps identify recurring or systemic issues

---


##  Deployment Readiness

* Environment‑based configuration
* Secure OAuth handling
* Production‑ready project structure
* Compatible with platforms like **Render / Vercel / Railway**

---

##  Future Enhancements

*  Role‑based admin permissions
*  Email notifications for high‑priority complaints
*  Analytics & insights dashboard
*  Cloud database (PostgreSQL / Firestore)
*  Advanced NLP model upgrade

---

## 🏁 Conclusion

**Complaint to Action System** demonstrates how AI, authentication, and thoughtful system design can convert unstructured complaints into **clear, actionable priorities**.

Built to be simple, scalable, and impactful — ideal for **hackathons, academic reviews, and real‑world adaptation**.

**Mann Shah**
Hackathon / Academic Project
