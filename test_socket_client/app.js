$(document).ready(function () {

    var $sayhi = $('#sayhi');
    var $messages = $('#messages');

    function message (m) {
        $messages.append($('<li></li>').html(m));
    }

    var sock = io.connect('http://localhost:8520');
    sock.on('connect', function () {
        message('Connected');
    });

    sock.on('disconnect', function () {
        message('Goodbye!');
    });

    sock.on('new_data', function (data) {
        console.log(data);
        message('New data ' + data);
    });

    $sayhi.click(function (event) {
        event.preventDefault();
        sock.emit('new_input_blob', {'profiles': {
            '1' : true,
            '2' : false,
            '3' : true,
            '4' : false,
            '5' : true,
            '6' : false,
            '7' : false,
            'hb' : 160 ,
            'c1' : 'ff0000'
        }})
    });
});
