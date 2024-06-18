function validateBookingDates(startDate, endDate) {
    const today = new Date();
    today.setHours(0, 0, 0, 0); // Set to midnight to ignore time differences

    // Convert startDate and endDate strings to Date objects
    const start = new Date(startDate);
    const end = new Date(endDate);

    // Validation: Start date should not be in the past
    if (start < today) {
        return { isValid: false, message: "Start date cannot be in the past." };
    }

    // Validation: End date should be after start date
    if (end <= start) {
        return { isValid: false, message: "End date should be after the start date." };
    }

    // If all validations pass
    return { isValid: true, message: "Booking  Successfull." };
}


