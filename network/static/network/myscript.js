let postarrangement = `<div class="row d-flex justify-content-center mt-3">
<div class="col-12 p-3 border border-secondary">
  <div class="d-flex flex-row justify-content-between">
    <div class="p-2">
      <a href="{% url 'profile_page' post.poster %}"><p class="font-weight-bold text-primary h4">{{post.poster}}</p></a>
    </div>
    <div class="p-2"><p class="text-muted">{{post.date_time}}</p></div>
  </div>

  <p class="lead">{{post.content}}</p>

  <div class="d-flex flex-row justify-content-between">
    <div class="p-2">
      <p class="text-danger">{{ post.liker.all.count }} likes</p>
    </div>
    <div class="p-2"><p>Edit</p></div>
  </div>
</div>
</div>`


document.addEventListener('DOMContentLoaded', () => {

  document.querySelectorAll('.like-bt').forEach(button => {
    button.onclick = function () {
      // console.log(this.innerHTML)
      if (this.innerHTML == 'Like') {
        fetch(`/like/${this.dataset.like}`, {
          method: 'PUT',
          body: JSON.stringify({
            'todo': 'like',
            'postid': this.dataset.like
          })

        }).then(response => response.json())
          .then(result => {
            document.querySelector(`#likes-count${this.dataset.like}`).innerHTML = `${result.likes_count} likes`
            console.log(result)
          })
        this.innerHTML = 'Unlike'
      } else {
        fetch(`/like/${this.dataset.like}`, {
          method: 'PUT',
          body: JSON.stringify({
            'todo': 'unlike',
            'postid': this.dataset.like
          })

        }).then(response => response.json())
          .then(result => {
            document.querySelector(`#likes-count${this.dataset.like}`).innerHTML = `${result.likes_count} likes`
            console.log(result)
          })
        this.innerHTML = 'Like'
        // alert('do like')
      }

    }
  });


  document.querySelectorAll('.btn-sm').forEach(button => {

    // When a button is clicked, switch to that page
    button.onclick = function () {
      const post_content = document.querySelector(`#content${this.dataset.edit}`).innerHTML

      // action="edit/${this.dataset.edit}"
      // method='POST'
      const editform = `<form  id="compose${this.dataset.edit}" >
<textarea
  name='textarea${this.dataset.edit}'
  id="textarea${this.dataset.edit}"
  type="textarea"
  class="form-control mb-3"
  rows="3"
>${post_content}</textarea>
<input
name='submitedit${this.dataset.edit}'
  id="submitedit${this.dataset.edit}"
  type="submit"
  value="SUBMIT"
  class="form-control bg-primary text-light"
/>
</form>`

      //document.querySelector(`#${this.dataset.edit}`).style.display = 'none';
      document.querySelector(`#a${this.dataset.edit}`).innerHTML = editform;
      // const edit_content = document.querySelector(`#textarea${this.dataset.edit}`).value

      document.querySelector(`#compose${this.dataset.edit}`).onsubmit = () => {
        fetch(`/edit/${this.dataset.edit}`, {
          method: 'PUT',
          body: JSON.stringify({
            'content': document.querySelector(`#textarea${this.dataset.edit}`).value,
            'id': this.dataset.edit
          })

          //  document.querySelector(`#a${this.dataset.edit}`).innerHTML = postarrangement


          //  console.log(document.querySelector(`#textarea${this.dataset.edit}`).value)


        })
          .then(response => response.json())
          .then(result => {
            // Print result
            // console.log(result)
            document.querySelector(`#a${this.dataset.edit}`).innerHTML = `
              <div class="d-flex flex-row justify-content-between">
                <div class="p-2">
                  <a href="/profile/${result.post_poster}"><p class="font-weight-bold text-primary h4">${result.post_poster}</p></a>
                </div>
                <div class="p-2"><p class="text-muted">${result.post_date_time}</p></div>
              </div>
            
              <p class="lead">${result.post_content}</p>
            
              <div class="d-flex flex-row justify-content-between">
                <div class="p-2">
                  <p class="text-danger">${result.post_likes} likes</p>
                </div>
                <div class="p-2"><button data-edit="${result.post_id}" class='btn bg-warning btn-sm'>Edit</button></div>
                <br>
        <button data-like="${result.post_id}" class='btn bg-success like-bt'>Like</button>
              </div>
            `

          });
        return false;

      }
    }


  })


  btn = document.querySelector('#follow_button')
  id = document.querySelector('#profile_id')
  // editbtn = document.querySelector('#editbtn')


  // editbtn.onclick = () => {
  //     alert('clicked')
  // }


  btn.onclick = () => {
    fetch(`/profile/${viewed_name}`, {
      method: 'PUT',
      body: JSON.stringify({
        'value': btn.value,
        'id': id.value
      })

    }
    ).then(response => response.json())
      .then(result => {
        document.querySelector('#followed-by').innerHTML = `${result.num_followers}`
        console.log(result)
      })


    if (btn.value == 'Follow') {
      btn.value = 'Unfollow'
    }
    else {
      btn.value = 'Follow'
    }

  }

})
