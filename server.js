var http_module = require('http');
var failsistem = require('fs');
var path = require('path');

function onrequest(request, response) {
    var filePath;
    

    var urlPath = request.url === '/' ? '/index.html' : request.url;
    var localPath = path.join(__dirname, urlPath);

  
    failsistem.access(localPath, failsistem.constants.F_OK, (err) => {
        if (err) {
            // Файл не найден - 404
            response.writeHead(404, { 'Content-Type': 'text/html; charset=utf-8' });
            response.write('<h1>404 Не найдено</h1><p>Запрошенный ресурс не существует</p>');
            response.end();
            return;
        }

    
        var extname = path.extname(localPath);
        var contentType = 'text/html';
        if (extname === '.css') contentType = 'text/css';
        if (extname === '.js') contentType = 'application/javascript';


        failsistem.readFile(localPath, function(err, data) {
            if (err) {
                response.writeHead(500);
                response.write('Ошибка сервера');
                response.end();
                return;
            }

            response.writeHead(200, { 
                'Content-Type': contentType + '; charset=utf-8',
                'Cache-Control': 'no-cache'
            });
            response.end(data);
        });
    });
}

var server = http_module.createServer(onrequest);
server.listen(3000, '0.0.0.0');
console.log('Сервер запущен на http://localhost:3000');