
# Ticket: Implement Transaction Tags & Grid

## Objective
Build a new feature that allows transactions to be categorized with multiple tags and display them in a new, advanced data grid with server-side sorting and pagination.

---

## Frontend Task: New Data Grid Component

**Task:**
Build a new React component (`TransactionGrid.tsx`) that consumes the API endpoint `/api/v1/transactions/grid`.

*   **Display:** The grid must display columns for `Date`, `Description`, `Amount`, `Category`, and the new `Tags` (rendered as a collection of pills or badges).
*   **Server-Side Sorting:** Clicking a column header (e.g., `Amount`) must trigger a new API call to fetch data sorted by that column.
*   **Server-Side Pagination:** UI controls (e.g., "Next", "Previous" buttons) must trigger new API calls to fetch the correct page of data.
*   **Implementation:** You are encouraged to build the grid using standard HTML table elements rather than adding a new third-party library.
