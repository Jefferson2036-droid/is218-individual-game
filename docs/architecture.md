# Architecture sketch

Draft. Update when the stack is confirmed.

```mermaid
flowchart LR
  subgraph Browser
    A[Account pages] --> G[Game]
    G --> D[Dashboard]
    D --> U[Account settings]
  end
  A -- register / login --> API
  G -- save result --> API
  D -- read my results --> API
  U -- update account --> API
  API[API: auth, results, users] --> DB[(Database: users, results)]
```

## Data sketch
- `users`: id, email, password_hash, display_name, created_at
- `results`: id, user_id, (score / outcome fields for the chosen concept), played_at

## Open questions
- Does the game run fully in the browser and only send the final result?
- How is a result protected from being faked by the client?
