# Curl Testing Guide for FastAPI Chat API

This document provides single-request curl tests only for verifying:

- Authenticated user (JWT)
- Global user (no token)

Works on:
- Windows CMD
- Windows PowerShell

---

# Base Endpoint
```
POST http://127.0.0.1:8000/chat
```

Request body:
```json
{
  "prompt": "your message"
}
```

---

# AUTH USER (JWT TOKEN)

## Windows CMD (Single Request)
```bash
curl -X POST "http://127.0.0.1:8000/chat" -H "Content-Type: application/json" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0IHVzZXIiLCJuYW1lIjoiSm9obiBEb2UiLCJpYXQiOjE1MTYyMzkwMjJ9.gI90L47RNZiY0iFtG46bfznvacqabWwRJRqnDHu-JC8" -d "{\"prompt\":\"Hello auth user\"}"
```

---

## PowerShell (Single Request)
```powershell
$token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0IHVzZXIiLCJuYW1lIjoiSm9obiBEb2UiLCJpYXQiOjE1MTYyMzkwMjJ9.gI90L47RNZiY0iFtG46bfznvacqabWwRJRqnDHu-JC8"

Invoke-RestMethod -Uri "http://127.0.0.1:8000/chat" `
-Method POST `
-Headers @{ "Content-Type" = "application/json"; "Authorization" = "Bearer $token" } `
-Body '{"prompt":"Hello auth user"}'
```

---

# GLOBAL USER (NO TOKEN)

## Windows CMD (Single Request)
```bash
curl -X POST "http://127.0.0.1:8000/chat" -H "Content-Type: application/json" -d "{\"prompt\":\"Hello global user\"}"
```

---

## PowerShell (Single Request)
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/chat" `
-Method POST `
-Headers @{ "Content-Type" = "application/json" } `
-Body '{"prompt":"Hello global user"}'
```

---

# Notes

- Use CMD curl or PowerShell Invoke-RestMethod as shown
- Ensure FastAPI server is running:
```
uvicorn src.main:app --reload
```
- If Swagger /docs works but terminal fails, check JSON escaping or PowerShell formatting

---

# Expected Behavior

## Auth User
- Returns Gemini response using JWT identity

## Global User
- Returns Gemini response as unauthenticated user

