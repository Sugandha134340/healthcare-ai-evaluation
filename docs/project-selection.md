# Project Selection & Evaluation Fit

## Selected Healthcare Application

**Project:** Hospital Management System  
**Repository:** https://github.com/Adinath-Jagtap/hospital-management-system  
**Version:** `main` branch; record the exact commit used for the final submission.

## Why this project was selected

The project provides realistic hospital workflows rather than only generic CRUD functionality. Its documented capabilities include patient, doctor and administrator roles, doctor availability, appointment booking/cancellation/rescheduling, treatment history and medical-record workflows.

These capabilities allow the evaluation framework to derive realistic scenarios for appointment availability, booking, cancellation, contradictory requests, authorization, privacy and data-integrity behavior.

## Healthcare Functionality

- Patient management
- Doctor management
- Doctor availability
- Appointment scheduling
- Appointment cancellation/rescheduling
- Treatment and medical history
- Role-based access for administrators, doctors and patients

## Data / API Surface

The repository documents API endpoints for doctors and appointments, including:

- `GET /api/doctors`
- `GET /api/appointments`
- `GET /api/appointment/{appointment_id}`
- `PUT /api/appointment/{appointment_id}`
- `DELETE /api/appointment/{appointment_id}`

The repository also documents collections/entities for users, departments, doctors, patients, appointments, doctor availability and treatments.

## Evaluation Relevance

The application supports scenarios for:

- Availability lookup
- Appointment booking
- Appointment cancellation
- Appointment modification
- Duplicate operations
- Unavailable slots
- Patient/doctor information
- Data consistency
- Authorization and privacy

## Safety Relevance

Healthcare records and appointment information create safety-sensitive and privacy-sensitive evaluation cases. The evaluation framework will test whether the target AI agent avoids exposing unauthorized information and handles urgent or out-of-scope medical requests appropriately.

## Reproducibility

The repository provides setup instructions and identifies Python, Flask and MongoDB dependencies. The final evaluation project will pin or record the selected commit and keep the scenario dataset version-controlled.

## Limitations

This application is being used as the healthcare context from which evaluation scenarios are derived. It is not the system being evaluated itself. The supplied healthcare AI agent remains the primary evaluation target. If the supplied agent is unavailable, a clearly labelled local fallback agent will be used only to demonstrate that the evaluation infrastructure runs end-to-end.
