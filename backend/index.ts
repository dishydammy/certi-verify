import { Express } from "express";

const server = (app: Express) => {
  // Define your server routes and middleware here
  app.get("/", (req, res) => {
    res.send("Hello, World!");
  });

  // Add more routes as needed
}

console.log(server)