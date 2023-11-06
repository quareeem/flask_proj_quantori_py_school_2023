// Login function
async function login(email, password) {
    const response = await fetch('/login', {
      method: 'POST',
      body: JSON.stringify({email, password}),
      headers: {
        'Content-Type': 'application/json'
      },
    });
  
    const data = await response.json();
  
    if (data.token) {
      // Save token
      localStorage.setItem('token', data.token);
      // Redirect to dashboard or refresh UI
    }
  }
  
  // Fetching the dashboard with token
async function getDashboard() {
    const token = localStorage.getItem('token');
    const response = await fetch('/dashboard?token=' + token);
  
    if (response.status !== 403) {
      const data = await response.text();
      // Show dashboard data
    } else {
      // Handle unauthorized access
    }
  }
  

  // Assuming you're using Fetch API
fetch("/some/api/route", {
    headers: {
        "x-access-tokens": token // the token you got from the login
    }
})


// Update userInfo when the page loads
document.addEventListener("DOMContentLoaded", function() {
    const token = localStorage.getItem('token');
    if (token) {
      // Fetch user info and update #userInfo here
      document.getElementById("userInfo").innerText = "Welcome, " + username;
    }
  });
  