import { PactV3, SpecificationVersion } from '@pact-foundation/pact'
import path from 'path'


export const createProvider = ({ consumerName, providerName }) => {
  return new PactV3({
    consumer: consumerName,
    provider: providerName,

    spec: SpecificationVersion.SPECIFICATION_VERSION_V4,
    dir: path.resolve(process.cwd(), 'pacts'),
  })
}
