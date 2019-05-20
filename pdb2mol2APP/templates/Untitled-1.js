$("#downbutton").click(function () {
    // 
    var nodes = document.querySelectorAll(".dz-finished");
    var molfiles = new Array();
    for (let node of nodes) {
        molfile = node.parentNode.parentNode.querySelector('.downloadpdb').textContent;
        molfiles.push(molfile)
    }

    parastr = molfiles.join('&molfile=')

    $.ajax({
        url: '/zip' + '?molfile=' + parastr, //
        type: 'GET',
        dataType: 'json',
        success: function (res) {
            $.ajax({ url: '/downloadall/' + res.zipfile, type: 'GET', });
        }


    });
}
);



