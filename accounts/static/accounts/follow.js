$(document).ready(function () {
    $('a.follow').click(function (e) {
        e.preventDefault();
        $.post(
          $('a.follow').data('href'),
          {
            id: $(this).data('id'),
            action: $(this).data('action')
          },
          function (data) {
            console.log(data);
            if (data['status'] == 'ok') {
              var previous = $('a.follow').data('action');
              $('a.follow').data('action', previous == 'follow' ? 'unfollow' : 'follow');
              $('a.follow').text(previous == 'follow' ? 'Unfollow' : 'Follow');
              var previous_followers = parseInt($('span.count .total').text());
              $('span.count .total').text(previous == 'follow' ? previous_followers + 1 : previous_followers - 1);
            }
          });
      });
});
