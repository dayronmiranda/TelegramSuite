graph TD
    A[Start] --> B[Define API Router]
    B --> C[Register Session Endpoint]
    C --> D[Create Telegram Client]
    D --> E{User Authorized?}
    E -->|Yes| F[Save Session to DB]
    E -->|No| G[Request 2FA Code]
    B --> H[Verify Code Endpoint]
    H --> I[Retrieve Session Data]
    I --> J[Sign In with Code]
    J --> K[Return Success]
