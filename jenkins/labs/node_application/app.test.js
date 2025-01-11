const request = require('supertest');
const app = require('./app'); // Import your app

let server; // Store the server instance

beforeAll(() => {
    // Start the server before tests
    server = app.listen(3000, () => {
        console.log('Test server running at http://localhost:3000/');
    });
});

afterAll(() => {
    // Close the server after tests
    server.close(() => {
        console.log('Test server closed');
    });
});

describe('GET /', () => {
    it('should return a message', async () => {
        const res = await request(app).get('/');
        expect(res.statusCode).toEqual(200);
        expect(res.body).toHaveProperty('message', 'Hello, Jenkins!');
    });
});
