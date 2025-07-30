# Box Office Sales Calculator

## Overview

This is a comprehensive Flask-based web application for managing box offices (taquillas) and calculating ticket sales revenue with daily financial tracking. The application allows users to create multiple box offices, set ticket prices, calculate total sales, track daily expenses, and view detailed financial cuts (cortes) per day. It features a responsive dark-themed UI built with Bootstrap, the Atracciones Tijuana logo, and provides real-time form validation.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

The application follows a simple monolithic Flask architecture with the following structure:

- **Frontend**: Server-side rendered HTML templates using Jinja2
- **Backend**: Flask web framework with Python
- **Data Storage**: In-memory Python list (temporary storage)
- **Styling**: Bootstrap with dark theme and custom CSS
- **Client-side Enhancement**: Vanilla JavaScript for form validation and UX improvements

## Key Components

### Backend Components

1. **Flask Application** (`app.py`)
   - Main application logic with comprehensive route handlers:
     - Index page with dashboard
     - Adding and managing box offices (taquillas)
     - Calculating ticket sales revenue
     - Adding and tracking daily expenses
     - Automatic daily cuts (cortes) generation
   - Advanced form validation and error handling
   - Flash messaging system for user feedback
   - Financial tracking with net income calculations

2. **Application Entry Point** (`main.py`)
   - Simple wrapper to run the Flask app
   - Configured for development with debug mode

### Frontend Components

1. **Base Template** (`templates/base.html`)
   - Responsive HTML structure with Bootstrap dark theme
   - Navigation bar with branding
   - Flash message display system
   - Font Awesome icons integration

2. **Main Interface** (`templates/index.html`)
   - Form for adding new box offices
   - Display of existing box offices
   - Sales calculation interface for each box office

3. **Styling** (`static/css/custom.css`)
   - Custom CSS enhancements over Bootstrap
   - Card hover effects and form styling
   - Responsive design improvements

4. **Client-side Logic** (`static/js/app.js`)
   - Form validation enhancement
   - Loading states for form submissions
   - Bootstrap tooltip initialization
   - Real-time input validation

## Data Flow

1. **Adding Box Offices**:
   - User submits form with box office name and ticket price
   - Server validates input (required fields, unique names, positive prices)
   - Valid data is stored in global list
   - User receives success/error feedback via flash messages

2. **Sales Calculation**:
   - User inputs initial and final ticket numbers for a specific box office
   - Server calculates total sales: (final - initial - 2) × ticket_price
   - Result is stored and displayed on the interface
   - **NEW**: Sales are automatically added to daily cuts (cortes)

3. **Expense Tracking**:
   - **NEW**: User can add daily expenses with description and amount
   - Expenses are grouped by date with timestamps
   - Individual expenses can be deleted
   - Expenses are automatically included in daily financial reports

4. **Daily Cuts (Cortes)**:
   - **NEW**: Automatically generated when sales are calculated
   - Shows gross income, gross expenses, and net income per day
   - Daily view with detailed expense breakdowns
   - Historical tracking with date sorting

5. **Google Sheets Integration**:
   - **NEW**: Optional automatic synchronization with Google Sheets
   - Sales data synced to "Ventas" worksheet with complete transaction details
   - Expenses synced to "Gastos" worksheet with timestamps
   - Daily cuts can be manually synced to "Cortes" worksheet
   - Requires GOOGLE_SHEETS_CREDENTIALS and GOOGLE_SPREADSHEET_ID environment variables

6. **Data Persistence**:
   - Currently uses in-memory storage (global Python dictionaries and lists)
   - Data structures: taquillas[], cortes{}, gastos{}
   - Data is lost when application restarts
   - **NEW**: Google Sheets provides persistent backup and analysis capabilities
   - Ready for database integration (Drizzle/Postgres can be added later)

## External Dependencies

### Python Packages
- **Flask**: Web framework for routing and templating
- **gspread**: Google Sheets API integration for data synchronization
- **oauth2client**: OAuth2 authentication for Google Services
- **Standard Library**: os, logging, json, datetime for configuration and functionality

### Frontend Libraries
- **Bootstrap**: CSS framework with dark theme from Replit CDN
- **Font Awesome**: Icon library for UI enhancement
- **Vanilla JavaScript**: No additional JS frameworks

### CDN Resources
- Bootstrap CSS with Replit dark theme
- Font Awesome icons

## Deployment Strategy

### Development Setup
- Flask development server with debug mode enabled
- Host: 0.0.0.0 (accessible from external connections)
- Port: 5000
- Environment-based secret key configuration

### Production Considerations
- Environment variable for session secret (`SESSION_SECRET`)
- Logging configured for debugging
- Ready for database migration from in-memory storage
- Static file serving through Flask (suitable for small-scale deployment)

### Architecture Decisions

1. **In-Memory Storage**: 
   - **Problem**: Need simple data persistence for MVP
   - **Solution**: Global Python list for temporary storage
   - **Rationale**: Quick development without database setup complexity
   - **Future**: Easy migration to Drizzle ORM with Postgres

2. **Server-Side Rendering**:
   - **Problem**: Need dynamic content with form handling
   - **Solution**: Jinja2 templates with Flask
   - **Rationale**: Simpler than API + SPA, better SEO, faster initial load

3. **Bootstrap Dark Theme**:
   - **Problem**: Need professional, responsive UI quickly
   - **Solution**: Bootstrap with Replit's dark theme
   - **Rationale**: Consistent with Replit environment, reduces custom CSS needs

4. **Flash Messaging**:
   - **Problem**: Need user feedback for form submissions
   - **Solution**: Flask's built-in flash messaging system
   - **Rationale**: Server-side validation with immediate user feedback