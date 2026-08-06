-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Enum Types
CREATE TYPE user_role AS ENUM ('Patient', 'Doctor', 'Receptionist', 'Admin');
CREATE TYPE appointment_status AS ENUM ('Scheduled', 'Completed', 'Cancelled', 'No-show');
CREATE TYPE notification_type AS ENUM ('Reminder', 'Confirmation', 'Cancellation', 'Follow-up');
CREATE TYPE notification_status AS ENUM ('Pending', 'Sent', 'Failed');

-- 1. Users Table (Core Auth representation)
CREATE TABLE Users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    role user_role NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. Departments Table
CREATE TABLE Departments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT
);

-- 3. Patients Table
CREATE TABLE Patients (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES Users(id) ON DELETE CASCADE,
    full_name VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    dob DATE NOT NULL,
    gender VARCHAR(20),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 4. Doctors Table
CREATE TABLE Doctors (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES Users(id) ON DELETE CASCADE,
    department_id UUID NOT NULL REFERENCES Departments(id),
    full_name VARCHAR(255) NOT NULL,
    specialization VARCHAR(150),
    working_hours JSONB NOT NULL, -- Format: { "days": [1,2,3,4,5], "start_time": "09:00", "end_time": "17:00", "break": {"start": "12:00", "end": "13:00"}, "slot_duration": 30 }
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 5. Appointments Table (The Core Payload)
CREATE TABLE Appointments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    patient_id UUID NOT NULL REFERENCES Patients(id),
    doctor_id UUID NOT NULL REFERENCES Doctors(id),
    appointment_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    status appointment_status DEFAULT 'Scheduled',
    queue_number INT,
    qr_code_url VARCHAR(500),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Deterministic Constraint: Ensure start_time is before end_time
    CONSTRAINT chk_time_order CHECK (start_time < end_time)
);

-- Unique index to prevent Double Bookings at the database layer.
-- This ensures a doctor cannot have two active appointments starting at the same time on the same day.
-- We only apply this to 'Scheduled' or 'Completed' appointments using a partial index.
CREATE UNIQUE INDEX idx_unique_active_appointment
ON Appointments(doctor_id, appointment_date, start_time)
WHERE status IN ('Scheduled', 'Completed');

-- 6. Notifications Table
CREATE TABLE Notifications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES Users(id) ON DELETE CASCADE,
    type notification_type NOT NULL,
    status notification_status DEFAULT 'Pending',
    payload JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Row Level Security (RLS) can be enabled later.
