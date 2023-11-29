$(document).ready(() => {

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
          const cookies = document.cookie.split(';');
          for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
            }
          }
        }
        return cookieValue;
      }
      const csrftoken = getCookie('csrftoken');

    // Delete Question
    var $deletebtn = $("#delete_question_btn")
    $deletebtn.click((e) => {
        var $checkedboxes = $("input[type='checkbox']:checked").map((i, el) => el.value).get()

        $.ajax({
            type: 'GET',
            url: $deletebtn.data('url'),
            data: {
                checkedboxes: $checkedboxes
            },
            success: (response) => {
                location.reload()
            }
        })

    })
console.log("hello")
    // Delete Question
    var $deletebtn = $("#delete_interest_btn")
    $deletebtn.click((e) => {
        var $checkedboxes = $("input[type='checkbox']:checked").map((i, el) => el.value).get()

        $.ajax({
            type: 'POST',
            url: $deletebtn.data('url'),
            data: {
                checkedboxes: $checkedboxes
            },
            headers: {
                'X-CSRFToken': csrftoken
              },
            success: (response) => {
                location.reload()
            }
        })

    })

    htmx.on('htmx:load', (e) => {
        setTimeout(function () {
            $("#id_alert").fadeOut("slow")
        }, 2000);
    })

})