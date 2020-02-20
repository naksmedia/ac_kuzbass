$('#refresh-captcha').click(function (event) {
  event.preventDefault();
  $.getJSON("/captcha/refresh/", function (result) {
      $('.captcha').attr('src', result['image_url']);
      $('#id_captcha_0').val(result['key'])
  });

});

$('#order_service_button').click(function(event) {
    event.preventDefault();
    order = $('#order_form').serializeArray();
    $('.choose__item ul li').each(function() {
        if ($(this).hasClass('selected')) {
          // console.log('DATA', $(this).data('order'));
          order.push({"name": $(this).data('order'), "value": "selected"});
        }
      });
    // console.table(order);
    console.log(order)
    $.post('/accept_order/', order)
      .done(response=>{
          if (response['order_id']) {
            var id = response['order_id'];
            $('.modal-title:visible').text('Спасибо!');
            $('.modal__title__small__text:visible').hide();
            $('.modal-body:visible').html(`
            <h3 class="text text-info">
              Обращение зарегистрировано, идентификатор заявки ${id}
            </h3>
            <p class="text text-primary py-3">
              В ближайшее время с Вами свяжется наш специалист
            </p>
            `);
            $('.modal-footer:visible').hide();
          }

          if (response['errors']) {
            $('.invalid-feedback').remove();
            $('.border').each(function() {
              $(this).removeClass('border border-danger');
            });
            for (let key in response['errors']) {
              // remove all red borders
              // $('.border-danger').removeClass('is-invalid border border-danger');
              // $('.invalid-feedback:visible').hide();
              console.log(
                key, ":", response['errors'][key]
                );
              let form = $("#order_form");
              let element = form.find(`input[name="${key}"]`);

              // element.after(`<small class="text-danger">${response['errors'][key]}</small>`);
              element.addClass('is-invalid border border-danger');
              element.after(`<div class="invalid-feedback">${response['errors'][key]}</div>`);
              if (key == 'captcha') {
                let captcha_div = $('#order_captcha_check');
                captcha_div.addClass('border border-danger');
                captcha_div.css("border-radius", "3px");
                $('#order_captcha_message').html(
                `<p class="text text-danger">
                  ${response['errors'][key]}
                </p>`
                )}
            }
          }
        }
      )
      .fail(response=>{
        console.log('fail');
        console.log(response);
        }
      );
  });