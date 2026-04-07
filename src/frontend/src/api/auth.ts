import client from './client.ts'

type AuthStatus = {
    authenticated: boolean
}

export function getAuthStatus(): Promise<AuthStatus>
{
    return client.get<AuthStatus>("/spotify/auth/status")
        .then(res => res.data);
}

export function auth() {
  window.location.href = "http://localhost:8000/spotify/auth";
}