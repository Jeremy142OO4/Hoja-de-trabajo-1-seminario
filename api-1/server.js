const http = require("http");

const port = Number(process.env.PORT || 3000);
const studentId = process.env.CARNET || "202300644";
const studentName = process.env.ESTUDIANTE || "Jeremy Estuardo Orellana Aldana";

const server = http.createServer((request, response) => {
  response.setHeader("Content-Type", "application/json; charset=utf-8");

  if (request.method !== "GET") {
    response.writeHead(405, { Allow: "GET" });
    response.end(JSON.stringify({ error: "Method not allowed" }));
    return;
  }

  if (request.url === "/check") {
    response.writeHead(200);
    response.end(JSON.stringify({ status: "OK" }));
    return;
  }

  if (request.url === "/") {
    response.writeHead(200);
    response.end(
      JSON.stringify({
        Instancia: "Instancia #1 - API #1",
        Curso: "Seminario de Sistemas 1",
        Estudiante: `${studentName} - ${studentId}`,
      })
    );
    return;
  }

  response.writeHead(404);
  response.end(JSON.stringify({ error: "Not found" }));
});

server.listen(port, "0.0.0.0", () => {
  console.log(`API #1 listening on port ${port}`);
});
