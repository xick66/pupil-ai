const axios = require('axios');

const baseURL = 'http://127.0.0.1:5000';

const api = axios.create({
  baseURL,
  //   timeout: 5000, // Set a timeout for requests (optional)
});

const screenshot= async() => {
  try {
    const response = await api.get(`/screenshot`);
    return response
  } catch (error) {
    console.error('Error fetching data:', error);
    throw error
  }
}

const conversation = (chat) => {
  return new Promise((resolve, reject) => {
    api.get(`/conversation?question=${chat}`)
      .then(response => {
        resolve(response);
      })
      .catch(error => {
        console.error('Error fetching conversation:', error);
        reject(error);
      });
  });
}

module.exports = {
  screenshot,
  conversation
}
