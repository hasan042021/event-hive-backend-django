# Event Hive

**Event Hive** is a web application designed to streamline the management of events, providing an intuitive interface for Event Organizers and Attendees. It includes features for user registration, event creation, RSVPs, and event tracking, making organizing and attending events simple and efficient.

---

## Features

### 1. **User Authentication**
   - **Registration & Login**: Users can create accounts and log in.
   - **Roles**:
     - Event Organizers: Create and manage events.
     - Attendees: Browse events and RSVP.
   - **Email Verification**: Verifies user registration via email.

### 2. **Event Management**
   - **Event Creation**: Organizers can create events with the following details:
     - Event name
     - Event date
     - Event time
     - Event location
     - Event description
     - Event categories
     - Event tags
     - Public/Private status
   - **RSVP System**: Attendees can accept or decline invitations, which automatically updates the attendee count.
   - **Event Details**: Displays comprehensive event information:
     - Event description
     - Date/time
     - Location
     - Attendee count
     - Organizer information
   - **RSVP Notifications**: Users receive notifications about pending RSVPs for events they are invited to.

### 3. **User Dashboard**
   - **Organizer Dashboard**: Organizers can:
     - Manage created events
     - Edit event details
     - View Attendees of each events
     - Manage profile data and settings
   - **Attendee Dashboard**: Attendees can:
     - Track accepted events
     - sort events by date and time
     - View pending RSVPs
     - Manage profile data and settings

### 4. **Event Categories and Tags**
   - **Categories & Tags**: Events are categorized (e.g., conferences, workshops) for easy filtering and discovery by users.

---

## CRUD Operations

- **Create**: 
  - Event Organizers can create events.
  - Users can create profiles.

- **Read**: 
  - Users can view upcoming events and detailed event information.

- **Update**: 
  - Event Organizers can edit event details.
  - Users can update their profiles.

- **Delete**: 
  - Event Organizers can cancel or delete their events.

---

## Deployment

- **Frontend**: [Event Hive Frontend](https://event-hive-client-react-102.onrender.com/)
- **Backend**: [Event Hive Backend](https://event-hive-backend-api.onrender.com/)
- **File Storage**: The application uses **S3 Bucket** for secure and scalable file storage, allowing event images and thumbnails to be uploaded and served efficiently.

---

## Technologies

- **Frontend**: React, Tailwind CSS
- **Backend**: Django REST Framework, Supabase (for database management)
- **Authentication**: JWT, Email Verification (via SMTP)
- **Deployment**: [Platform name (e.g., Vercel, Render, etc.)]
- **File Storage**: AWS S3
- **Database**: PostgreSQL (via Supabase)

---



