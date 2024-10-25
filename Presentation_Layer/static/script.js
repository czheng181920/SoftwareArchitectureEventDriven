// static/script.js
document.addEventListener('DOMContentLoaded', function () {
  console.log('JavaScript is loaded!');
});

// Function to handle changes in the main dropdown (Meetings, Calendars, Participants, Attachments)
function handleOptionChange() {
  const selectedOption = document.getElementById("choice").value;

  // Hide all forms initially
  document.getElementById("meetingForm").style.display = "none";
  document.getElementById("calendarForm").style.display = "none";
  document.getElementById("participantsForm").style.display = "none";
  document.getElementById("attachmentsForm").style.display = "none";

  // Show the relevant form based on the user's choice
  if (selectedOption === "1") {
    document.getElementById("meetingForm").style.display = "block";
  } else if (selectedOption === "2") {
    document.getElementById("calendarForm").style.display = "block";
  } else if (selectedOption === "3") {
    document.getElementById("participantsForm").style.display = "block";
  } else if (selectedOption === "4") {
    document.getElementById("attachmentsForm").style.display = "block";
  }
}

// Function to handle changes in the meeting management options
function handleMeetingOptionChange() 
{
  const selectedMeetingOption = document.getElementById("meeting-option").value;
  
  const meetingIdSection = document.getElementById("meeting-id-section");
  const meetingTitleSection = document.getElementById("meeting-title-section");
  const meetingDateSection = document.getElementById("meeting-date-section");
  const meetingLocationSection = document.getElementById("meeting-location-section");
  const meetingDetailsSection = document.getElementById("meeting-details-section");
  const meetingSubmitSection = document.getElementById("meeting-submit-section");
  
  const meetingSubmitButton = document.getElementById("submitButton");


  // Display the meeting ID input field only for options that require it
  if (selectedMeetingOption === "1" || selectedMeetingOption === "4") 
  {
    // Creating meetings and querying meeting by id 
    meetingIdSection.style.display = "block";
    meetingTitleSection.style.display = "block";  
    meetingDateSection.style.display = "block";    
    meetingLocationSection.style.display = "block";    
    meetingDetailsSection.style.display = "block";
    meetingSubmitSection.style.display = "block";
  } 
  else if (selectedMeetingOption === "2") 
  {
    // querying all meeting id
    meetingIdSection.style.display = "none";
    meetingTitleSection.style.display = "none";   
    meetingDateSection.style.display = "none";    
    meetingLocationSection.style.display = "none";    
    meetingDetailsSection.style.display = "none"; 
    meetingSubmitSection.style.display = "block";    
  } 
  else {
    // update, delete, list of cal for meeting, list of attachement, list of participants
    meetingIdSection.style.display = "block";
    meetingTitleSection.style.display = "none";
    meetingDateSection.style.display = "none";    
    meetingLocationSection.style.display = "none";    
    meetingDetailsSection.style.display = "none";
    meetingSubmitSection.style.display = "block";    
  }

  meetingSubmitButton.onclick = function() {
    if (selectedMeetingOption === "1") {
      meetingSubmit();
    } else if (selectedMeetingOption === "2") {
      meetingQuery();
    } else if (selectedMeetingOption === "3") {
      meetingQueryByID();
    } else if (selectedMeetingOption === "4") {
      updateMeeting();
    } else if (selectedMeetingOption === "5") {
      deleteMeeting();
    } else if (selectedMeetingOption === "6") {
      listOfCalendarsMeeting();
    } else if (selectedMeetingOption === "7") {
      listofParticipantsMeeting();
    } else if (selectedMeetingOption === "8") {
      listofAttachmentsMeeting();
    }
  };
  
}

// Function to handle changes in the calendar management options
function handleCalendarOptionChange() 
{
  const selectedCalendarOption = document.getElementById("calendar-option").value;
  
  const calendarIdSection = document.getElementById("calendar-id-section");
  const meetingIdSection = document.getElementById("meeting-id-section");
  const calendarTitleSection = document.getElementById("calendar-title-section");
  const calendarDetailsSection = document.getElementById("calendar-details-section");
  const calendarSubmitSection = document.getElementById("calendar-submit-section");
  
  const calendarSubmitButton = document.getElementById("calendarSubmitButton");

  console.log(selectedCalendarOption);

  // Display the meeting ID input field only for options that require it
  if (selectedCalendarOption === "1" || selectedCalendarOption === "4") {
    // Creating or querying all meetings does not require a meeting ID
    calendarIdSection.style.display = "block";  
    calendarTitleSection.style.display = "block";    
    calendarDetailsSection.style.display = "block";
    calendarSubmitSection.style.display = "block";
    meetingIdSection.style.display= "none";
  } 
  else if (selectedCalendarOption === "2") {
    // Creating or querying all meetings does not require a meeting ID
    calendarIdSection.style.display = "none";
    calendarTitleSection.style.display = "none";       
    calendarDetailsSection.style.display = "none"; 
    calendarSubmitSection.style.display = "block";    
    meetingIdSection.style.display= "none";
  } 
  else if (selectedCalendarOption === "7") {
    calendarIdSection.style.display = "block";
    meetingIdSection.style.display= "block";
    calendarSubmitSection.style.display = "block"; 
  } else {
    // Other options (query by ID, update, delete) require a meeting ID
    calendarIdSection.style.display = "block";
    calendarTitleSection.style.display = "none";   
    calendarDetailsSection.style.display = "none";
    calendarSubmitSection.style.display = "block";   
    meetingIdSection.style.display= "none";
  }

  calendarSubmitButton.onclick = function() 
  {
    if (selectedCalendarOption === "1") 
    {
      addCalendar();
    } else if (selectedCalendarOption === "2") {
      allCalendar();
    } else if (selectedCalendarOption === "3") {
      findCalendarById()
    } else if (selectedCalendarOption === "4") {
      updateCalendar();
    } else if (selectedCalendarOption === "5") {
      deleteCalendar();
    } else if (selectedCalendarOption === "6") {
      allMeetinginCalendar();
    } else if (selectedCalendarOption === "7") {
      associateMeetingWithCalendar()
    }
  };

}

// Function to handle changes in the participant management options
function handleParticipantOptionChange() 
{
  const selectedParticipantOption = document.getElementById("participant-option").value;
  
  const participantIdSection = document.getElementById("participant-id-section");
  const meetingIdSection = document.getElementById("meeting-id-section-participant");
  const participantNameSection = document.getElementById("participant-name-section");
  const participantEmailSection = document.getElementById("participant-email-section");

  const participantSubmitSection = document.getElementById("participant-submit-section"); 
  const participantSubmitButton = document.getElementById("participantSubmitButton")

  // Display the meeting ID input field only for options that require it
  if (selectedParticipantOption === "1" || selectedParticipantOption === "4") 
  {
    // Creating or querying all meetings does not require a meeting ID
    participantIdSection.style.display = "block";  
    meetingIdSection.style.display = "block";  
    participantNameSection.style.display = "block";    
    participantEmailSection.style.display = "block"; 
    participantSubmitSection.style.display = "block";  
  } 
  else if (selectedParticipantOption === "2") {
    // Creating or querying all meetings does not require a meeting ID
    participantIdSection.style.display = "none";
    participantNameSection.style.display = "none";       
    participantEmailSection.style.display = "none";  
    meetingIdSection.style.display = "none"; 
    participantSubmitSection.style.display = "block";  
  } else {
    // Other options (query by ID, update, delete) require a meeting ID
    participantIdSection.style.display = "block";
    //meetingIdSection.style.display = "block";
    participantNameSection.style.display = "none";   
    participantEmailSection.style.display = "none"; 
    participantSubmitSection.style.display = "block";     
  }

  participantSubmitButton.onclick = function() 
  {
    if (selectedParticipantOption === "1") 
    {
      addParticipant();
    } else if (selectedParticipantOption === "2") {
      allParticipants();
    } else if (selectedParticipantOption === "3") {
      findParticipantById()
    } else if (selectedParticipantOption === "4") {
      updateParticipant();
    } else if (selectedParticipantOption === "5") {
      deleteParticipant();
    } 
  };

}

// Function to handle changes in the attachment management options
function handleAttachmentOptionChange() {
  const selectedAttachmentOption = document.getElementById("attachment-option").value;
  
  const attachmentIdSection = document.getElementById("attachment-id-section");
  const meetingIdSection = document.getElementById("meeting-id-section-attachment");
  const attachmentUrlSection = document.getElementById("attachment-url-section");
  const attachmentSubmitButton = document.getElementById("attachmentSubmitButton");

  const attachmentSubmitSection = document.getElementById("attachment-submit-section");

  // Display the meeting ID input field only for options that require it
  if (selectedAttachmentOption === "1" || selectedAttachmentOption === "4") {
    // Creating or querying all meetings does not require a meeting ID
    attachmentIdSection.style.display = "block";  
    meetingIdSection.style.display = "block";  
    attachmentUrlSection.style.display = "block";
    attachmentSubmitSection.style.display = "block";    
  } 
  else if (selectedAttachmentOption === "2") {
    // Creating or querying all meetings does not require a meeting ID
    attachmentIdSection.style.display = "none";
    meetingIdSection.style.display = "none";  
    attachmentUrlSection.style.display = "none";
    attachmentSubmitSection.style.display = "block"; 

  } else {
    // Other options (query by ID, update, delete) require a meeting ID
    attachmentIdSection.style.display = "block";
    meetingIdSection.style.display = "none";  
    attachmentUrlSection.style.display = "none";
     attachmentSubmitSection.style.display = "block";    
  }

  attachmentSubmitButton.onclick = function() 
  {
    if (selectedAttachmentOption === "1") 
    {
      addAttachment();
    } else if (selectedAttachmentOption === "2") {
      allAttachments();
    } else if (selectedAttachmentOption === "3") {
      findAttachmentById()
    } else if (selectedAttachmentOption === "4") {
      updateAttachment();
    } else if (selectedAttachmentOption === "5") {
      deleteAttachment();
    } 
  };

}

async function meetingSubmit()
{
    const meetingID = document.getElementById("meeting-id").value;
    const meetingTitle = document.getElementById("meeting-title").value;
    const meetingDate = document.getElementById("meeting-date").value; 
    const meetingLocation = document.getElementById("meeting-location").value;
    const meetingDetails = document.getElementById("meeting-details").value; 

    // Create JSON object
    const data = {
      meeting_id: meetingID,
      title: meetingTitle, 
      date_time: meetingDate, 
      location: meetingLocation, 
      details: meetingDetails
      };

    // Send POST request
    try 
    {
      const response = await fetch('/addMeeting', 
        {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      });
    
      if (response.ok) 
      {
        const responseData = await response.json();
        console.log('Meeting created successfully:', responseData);
      } 
      else 
      {
        console.error('Error creating meeting:', response.status);
       
      }
    } 
    catch (error) 
    {
      console.error('Error:', error);
      
    }
}

async function meetingQuery()
{
  try {
    const response = await fetch('/allMeetings');

    if (response.ok) 
      {
      const meetingsData = await response.json();
      console.log(meetingsData);
      const meetingsList = document.getElementById('meetingsList');

      meetingsList.innerHTML = ''; // Clear previous content

      meetingsData.forEach(meeting => 
        {
        const meetingItem = document.createElement('li');
        meetingItem.innerHTML = `
          <strong>ID:</strong> ${meeting[0] || 'N/A'}<br>
          <strong>Title:</strong> ${meeting[1] || 'N/A'}<br>
          <strong>Date:</strong> ${meeting[2] || 'N/A'}<br>
          <strong>Location:</strong> ${meeting[3] || 'N/A'}<br>
          <strong>Details:</strong> ${meeting[4] || 'N/A'}
        `;
        meetingsList.appendChild(meetingItem);
      });
    } 
    else {
      console.error('Error retrieving meetings:', response.status);
    }
  } 
  catch (error) {
    console.error('Error:', error);
  }

}

async function meetingQueryByID() 
{
  const meetingID = document.getElementById("meeting-id").value;

  if (!meetingID) {
      console.error('Meeting ID is required.');
      return; // Exit the function if meeting ID is not provided
  }
  
  try {
      // Send a GET request to the endpoint with the meeting ID as a query parameter
      const response = await fetch(`/meetingByID?meeting-id=${encodeURIComponent(meetingID)}`, {
          method: 'GET',
          headers: {
              'Content-Type': 'application/json',
          },
      });

      if (response.ok) {
          const meetingData = await response.json();
          console.log('Meeting retrieved successfully:', meetingData);
          
          const meetingDetails = document.getElementById('meetingsList'); // Change to your actual HTML element
          meetingDetails.innerHTML = `
              <strong>ID:</strong> ${meetingData[0][0] || 'N/A'}<br>
              <strong>Title:</strong> ${meetingData[0][1] || 'N/A'}<br>
              <strong>Date:</strong> ${meetingData[0][2] || 'N/A'}<br>
              <strong>Location:</strong> ${meetingData[0][3] || 'N/A'}<br>
              <strong>Details:</strong> ${meetingData[0][4] || 'N/A'}
          `;
      } else {
          console.error('Error retrieving meeting:', response.status);
      }
  } catch (error) {
      console.error('Error:', error);
  }
}


async function updateMeeting()
{

  const meetingID = document.getElementById("meeting-id").value;
  const meetingTitle = document.getElementById("meeting-title").value;
  const meetingDate = document.getElementById("meeting-date").value; 
  const meetingLocation = document.getElementById("meeting-location").value;
  const meetingDetails = document.getElementById("meeting-details").value; 

    // Create JSON object
    const data = {
      meeting_id: meetingID,
      title: meetingTitle, 
      date_time: meetingDate, 
      location: meetingLocation, 
      details: meetingDetails
      };

    try {
        const response = await fetch('/updateMeeting', 
          {
            method: 'PUT',
            headers: 
            {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        if (response.ok) 
          {
            const updatedMeeting = await response.json();
            console.log('Updated Meeting:', updatedMeeting);
        } 
        else 
        {
            console.error('Error updating meeting:', response.status);
        }
    } 
    catch (error) 
    {
        console.error('Error:', error);
    }
}

async function deleteMeeting() {
  const meetingID = document.getElementById("meeting-id").value; // Get the meeting ID

  // Create JSON object
  const data = {
      meeting_id: meetingID
  };

  try {
      const response = await fetch('/deleteMeeting', {
          method: 'DELETE',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify(data),
      });

      if (response.ok) {
          const result = await response.json();
          console.log('Meeting deleted successfully:', result.message);
          // Optionally, you can update the UI to reflect the deletion
      } else {
          console.error('Error deleting meeting:', response.status);
      }
  } catch (error) {
      console.error('Error:', error);
  }
}

async function listOfCalendarsMeeting() {
  const meetingID = document.getElementById("meeting-id").value; // Get the meeting ID

  try {
    const response = await fetch(`/listofCalendars?meeting_id=${meetingID}`, {
      method: 'GET', // Keep it GET
      headers: {
        'Content-Type': 'application/json',
      }
    });

    if (response.ok) {
      const calendarsData = await response.json();
      console.log('Calendars retrieved successfully:', calendarsData);
      
      const calendarsList = document.getElementById('calendarsList'); // Assuming you have a <ul> or <div> with this ID

      calendarsList.innerHTML = '';
      console.log(calendarsData.length)

      // Check if the calendarsData has data and is an array
      if (Array.isArray(calendarsData) && calendarsData.length > 0) {
        calendarsData.forEach(calendar => {
          const calendarItem = document.createElement('li');
          calendarsList.innerHTML = `
              <strong>ID:</strong> ${calendarsData[0][0] || 'N/A'}<br>
              <strong>Name:</strong> ${calendarsData[0][1] || 'N/A'}<br>
              <strong>Details:</strong> ${calendarsData[0][2] || 'N/A'}<br>
          `;
          calendarsList.appendChild(calendarItem);
        });
      } else {
        calendarsList.innerHTML = '<li>No calendars found for this meeting.</li>'; // Handle empty response
      }
    } else {
      console.error('Error retrieving calendars:', response.status);
    }
  } catch (error) {
    console.error('Error:', error);
  }
}

async function listofParticipantsMeeting()
{

}

async function listofAttachmentsMeeting()
{

}

async function addCalendar()
{
  const calendarId = document.getElementById("calendar-id").value;
  const calendarTitle = document.getElementById("calendar-title").value;
  const calendarDetails = document.getElementById("calendar-details").value;

  // Create JSON object
  const data = {
    calendar_id: calendarId,
    title: calendarTitle,
    details: calendarDetails
  };

  // Send POST request
  try {
    const response = await fetch('/calendar', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    });

    if (response.ok) {
      const responseData = await response.json();
      console.log('Calendar created successfully:', responseData);
    } else {
      console.error('Error creating calendar:', response.status);
    }
  } catch (error) {
    console.error('Error:', error);
  }
}

async function allCalendar() {
  try {
    const response = await fetch('/allCalendars', {
      method: 'GET'
    });

    if (response.ok) {
      const calendarData = await response.json();
      console.log('Calendars retrieved successfully:', calendarData);
      
      const calendarDetails = document.getElementById('calendarList'); // Change to your actual HTML element
      calendarDetails.innerHTML = ''; // Clear previous content

      // Check if the calendarData has data and is an array
      if (Array.isArray(calendarData) && calendarData.length > 0) {
        calendarData.forEach(calendar => {
          const calendarItem = document.createElement('li'); // Create a new list item for each calendar
          calendarItem.innerHTML = `
            <strong>ID:</strong> ${calendar[0] || 'N/A'}<br>
            <strong>Title:</strong> ${calendar[1] || 'N/A'}<br>
            <strong>Details:</strong> ${calendar[2] || 'N/A'}
          `;
          calendarDetails.appendChild(calendarItem); // Append the new item to the calendarDetails element
        });
      } else {
        calendarDetails.innerHTML = '<li>No calendars found.</li>'; // Handle empty response
      }
    } else {
      console.error('Error retrieving calendars:', response.status);
    }
  } catch (error) {
    console.error('Error:', error);
  }
}

async function findCalendarById() {
  const calendarID = document.getElementById("calendar-id").value;

  if (!calendarID) {
    console.error('Calendar ID is required.');
    return; 
  }
  
  try {
    const response = await fetch(`/findCalendarById?calendar-id=${encodeURIComponent(calendarID)}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (response.ok) {
      const calendarData = await response.json();
      console.log('Calendar retrieved successfully:', calendarData);
      
      const calendarDetails = document.getElementById('calendarList'); // Change to your actual HTML element
      calendarDetails.innerHTML = ''; // Clear previous content

      // Check if calendarData has data and is an array
      if (Array.isArray(calendarData) && calendarData.length > 0) {
        // Display details of the found calendar
        const calendarItem = document.createElement('li');
        calendarItem.innerHTML = `
          <strong>ID:</strong> ${calendarData[0] || 'N/A'}<br>
          <strong>Title:</strong> ${calendarData[1] || 'N/A'}<br>
          <strong>Details:</strong> ${calendarData[2] || 'N/A'}
        `;
        calendarDetails.appendChild(calendarItem);
      } else {
        calendarDetails.innerHTML = '<li>No calendar found with this ID.</li>'; // Handle no data case
      }
    } else {
      console.error('Error retrieving calendar:', response.status);
    }
  } catch (error) {
    console.error('Error:', error);
  }
}

async function updateCalendar()
{
  const calendarID = document.getElementById("calendar-id").value;
  const calendarTitle = document.getElementById("calendar-title").value;
  const calendarDetails = document.getElementById("calendar-details").value; 
  console.log('js'+ calendarTitle);

    // Create JSON object
    const data = {
      calendar_id: calendarID,
      calendar_title: calendarTitle,  
      calendar_details: calendarDetails
      };

    try {
        const response = await fetch('/updateCalendar', 
          {
            method: 'PUT',
            headers: 
            {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        if (response.ok) 
          {
            const updatedCalendar= await response.json();
            console.log('Updated Calendar:', updatedCalendar);
        } 
        else 
        {
            console.error('Error updating calendar:', response.status);
        }
    } 
    catch (error) 
    {
        console.error('Error:', error);
    }


}

async function deleteCalendar()
{
  const calendarID = document.getElementById("calendar-id").value; 

  const data = {
      calendar_id: calendarID
  };

  try {
      const response = await fetch('/deleteCalendar', {
          method: 'DELETE',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify(data),
      });

      if (response.ok) 
      {
          const result = await response.json();
          console.log('Calendar deleted successfully:', result.message);
      } 
      else 
      {
          console.error('Error deleting calendar:', response.status);
      }
  } 
  catch (error) 
  {
      console.error('Error:', error);
  }



}

async function allMeetinginCalendar()
{
  

}


async function associateMeetingWithCalendar() {
  const meetingId = document.getElementById("meeting-id").value;
  const calendarId = document.getElementById("calendar-id").value;

  // Create the data object to send
  const data = {
    meeting_id: meetingId,
    calendar_id: calendarId
  };

  try {
    const response = await fetch('/addMeetingToCalendar', 
      {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    });

    if (response.ok) {
      const responseData = await response.json();
      console.log('Meeting associated with calendar successfully:', responseData);
    } else {
      console.error('Error associating meeting with calendar:', response.status);
    }
  } catch (error) {
    console.error('Error:', error);
  }
}

// Add a new participant
async function addParticipant() {
  const participantID = document.getElementById("participant-id").value;
  const meetingID = document.getElementById("meeting-id-participant").value;
  const participantName = document.getElementById("participant-name").value;
  const participantEmail = document.getElementById("participant-email").value;

  const data = {
    participant_id: participantID,
    meeting_id: meetingID, 
    name: participantName,
    email: participantEmail
  };

  try {
    const response = await fetch('/addParticipant', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    });

    if (response.ok) {
      const responseData = await response.json();
      console.log('Participant added successfully:', responseData);
    } else {
      console.error('Error adding participant:', response.status);
    }
  } catch (error) {
    console.error('Error:', error);
  }
}

// Get all participants
async function allParticipants() {
  try {
    const response = await fetch('/allParticipants', {
      method: 'GET',
      /*headers: {
        'Content-Type': 'application/json'
      }
      */
    });

    if (response.ok) {
      const participantData = await response.json();
      console.log('Participants retrieved successfully:', participantData);

      const participantList = document.getElementById('participantList'); // Replace with your actual HTML element
      participantList.innerHTML = ''; // Clear previous content

      // Check if participantData is an array and has data
      if (Array.isArray(participantData) && participantData.length > 0) {
        participantData.forEach(participant => {
          const participantItem = document.createElement('li'); // Create list item for each participant
          participantItem.innerHTML = `
            <strong>ID:</strong> ${participant[0] || 'N/A'}<br>
            <strong>Name:</strong> ${participant[1] || 'N/A'}<br>
            <strong>Email:</strong> ${participant[2] || 'N/A'}
          `;
          participantList.appendChild(participantItem); // Append to list
        });
      } else {
        participantList.innerHTML = '<li>No participants found.</li>'; // Handle empty response
      }
    } else {
      console.error('Error retrieving participants:', response.status);
    }
  } catch (error) {
    console.error('Error:', error);
  }
}

// Find a participant by ID
async function findParticipantById() {
  const participantID = document.getElementById("participant-id").value;

  if (!participantID) {
    console.error('Participant ID is required.');
    return;
  }

  try {
    const response = await fetch(`/participantsByID?participant_id=${encodeURIComponent(participantID)}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (response.ok) {
      const participantData = await response.json();
      console.log('Participant retrieved successfully:', participantData);

      const participantList = document.getElementById('participantList'); // Replace with your actual HTML element
      participantList.innerHTML = ''; // Clear previous content

      if (Array.isArray(participantData) && participantData.length > 0) {
        const participantItem = document.createElement('li');
        participantItem.innerHTML = `
          <strong>ID:</strong> ${participantData[0] || 'N/A'}<br>
          <strong>Name:</strong> ${participantData[1] || 'N/A'}<br>
          <strong>Email:</strong> ${participantData[2] || 'N/A'}
        `;
        participantList.appendChild(participantItem);
      } else {
        participantList.innerHTML = '<li>No participant found with this ID.</li>';
      }
    } else {
      console.error('Error retrieving participant:', response.status);
    }
  } catch (error) {
    console.error('Error:', error);
  }
}

// Update a participant
async function updateParticipant() {
  const participantID = document.getElementById("participant-id").value;
  const participantName = document.getElementById("participant-name").value;
  const participantEmail = document.getElementById("participant-email").value;

  const data = {
    participant_id: participantID,
    name: participantName,
    email: participantEmail
  };

  try {
    const response = await fetch('/updateParticipants', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data)
    });

    if (response.ok) {
      const updatedParticipant = await response.json();
      console.log('Participant updated successfully:', updatedParticipant);
    } else {
      console.error('Error updating participant:', response.status);
    }
  } catch (error) {
    console.error('Error:', error);
  }
}

// Delete a participant
async function deleteParticipant() {
  const participantID = document.getElementById("participant-id").value;

  const data = {
    participant_id: participantID
  };

  try {
    const response = await fetch('/deleteParticipants', {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data)
    });

    if (response.ok) {
      const result = await response.json();
      console.log('Participant deleted successfully:', result.message);
    } else {
      console.error('Error deleting participant:', response.status);
    }
  } catch (error) {
    console.error('Error:', error);
  }
}

// Add a new attachment
async function addAttachment() {
  const attachmentID = document.getElementById("attachment-id").value;
  const meetingID = document.getElementById("meeting-id-attachment").value;
  const attachmentURL = document.getElementById("attachment-url").value;

  const data = {
    attachment_id: attachmentID,
    meeting_id: meetingID,
    url: attachmentURL
  };

  try {
    const response = await fetch('/attachment', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    });

    if (response.ok) {
      const responseData = await response.json();
      console.log('Attachment added successfully:', responseData);
    } else {
      console.error('Error adding attachment:', response.status);
    }
  } catch (error) {
    console.error('Error:', error);
  }
}

// Get all attachments
async function allAttachments() {
  try {
    const response = await fetch('/attachments', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    });

    if (response.ok) {
      const attachmentData = await response.json();
      console.log('Attachments retrieved successfully:', attachmentData);

      const attachmentList = document.getElementById('attachmentList'); // Replace with your actual HTML element
      attachmentList.innerHTML = ''; // Clear previous content

      // Check if attachmentData is an array and has data
      if (Array.isArray(attachmentData) && attachmentData.length > 0) {
        attachmentData.forEach(attachment => {
          const attachmentItem = document.createElement('li'); // Create list item for each attachment
          attachmentItem.innerHTML = `
            <strong>ID:</strong> ${attachment[0] || 'N/A'}<br>
            <strong>Name:</strong> ${attachment[1] || 'N/A'}<br>
            <strong>File:</strong> ${attachment[2] || 'N/A'}
          `;
          attachmentList.appendChild(attachmentItem); // Append to list
        });
      } else {
        attachmentList.innerHTML = '<li>No attachments found.</li>'; // Handle empty response
      }
    } else {
      console.error('Error retrieving attachments:', response.status);
    }
  } catch (error) {
    console.error('Error:', error);
  }
}

// Find an attachment by ID
async function findAttachmentById() {
  const attachmentID = document.getElementById("attachment-id").value;

  if (!attachmentID) {
    console.error('Attachment ID is required.');
    return;
  }

  try {
    const response = await fetch(`/attachmentById?attachment_id=${encodeURIComponent(attachmentID)}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (response.ok) {
      const attachmentData = await response.json();
      console.log('Attachment retrieved successfully:', attachmentData);

      const attachmentList = document.getElementById('attachmentList'); // Replace with your actual HTML element
      attachmentList.innerHTML = ''; // Clear previous content

      if (Array.isArray(attachmentData) && attachmentData.length > 0) {
        const attachmentItem = document.createElement('li');
        attachmentItem.innerHTML = `
          <strong>ID:</strong> ${attachmentData[0] || 'N/A'}<br>
          <strong>Name:</strong> ${attachmentData[1] || 'N/A'}<br>
          <strong>File:</strong> ${attachmentData[2] || 'N/A'}
        `;
        attachmentList.appendChild(attachmentItem);
      } else {
        attachmentList.innerHTML = '<li>No attachment found with this ID.</li>';
      }
    } else {
      console.error('Error retrieving attachment:', response.status);
    }
  } catch (error) {
    console.error('Error:', error);
  }
}

// Update an attachment
async function updateAttachment() {
  const attachmentID = document.getElementById("attachment-id").value;
  const attachmentFile = document.getElementById("attachment-file").value; // Assuming only the URL needs to be updated

  const data = {
    url: attachmentFile // Adjusted to match what your backend expects
  };

  try {
    const response = await fetch(`/attachment/${attachmentID}`, { // Updated endpoint
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data)
    });

    if (response.ok) {
      const updatedAttachment = await response.json();
      console.log('Attachment updated successfully:', updatedAttachment);
    } else {
      console.error('Error updating attachment:', response.status);
    }
  } catch (error) {
    console.error('Error:', error);
  }
}

// Delete an attachment
async function deleteAttachment() {
  const attachmentID = document.getElementById("attachment-id").value;

  try {
    const response = await fetch(`/attachment/${attachmentID}`, { // Updated endpoint
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      }
    });

    if (response.ok) {
      const result = await response.json();
      console.log('Attachment deleted successfully:', result.message || 'Attachment deleted.');
    } else {
      console.error('Error deleting attachment:', response.status);
    }
  } catch (error) {
    console.error('Error:', error);
  }
}








