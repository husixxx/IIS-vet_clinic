import createClient from 'openapi-fetch';
import type { paths } from './api';

const customFetch: typeof fetch = ( input: RequestInfo | URL, { credentials = 'include', ...restConfig }: RequestInit = {}) => {
    return fetch(input, { credentials, ...restConfig });
};

const apiClient = createClient<paths>({ baseUrl: 'http://localhost:5000/', fetch: customFetch, });

export default apiClient;