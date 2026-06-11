# EventPass - Complete Workflow & Functional Requirements

## Project Goal

Build a simple, modern web application for event registration, attendee management, QR-based check-in, and instant badge printing.

The system should be easy to use, visually professional, and optimized for conferences, exhibitions, workshops, and corporate events.

---

# Main User Roles

## Organizer

The organizer creates and manages events.

Capabilities:

* Create event
* Edit event
* Delete event
* Upload event logo
* Upload badge design
* Configure badge settings
* View registrations
* Monitor attendance
* Export attendee data
* Reprint badges

---

## Attendee

The attendee registers for an event.

Capabilities:

* Fill registration form
* Receive confirmation
* Receive QR code
* Present QR code at check-in

---

## Check-in Staff

The staff member manages attendee entry.

Capabilities:

* Scan attendee QR code
* Validate registration
* Trigger automatic badge printing
* View attendee status

---

# Complete Workflow

## Workflow 1: Create Event

Organizer logs in.

Organizer clicks:

Create Event

System asks for:

* Event Name
* Description
* Start Date
* End Date
* Event Logo
* Registration URL

Organizer saves event.

System creates event successfully.

---

## Workflow 2: Configure Badge

Organizer opens event settings.

Organizer uploads badge background design.

The uploaded design is a complete badge image created externally using Canva, Photoshop, Illustrator, etc.

Organizer defines positions for:

* Full Name
* Company Name
* Job Title
* QR Code

Organizer saves template.

System stores all coordinates.

---

## Workflow 3: Configure Attendee Types

Organizer creates attendee categories.

Examples:

* Visitor
* Speaker
* VIP
* Organizer
* Sponsor

Each attendee type may have:

* Name
* Label
* Badge color
* Badge tag

These types can be selected during registration.

---

## Workflow 4: Registration

Attendee opens registration page.

Attendee fills:

* Full Name
* Email
* Phone Number
* Company
* Job Title
* Attendee Type

Attendee clicks Register.

System:

* Validates form
* Creates attendee record
* Generates unique UUID
* Generates QR code
* Stores registration

System displays registration success page.

---

## Workflow 5: Attendee Management

Organizer can:

* View all attendees
* Search attendees
* Edit attendee information
* Delete attendee
* Export attendees

Search filters:

* Name
* Email
* Company
* Attendee Type
* Registration Date

---

## Workflow 6: Check-in

Staff opens Check-in Screen.

The screen continuously waits for QR scans.

Staff scans attendee QR code.

System:

* Reads UUID
* Finds attendee
* Validates attendee
* Checks registration status

If valid:

* Mark attendee as checked in
* Store check-in timestamp
* Generate badge
* Automatically print badge

No manual print button required.

---

## Workflow 7: Duplicate Check-in Protection

If attendee already checked in:

System displays:

Already Checked In

System shows:

* Attendee Name
* Previous Check-in Time
* Badge Printed Status

No automatic printing occurs.

Only authorized users can reprint.

---

## Workflow 8: Reprint Badge

Organizer searches attendee.

Organizer clicks Reprint Badge.

System:

* Generates badge again
* Sends badge to printer
* Records reprint action in audit log

---

## Workflow 9: Badge Generation

When badge generation is requested:

System:

1. Loads badge background image
2. Loads attendee information
3. Generates QR image
4. Places attendee data on badge
5. Creates final badge
6. Generates printable PDF
7. Sends PDF to printer

---

## Workflow 10: Dashboard

Organizer dashboard displays:

* Total Registrations
* Total Check-ins
* Total Badges Printed
* Attendance Rate
* Registrations by Attendee Type

---

# Functional Requirements

## Event Management

Must support:

* Create Event
* Update Event
* Delete Event
* View Event

---

## Badge Management

Must support:

* Upload badge design
* Configure badge coordinates
* Preview badge
* Generate badge

---

## Registration

Must support:

* Public registration page
* Attendee creation
* QR generation
* Validation

---

## QR System

Must support:

* Unique UUID generation
* QR generation
* QR validation
* QR scanning

QR must contain only UUID.

No personal information inside QR.

---

## Check-in System

Must support:

* QR scanning
* Registration validation
* Attendance tracking
* Automatic badge printing

---

## Reporting

Must support:

* Registration count
* Attendance count
* Badge print count
* Export to Excel
* Export to CSV

---

## Audit Logs

System must record:

* Check-ins
* Badge printing
* Badge reprints
* Attendee modifications

---

# User Experience Requirements

The system should:

* Be simple
* Require minimal clicks
* Support Arabic and English
* Be mobile responsive
* Have a clean modern design
* Provide fast check-in performance
* Print badges within seconds after scan

The entire attendee check-in process should take less than 3 seconds from QR scan to badge printing.
