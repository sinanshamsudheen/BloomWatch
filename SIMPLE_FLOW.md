# Simple BloomWatch Flow

```mermaid
graph LR
    A[User] --> B{Action}
    B -->|Search region & flower| C[Frontend sends request to Backend]
    B -->|Upload flower image| D[Image classification]
    C --> E[Backend processes with AI/ML]
    D --> E
    E --> F[Results to Frontend]
    F --> G[Visualize on Map & Info Panel]
    G --> H[User sees bloom data/explanation]