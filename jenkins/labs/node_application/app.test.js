const request = require('supertest');
const app = require('./app');

describe('GET /', () => {
    it('should return a message', async () => {
        const res = await request(app).get('/');
        expect(res.statusCode).toEqual(200);
        expect(res.body).toHaveProperty('message', 'Hello, Jenkins!');
    });
});
