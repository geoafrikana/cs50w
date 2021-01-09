

document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

  

});

//gotocompose function
function gotocompose(mail_id){
  document.querySelector('#compose-view').style.display = 'block'
  document.querySelector('#emails-view').style.display = 'none'

  fetch(`/emails/${mail_id}`)
.then(response => response.json())
.then(email => {
 
    document.querySelector('#compose-recipients').value = email.sender
    var res = email.subject.slice(0, 4);
  if ("RE: "  == res){
    document.querySelector('#compose-subject').value = email.subject
  }else{
    document.querySelector('#compose-subject').value = `Re: ${email.subject}`
  }
  document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote:\n ${email.body}`


});
}

//archive function
function archivefunct(idofmail){
  //check if mail is archived
  fetch(`/emails/${idofmail}`)
  .then(response => response.json())
  .then(email => {
      // Print emails
      const archivestatus = email.archived;

      //place (un)archive logic below this line
      if(archivestatus){
        //unarchive
        fetch(`/emails/${idofmail}`, {
          method: 'PUT',
          body: JSON.stringify({
              archived: false
          })
        })
        load_mailbox('inbox')
      }
      else{
        //archive mail
        fetch(`/emails/${idofmail}`, {
          method: 'PUT',
          body: JSON.stringify({
              archived: true
          })
        })
        load_mailbox('inbox')
        
      }
  })

  
  //load the inbox
  
}
//href function

function hrefFunction(email_id){


  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
      // Print emails
       if (email.sender == useremail){
          //sent mailbox logic
          document.querySelector('#emails-view').innerHTML +=  `<div>
      <h3>${email.subject}</h3><hr>
      <p><b>Sender:</b> ${email.sender}</p><hr>
      <p><b>Recipients:</b> ${email.recipients}</p><hr>
      <p>${email.timestamp}</p><hr>
      <p>${email.body}</p>
  </div>`
        }
        else{
          document.querySelector('#emails-view').innerHTML +=  `<div>
      <h3>${email.subject}</h3><hr>
      <p><b>Sender:</b> ${email.sender}</p><hr>
      <p><b>Recipients:</b> ${email.recipients}</p><hr>
      <p>${email.timestamp}</p><hr>
      <p>${email.body}</p>
      <button type="button" class="btn btn-primary" id='archivebutton' onclick="archivefunct(${email.id})"><i class="fa fa-folder"></i></button>
      <button type="button" class="btn btn-primary" id='gotocompose' onclick="gotocompose(${email.id})">Reply</button>
  </div>`
        }
      //sender, recipients, subject, timestamp, and body

      

} );
document.querySelector('#inbox-list').style.display = 'none'
document.querySelector('#mailbox-title').style.display = 'none'

fetch(`/emails/${email_id}`, {
  method: 'PUT',
  body: JSON.stringify({
      read: true
  })
})



}


function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {

  document.querySelector('#emails-view').innerHTML = `<h3 id= 'mailbox-title'>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      // Print emails

      document.querySelector('#emails-view').innerHTML +=  `<div id='inbox-list'>

      <table class="table table-sm">
          <thead class="text-info">
          <tr>
          <th>Sender</th>
          <th>Subject</th>
          <th>Time</th>
          </tr>
          </thead>
           </table>
  </div>`

      emails.forEach((item) => {
      
      mail_archived =  item.archived
      mail_body= item.body
      mail_id=  item.id
      mail_read =  item.read
      mail_recipients=  item.recipients
      mail_sender =  item.sender
      mail_subject =  item.subject
      mail_timestamp = item.timestamp

        
       if(mail_read==false){
            document.querySelector('.table').innerHTML +=
          `<tr  onclick='hrefFunction(${mail_id})'>  
          <td id='sender'>${mail_sender}</td>
             <td id='subject'>${mail_subject}</td>
          <td id='timestamp'>${mail_timestamp}</td>
          </tr>`   
       } 
       else{document.querySelector('.table').innerHTML +=
      `<tr class= 'bg-secondary text-light' onclick='hrefFunction(${mail_id})'>
      <td id='sender'>${mail_sender}</td>
         <td id='subject'>${mail_subject}</td>
      <td id='timestamp'>${mail_timestamp}</td>
      </tr>
      ` 
  }       
  
  
  
 
          
      });


     
      // ... do something else with emails ...
      
  // Show the mailbox and hide other views
  
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
 

  

      
  });
}