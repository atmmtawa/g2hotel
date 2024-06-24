function validateForm() {
    // Get form inputs
    var fullName = document.getElementById("username").value;
    var email = document.getElementById("email").value;
    var password = document.getElementById("password1").value;
    var confirmPassword = document.getElementById("password2").value;
    var phoneNumber = document.getElementById("phone_number").value;
   
   
  
    // Validate full name
    if (fullName == "") {
      alert("Full Name must be filled out");
      return false;
    }
  
    // Validate email
    var emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailPattern.test(email)) {
      alert("Please enter a valid email address");
      return false;
    }
  
    // Validate password
    if (!validatePassword(password)) {
      alert("Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one number, and one special character");
      return false;
    }
  
    // Validate password confirmation
    if (password != confirmPassword) {
      alert("Passwords do not match");
      return false;
    }
  
    // Validate phone number
    var phonePattern = /^[0-9]{10}$/;
    if (!phonePattern.test(phoneNumber)) {
      alert("Please enter a valid 10-digit phone number");
      return false;
    }
    
  
    
    alert("Form submitted successfully!");
    return true;
  }
  
  function validatePassword(password) {
    var strongPasswordPattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
    return strongPasswordPattern.test(password);
  }
  