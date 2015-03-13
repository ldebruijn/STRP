$(document).ready(function () {

    var $sayhi = $('#sayhi');
    var $messages = $('#messages');
    var isopen = false;


    function message (m) {
        $messages.append($('<li></li>').html(m));
    }

    var sock =new WebSocket("ws://127.0.0.1:8888");
    sock.binaryType = "arraybuffer";

    sock.onopen = function() {
        message('Connected');
        isopen = true;
    };

    sock.onclose = function(e) {
        message('Goodbye!');
        socket = null;
        isopen = false;
    };

    sock.onmessage = function(e) {
        if (typeof e.data == "string") {
            message('New data ' + JSON.parse(e.data));
            console.log(JSON.parse(e.data));
        }
    };

    $sayhi.click(function (event) {
        event.preventDefault();
        sock.send(JSON.stringify({
            'message': 'new_input_blob',
            'data': {
                'profiles': {
                    '1' : true,
                    '2' : false,
                    '3' : true,
                    '4' : false,
                    '5' : true,
                    '6' : false,
                    '7' : false,
                    'hb' : 160 ,
                    'c1' : 'ff0000'
                }
            }
        }))
    });
});
