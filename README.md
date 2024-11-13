# Event Hive

Event Hive is a web application designed to streamline the management of events, providing an intuitive interface for Event Organizers and Attendees. With features for user registration, event creation, RSVPs, and tracking, Event Hive makes organizing and attending events simple and efficient.

## Features

### User Authentication

- **Registration & Login**: Users can create accounts and log in.
- **Roles**: Supports **Event Organizers** (create/manage events) and **Attendees** (browse and RSVP to events).
- **Email Verification**: Verifies user registration via email.

### Event Management

- **Event Creation**: Organizers can create events with details like name, date, time, location, and description. Events can be categorized, tagged, and marked as public or private.
- **RSVP System**: Attendees can Accept/Decline invitations, automatically updating the attendee count.
- **Event Details**: Displays comprehensive event information, including description, date/time, location, attendee count, and organizer info. Organizers can view the list of attendees.
- **RSVP Notifications**: Users receive notifications about the number of pending RSVPs they have yet to respond to, helping them keep track of upcoming events.

### User Dashboard

- **Organizer Dashboard**: Manage created events and edit event details.
- **Attendee Dashboard**: Track accepted events, view pending RSVPs, and manage profile settings.

### Event Categories and Tags

- **Categories & Tags**: Organize events by type (e.g., conferences, workshops) for easy filtering and discovery.

### Deployment

- **Hosting**: [Live Site](https://event-hive-backend-django.onrender.com/)

## CRUD Operations

- **Create**: Event Organizers can create events. Users can create profiles.
- **Read**: Users can view upcoming events and event details.
- **Update**: Organizers can edit event details. Users can update profiles.
- **Delete**: Organizers can cancel or delete their events.
