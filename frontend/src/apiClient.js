// axios-based Todo API client

import axios from 'axios';


export default class TodoApiClient {
  constructor(baseUrl) {
    this.client = axios.create({
      baseURL: baseUrl,
      headers: {
        Accept: 'application/json',
      },
    });
  }

  async getTodos() {
    return this.client.get('/todos');
  }

  async getTodoById(id) {
    return this.client.get(`/todos/${id}`);
  }

  async getTodosByGroup({ groupId, groupName }) {
    const params = {};
    if (groupId) params.group_id = groupId;
    if (groupName) params.group_name = groupName;

    return this.client.get('/todos', { params });
  }

  async createTodo({ title, description, groups = [] }) {
    const payload = { title, description, groups };

    return this.client.post('/todos', payload);
  }

  async updateTodo(id, { title, description }) {
    return this.client.put(`/todos/${id}`, { title, description });
  }

  async patchTodoGroups(id, { linkGroups = [], unlinkGroups = [] }) {
    return this.client.patch(`/todos/${id}`, {
      linkGroups,
      unlinkGroups,
    });
  }

  // Groups
  async getGroups({ name } = {}) {
    const params = {};
    if (name) params.name = name;

    return this.client.get('/groups', { params });
  }

  async getGroupById(id) {
    return this.client.get(`/groups/${id}`);
  }

  async createGroup({ name, description }) {
    return this.client.post('/groups', { name, description });
  }

  async updateGroup(id, { name, description }) {
    return this.client.put(`/groups/${id}`, { name, description });
  }
}
