# Ticket: Fix Haunted Codebase

## Objective
Address two separate, pre-existing technical debt issues in the `main` branch to improve performance and user experience.

---

### 1. Frontend Report: Unnecessary Component Re-renders

**Symptom:** The product owner noticed that when they interact with certain UI elements in the header (e.g., hovering over the user profile icon), the main transaction data grid seems to flicker and re-render, even though the transaction data itself has not changed. This is causing a sluggish feel on the dashboard.

**Task:**
Using browser developer tools (like the React Profiler), confirm the unnecessary re-rendering of the transaction list component.

Your goal is to identify the root cause of the wasted renders and apply a fix to ensure the transaction list only re-renders when its data or relevant state actually changes.
