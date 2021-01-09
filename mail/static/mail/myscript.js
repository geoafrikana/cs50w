//my custom function for form submission
document.addEventListener('DOMContentLoaded', () =>{


//send mail and redirect to sent mailbox
    document.querySelector('#compose-form').onsubmit = () => {

        // Select all form fields and store in variables
        const recipient =  document.querySelector('#compose-recipients');
        const subject = document.querySelector('#compose-subject');
        const mailbody = document.querySelector('#compose-body');
    
      
        fetch('/emails', {
            method: 'POST',
            body: JSON.stringify({
                recipients: recipient.value,
                subject: subject.value,
                body: mailbody.value
            })
          })
          .then(response => response.json())
          .then(result => {
              // Print result
              console.log(result);
              load_mailbox('sent')
          });

      
      
      // Clear input field
      recipient.value = '' ;
      subject.value = '' ;
      mailbody.value = '' ;

      alert('done')
      
    
      // Stop form from submitting
  return false;
    };

    // document.querySelector('#inbox').onclick = ()=>{
       
    //     fetch('/emails/inbox')
    //     .then(response => response.json())
    //     .then(emails => {
    //         // Print emails
    //         console.log(emails);
    //         document.querySelector('#emails-view').innerHTML +=  `<div>

    //         <table class="table table-sm">
    //             <thead class="thead-dark">
    //             <tr>
    //             <th>Sender</th>
    //             <th>Subject</th>
    //             <th>Time</th>
    //             </tr>
    //             </thead>
    //              </table>
    //     </div>`

    //         emails.forEach((item) => {
            
    //         mail_archived =  item.archived
    //         mail_body= item.body
    //         mail_id=  item.id
    //         mail_read =  item.read
    //         mail_recipients=  item.recipients
    //         mail_sender =  item.sender
    //         mail_subject =  item.subject
    //         mail_timestamp = item.timestamp

              
    //          if(mail_read==false){
    //               document.querySelector('.table').innerHTML +=
    //             `<tr class= 'bg-secondary .text-light'>  
    //             <td id='sender'>${mail_sender}</td>
    //                <td id='subject'>${mail_subject}</td>
    //             <td id='timestamp'>${mail_timestamp}</td>
    //             </tr>`   
    //          } 
    //          else{document.querySelector('.table').innerHTML +=
    //         `<td id='sender'>${mail_sender}</td>
    //            <td id='subject'>${mail_subject}</td>
    //         <td id='timestamp'>${mail_timestamp}</td>
    //         </tr>
    //         ` 
    //     }          
                
    //         });
    //         // ... do something else with emails ...
            

            
    //     });

    // }


});
