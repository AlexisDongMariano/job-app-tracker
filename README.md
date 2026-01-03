# job-app-tracker

# fields
company - req
role - req
status - req
> applied
> rejected
> job offer
> interviewed
> interview scheduled

date applied - opt
deadline - opt
contact - opt

job-type
> full-time
> part-time
> freelance
> contract

salary (annual) - opt
location - opt



htmx - 
Next, the most valuable “real app” upgrade is proper error handling + validation in HTMX, so you can show a message without a page reload when something goes wrong.

A perfect example is preventing duplicates (same company + role), because it forces you to handle:

DB constraints

API errors

HTMX error rendering

We’ll do it in small steps.

tailwind
sort functionality