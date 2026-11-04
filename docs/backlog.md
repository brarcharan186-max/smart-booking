# Product Backlog

Copy each user story into GitHub Projects as an issue. Put Stage 1 items in "Sprint 1", and so on.

## Stage 1: Plan

| ID | User story | Done when |
| --- | --- | --- |
| US-01 | As the team, we want a GitHub repository with a README so our work is version-controlled. | Repo exists with README and .gitignore |
| US-02 | As the team, we want an architecture and data-flow diagram so we agree on the design. | Diagrams added to the repo or report |
| US-03 | As the team, we want a database design so we know which fields to store. | `app/schema.sql` committed |

## Stage 2: Build

| ID | User story | Done when |
| --- | --- | --- |
| US-04 | As a customer, I want to book a service, date and time online so I don't have to phone. | Booking form saves to SQLite and shows a confirmation |
| US-05 | As a customer, I want a clear error if I miss a field so I can fix it. | Missing fields are rejected with a message |
| US-06 | As a business owner, I want double bookings blocked so two customers never share a slot. | Booking the same service, date and time twice is rejected |
| US-07 | As staff, I want to see all appointments so I can plan the day. | Staff dashboard lists bookings |
| US-08 | As staff, I want to cancel a booking so the slot can be used again. | Cancel sets status to cancelled and frees the slot |
| US-09 | As the team, we want automated tests for the booking rules. | pytest tests pass locally |

## Stage 3: Automate

| ID | User story | Done when |
| --- | --- | --- |
| US-10 | As the team, we want tests to run on every push and pull request. | GitHub Actions workflow is green |
| US-11 | As the team, we want the app packaged in Docker so it runs the same anywhere. | `docker compose up` runs the app |
| US-12 | As the team, we want the Docker image built only when tests pass. | Docker job depends on the test job |
| US-13 | As staff, we want bookings kept when the container restarts. | Docker volume stores the database |
