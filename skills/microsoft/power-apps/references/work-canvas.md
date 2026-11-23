# Canvas app design and Power Fx review

Use for a task-specific canvas app, formula review or incomplete gallery. Deliver a design draft in chat using an approved schema or synthetic data. The Outlook, calendar and SharePoint readers are never used to build, modify or publish an app. No new connection or maker access is required for this review.

1. Define the user's job, roles, device, source list/table, row count, expected growth, data types and required business key. Record whether the app needs search, detail, edit or offline behavior. Reuse an existing list view or form if it completes the job.
2. Sketch the smallest screen path. For a browse-only request use **Search → Results → Detail**. Specify initial, loading, empty, error and access-denied states. A failed read must display a retry/error state rather than “no matching records.” Place labels, keyboard focus and status messages where a keyboard or screen-reader user can reach them.
3. Map each control to its property and source field. For a SharePoint single-line text field and a classic text input, draft the following gallery `Items` formula. Verify delegation for the source, column type and operation. Keep the table on the server and avoid copying an unbounded list into a collection.

```powerfx
Filter(WorkRequests, StartsWith(Title, txtPrefix.Text))
```

4. For a requested edit, deliver a separate maker design. Specify record key, permitted actors, required fields, validation, duplicate-submit behavior, concurrency and what to show on failure. Capture success only after the source acknowledges the save. Role-based control visibility assists navigation. Source permissions enforce access. List any connector license, environment or data policy as a dependency for the owner to verify.
5. Return a screen/control/formula table, named assumptions, a test matrix and release/rollback notes. Identify the known-good version and any schema dependencies before an authorized owner considers promotion.

**Synthetic acceptance.** A 3,200-row list contains a single “Zebra intake” beyond the first 2,000 rows. Search for “Zeb” with the maker test data-row limit set to 1. Expect the item if the filter delegates. Check the Studio delegation warning and test empty and denied responses separately. Repeat the path using the keyboard and verify the result/error is announced. Record unexecuted tests as pending tenant validation.

[Microsoft Learn: delegation and testing with a data-row limit of 1](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/delegation-overview) · [SharePoint field and operator support](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/connections/connection-sharepoint-online) · [accessibility review](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/accessibility-checker)
