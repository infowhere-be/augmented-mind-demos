const express = require('express');
const app = express();

app.use(express.json());

const tasks = [];

app.get('/tasks', (req, res) => {
  res.json(tasks);
});

app.post('/tasks', (req, res) => {
  const task = { id: tasks.length + 1, ...req.body };
  tasks.push(task);
  res.status(201).json(task);
});

app.listen(3000, () => console.log('api-tarefas rodando na porta 3000'));
