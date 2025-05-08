// Todo API Pact tests

import { MatchersV3 } from '@pact-foundation/pact'
const { eachLike, like } = MatchersV3
import { describe, expect, it } from 'vitest'

import { createProvider } from '../common'
import TodoApiClient from '../../src/apiClient'


const sampleTodo = {
  title: 'Buy groceries',
  description: 'Milk, Bread, Eggs and others',
  groups: [],
}

const sampleGroup = {
  name: 'Home Stuff',
  description: 'Stuff related to home activities',
}


describe('Todo API', () => {
  it('obtains a list of existing todos', () => {
    const provider = newProvider()

    provider
      .given('Some todos exist')

      .uponReceiving('a request for all todos')
      .withRequest({
        method: 'GET',
        path: '/todos',
        // headers: { Accept: 'application/json' },
      })

      .willRespondWith({
        status: 200,
        headers: { 'Content-Type': 'application/json' },
        body: eachLike(sampleTodo)
      })

    return provider.executeTest(async (mockserver) => {
      const client = new TodoApiClient(mockserver.url)

      const response = await client.getTodos()

      expect(response.data[0]).to.deep.equal(sampleTodo)
    })
  })

  it('obtains a specific todo by ID', () => {
    const provider = newProvider()
    const todoId = 1

    provider
      .given(`A todo with ID ${todoId} exists`)

      .uponReceiving('a request for a single todo')
      .withRequest({
        method: 'GET',
        path: `/todos/${todoId}`,
        headers: { Accept: 'application/json' },
      })

      .willRespondWith({
        status: 200,
        headers: { 'Content-Type': 'application/json' },
        body: like(sampleTodo)
      })

    return provider.executeTest(async (mockserver) => {
      const client = new TodoApiClient(mockserver.url)

      const response = await client.getTodoById(todoId)

      expect(response.data).to.deep.equal(sampleTodo)
    })
  })

  it('creates a new Todo', () => {
    const provider = newProvider()

    provider
      .uponReceiving('a request to create a new todo')
      .withRequest({
        method: 'POST',
        path: '/todos',
        headers: { Accept: 'application/json' },
        body: sampleTodo,
      })

      .willRespondWith({
        status: 201,
        headers: { 'Content-Type': 'application/json' },
        body: { id: like(1) },
      })

    return provider.executeTest(async (mockserver) => {
      const client = new TodoApiClient(mockserver.url)

      const response = await client.createTodo(sampleTodo)

      expect(response.data).to.deep.equal({ id: 1 })
    })
  })


  it('obtains all existing groups', () => {
    const provider = newProvider()

    provider
      .given('Some groups exist')

      .uponReceiving('a request for all groups')
      .withRequest({
        method: 'GET',
        path: '/groups',
        headers: { Accept: 'application/json' },
      })

      .willRespondWith({
        status: 200,
        headers: { 'Content-Type': 'application/json' },
        body: eachLike(sampleGroup),
      })

    return provider.executeTest(async (mockserver) => {
      const client = new TodoApiClient(mockserver.url)

      const response = await client.getGroups()

      expect(response.data[0]).to.deep.equal(sampleGroup)
    })
  })

  it('obtains a specific group by ID', () => {
    const provider = newProvider()
    const groupId = '1'

    provider
      .given(`A group with ID ${groupId} exists`)

      .uponReceiving('a request for a single group')
      .withRequest({
        method: 'GET',
        path: `/groups/${groupId}`,
        headers: { Accept: 'application/json' },
      })

      .willRespondWith({
        status: 200,
        headers: { 'Content-Type': 'application/json' },
        body: like(sampleGroup),
      })

    return provider.executeTest(async (mockserver) => {
      const client = new TodoApiClient(mockserver.url)

      const response = await client.getGroupById(groupId)

      expect(response.data).to.deep.equal(sampleGroup)
    })
  })

  it('creates a new group', () => {
    const provider = newProvider()
    const groupExample = { name: 'Group A', description: 'A sample group' }

    provider
      .uponReceiving('a request to create a new group')
      .withRequest({
        method: 'POST',
        path: '/groups',
        headers: { Accept: 'application/json' },
        body: groupExample,
      })

      .willRespondWith({
        status: 201,
        headers: { 'Content-Type': 'application/json' },
        body: { id: like(1) },
      })

    return provider.executeTest(async (mockserver) => {
      const client = new TodoApiClient(mockserver.url)

      const response = await client.createGroup(groupExample)

      expect(response.data).to.deep.equal({ id: 1 })
    })
  })

})


/** helpers **/


const newProvider = () => {
  return createProvider({
    consumerName: 'TodoApiClient',
    providerName: 'TodoBackend',
  })
}
