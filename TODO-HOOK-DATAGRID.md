# Ticket: Build a Custom Data Grid State Hook

## Objective
Create a reusable custom React hook to manage the state and logic for data grids, including sorting, pagination, and API integration. This hook should be generic enough to support multiple grid components in the application.

---

## Task: Implement `useDataGrid` Hook

**Task:**
Build a new custom hook called `useDataGrid` that encapsulates all state and logic for a data grid component. The hook should:

- Manage grid state: current page, page size, sorting column, sorting order, and loading/error states.
- Handle API requests for grid data, including passing pagination and sorting parameters.
- Expose methods for changing page, sorting, and refreshing data.
- Be generic and reusable for any grid that consumes paginated/sorted API data.
- Include TypeScript types for strong typing and reusability.

### Acceptance Criteria
- The hook must be implemented in a new file (e.g., `src/hooks/useDataGrid.ts`).
- The hook should be used in the `TransactionGrid.tsx` component to manage its state and API calls.
- The hook should expose:
    - `data`: the current grid data
    - `total`: total number of items
    - `loading`/`error` states
    - `page`, `pageSize`, `sortBy`, `sortOrder`
    - `setPage`, `setSort`, `refresh`
- The hook should be documented with usage examples in comments.
- The solution should avoid unnecessary re-renders and be optimized for performance.

### Bonus
- Support for server-side filtering (e.g., by transaction type or tag) via hook parameters.
- Unit tests for the hook (e.g., using React Testing Library).

---

## Implementation Notes
- You may use `useReducer` or `useState` for state management.
- API integration should use `fetch` or your preferred HTTP client.
- The hook should be generic, e.g., `useDataGrid<T>(...)`.
- Document any trade-offs or architectural decisions in the code comments.

---

## Deliverable
- A new custom hook file (`src/hooks/useDataGrid.ts`) with implementation and documentation.
- Integration of the hook in the grid component.
- (Optional) Unit tests for the hook.
