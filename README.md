# SHEQ+ — Frontend

This folder contains the frontend for the SHEQ+ web app (static HTML/CSS/JS). It is intentionally small and mobile-first.

## Files
- index.html — Landing page
- about.html — About and mission
- faq.html — Frequently asked questions
- report.html — Report incident form
- chat.html — AI chat interface
- login.html — Login/register UI
- admin.html — Admin viewer (must be protected server-side)
- styles.css — Theme, responsive layout, dark-mode
- script.js — Client-side logic (theme, auth, forms, chat)

## Next steps
1. Place these files in your `frontend/` folder. Serve them with Flask static files or a simple static host.
2. Ensure the backend routes exist: `/api/register`, `/api/login`, `/api/report`, `/api/chat`, `/api/admin/users`, `/api/admin/reports`.
3. Configure OpenAI key and SMTP on your backend.
4. Protect admin endpoints with authentication.
