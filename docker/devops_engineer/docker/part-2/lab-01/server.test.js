const request = require("supertest");
const express = require("express");

const app = express();
app.get("/", (req, res) => res.send("Hello, Multi-Stage Docker Build!"));

test("GET / should return correct message", async () => {
  const res = await request(app).get("/");
  expect(res.text).toBe("Hello, Multi-Stage Docker Build!");
  expect(res.statusCode).toBe(200);
});
