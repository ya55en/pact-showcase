// Todo API Pact tests
import { PactV3, MatchersV3, SpecificationVersion } from '@pact-foundation/pact'
import { describe, expect, it } from 'vitest'

import path from 'path'
import TodoApiClient from '../../src/apiClient'


const provider = new PactV3({
  consumer: 'TodoApiClient',
  provider: 'TodoBackend',
  spec: SpecificationVersion.SPECIFICATION_VERSION_V4,
  dir: path.resolve(process.cwd(), 'pacts'),
})


const todoExample = {
  title: 'Buy groceries',
  description: 'Milk, Bread, Eggs and others',
}


describe('Todo API', () => {
  it('obtains a list of existing todos', () => {
    provider
      .given('Some todos exist')

      .uponReceiving('a request for all todos')
      .withRequest({
        method: 'GET',
        path: '/todos',
        headers: { Accept: 'application/json' },
      })

      .willRespondWith({
        status: 200,
        headers: { 'Content-Type': 'application/json' },
        body: MatchersV3.eachLike(todoExample)
      })

      provider.executeTest(async (mockserver) => {
        const client = new TodoApiClient(mockserver.url)

        const response = await client.getTodos()

        expect(response.data[0]).to.deep.equal(todoExample)
      })
  })
})
